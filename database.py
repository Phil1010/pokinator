import sqlite3
import numpy as np

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()

        self.init_tables()

    def init_tables(self):
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS pokemon (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    label TEXT
                    )""")

        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS feature (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    label TEXT UNIQUE
                    )""")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sample (
                pokemon_id INTEGER,
                feature_id INTEGER, 
                FOREIGN KEY(pokemon_id) REFERENCES pokemon(id),
                FOREIGN KEY(feature_id) REFERENCES feature(id),
                CONSTRAINT unique_pokemon_feature UNIQUE (pokemon_id, feature_id)
            )""")

    def insert_pokemon(self, pokemon_label: str) -> int | None: 
        self.cursor.execute("INSERT INTO pokemon (label) values (?)", [pokemon_label])
        self.conn.commit()
        return self.cursor.lastrowid

    def get_pokemon(self, pokemon_label: str) -> list[tuple[int, str]]: 
        return self.cursor.execute("SELECT id, label FROM pokemon WHERE label = ?", [pokemon_label]).fetchall()[0]

    def insert_feature(self, feature_label: str) -> int | None:
        self.cursor.execute("INSERT INTO feature (label) values (?)", [feature_label])
        self.conn.commit()
        return self.cursor.lastrowid

    def get_feature(self, feature_label: str) -> tuple[int, str]: 
        return self.cursor.execute("SELECT id, label FROM feature WHERE label = ?", [feature_label]).fetchall()[0]

    def insert_sample(self, pokemon_label: str, feature_label_list: list[str]):
        pokemon_id = self.insert_pokemon(pokemon_label)
        
        for feature in feature_label_list:
            (feature_id, feature_label) = (-1, feature)

            try: # on essaye de récupérer la feature par label
                (feature_id, feature_label) = self.get_feature(feature)
            except: # si on la trouve pas on l'ajoute
                feature_id = self.insert_feature(feature)

            print(pokemon_id, feature_id)           
            self.cursor.execute("INSERT INTO sample (pokemon_id, feature_id) values (?, ?)", [pokemon_id, feature_id])
            self.conn.commit()

    def get_all_pokemons(self):
        return self.cursor.execute("select id, label from pokemon").fetchall()

    def get_samples(self):
        f = {}
        feature = []
        feature_label = []
        samples = []
        samples_labels = []

        samples_list = self.cursor.execute(
            """
            SELECT 
                p.id AS pokemon_id,
                p.label AS pokemon_label,
                GROUP_CONCAT(CASE WHEN sf.pokemon_id IS NULL THEN 0 ELSE 1 END) AS features
            FROM 
                pokemon p
            CROSS JOIN feature f
            LEFT JOIN sample sf ON p.id = sf.pokemon_id AND f.id = sf.feature_id
            WHERE p.id IN (SELECT DISTINCT pokemon_id FROM sample)
            GROUP BY p.id;
            """
        ).fetchall()

        for (pokemon_id, pokemon_label, feature_list) in samples_list:
            try:
                f[pokemon_label]
            except:
                f[pokemon_label] = len(f)
           
            feature.append(f[pokemon_label])
            samples_labels.append(pokemon_label)

            feature_list = np.array(feature_list.split(","), dtype=int)
            samples.append(feature_list)

        feature_list = self.cursor.execute(
            """
            SELECT 
                label
            FROM
                feature
            """
        ).fetchall()

        for (label,) in feature_list:
            feature_label.append(label)

        print("LISTE DES F", f)

        return (feature, feature_label, samples, samples_labels)


