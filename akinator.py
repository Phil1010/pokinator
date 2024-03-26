import matplotlib.pyplot as plt
import numpy as np

from sklearn import tree

import sqlite3

con = sqlite3.connect("database.db")

cursor = con.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS sample (id INTEGER PRIMARY KEY AUTOINCREMENT, pokemon TEXT UNIQUE)")
cursor.execute("CREATE TABLE IF NOT EXISTS feature (id INTEGER PRIMARY KEY AUTOINCREMENT, feature TEXT UNIQUE)")
cursor.execute("CREATE TABLE IF NOT EXISTS sample_feature (sample_id INTEGER, feature_id INTEGER, FOREIGN KEY(sample_id) REFERENCES sample(id), FOREIGN KEY(feature_id) REFERENCES feature(id))")

class Pokinator:
    def __init__(
            self, 
        ):

        # self.load_db()


        self.classifier = tree.DecisionTreeClassifier()
        # self.classifier = self.classifier.fit(self.samples, self.features)

        # self.tree = self.classifier.tree_

        self.current_node = 0

    def get_feature_index(self, feature_res, feature_id):
        i = 0
        for feature_tuple in feature_res:
            (id, feature) = feature_tuple
            if (feature_id == id):
                return i
            
            i += 1

        return -1

    def load_db(self):
        sample_res = cursor.execute("select id, pokemon from sample").fetchall()
        feature_res = cursor.execute("select id, feature from feature").fetchall()

        self.samples = []
        self.samples_labels = []
        self.features_labels = []
        self.features = []

        for feature_tuple in feature_res:
            (id, feature) = feature_tuple
            self.features_labels.append(feature)


        for sample_tuple in sample_res: # pour chaque pokemon
            (id, pokemon) = sample_tuple

            s = np.zeros(len(feature_res)) # on initialise sample vide

            sample_feature_res = cursor.execute("select feature_id from sample_feature where sample_id = ?", [id]).fetchall()
            for sample_feature_tuple in sample_feature_res: # on check toutes ses features
                (feature_id,) = sample_feature_tuple
                # on trouve la place de la feature dans la liste
                index = self.get_feature_index(feature_res, feature_id)
                if index != -1:
                    s[index] = 1

            self.samples.append(s)
            self.features.append(id)
            self.samples_labels.append(pokemon)


    def update_tree(self):
        self.load_db()
        print(self.samples, self.samples_labels, self.features, self.features_labels)
        print(len(self.samples), len(self.features))

        self.classifier = self.classifier.fit(self.samples, self.features)
        self.tree = self.classifier.tree_

    def get_feature(self):
        feature_index = self.tree.feature[self.current_node]
        return self.features_labels[feature_index]
    
    def get_sample():
        pass
    
    def get_yes_node(self):
        yes_node = self.tree.children_right[self.current_node]
        return yes_node
    
    def get_no_node(self):
        no_node = self.tree.children_left[self.current_node]
        return no_node

    def show_tree(self):
        plt.figure()
        tree.plot_tree(
            self.classifier, 
            feature_names=self.features_labels, 
            class_names=self.samples_labels,
            filled=True,
        )
        plt.show()

    def is_terminal(self):
        return self.get_yes_node() == -1 or self.get_no_node() == -1
    
    def guess(self):
        samples_labels_index = self.tree.value[self.current_node].argmax()
        return self.samples_labels[samples_labels_index]

    def answer(self, answer):
        if answer == "yes":
            self.current_node = self.get_yes_node()
        else:
            self.current_node = self.get_no_node()

    def add_sample(self, sample: str):
        res = cursor.execute("select pokemon from sample where pokemon = ?", (sample,))
        if (len(res.fetchall()) == 0):
            cursor.execute("insert into sample (pokemon) values (?)", (sample,))
            con.commit()

    def add_feature(self, feature: str):
        res = cursor.execute("select feature from feature where feature = ?", (feature,))
        if (len(res.fetchall()) == 0):
            cursor.execute("insert into feature (feature) values (?)", (feature,))
            con.commit()

    def add_sample_feature(self, sample: str, feature: str):
        sample_id = cursor.execute("select id from sample where pokemon = ?", (sample,)).fetchall()
        feature_id = cursor.execute("select id from feature where feature = ?", (feature,)).fetchall()
        print(sample_id, feature_id)
        cursor.execute("insert into sample_feature (sample_id, feature_id) values (?, ?)", [sample_id[0][0], feature_id[0][0]])
        con.commit()


    # def add_sample_label(self, sample_label):
    #     try: # si le nom du pokemon est déjà dans la liste
    #         index = self.samples_labels.index(sample_label)
    #         self.features.append(index)

    #     except: # s'il ne l'est pas encore
    #         self.samples_labels.append(sample_label)
    #         self.features.append(len(self.features))


    # def add_feature_label(self, feature_label):
    #     try: 
    #         index = self.features_labels.index(feature_label) # on vérifie si la feature existe

    #         samples_labels_index = self.tree.value[self.current_node].argmax()
    #         sample = self.samples[samples_labels_index].copy()
    #         sample[index] = 1
    #         self.samples.append(sample) # on ajoute un exemple d'individu
            
    
    #     except: 
    #         samples_labels_index = self.tree.value[self.current_node].argmax()
    #         self.samples.append(self.samples[samples_labels_index]) # on ajoute un exemple d'individu
    #         self.samples = np.hstack((self.samples, np.zeros((len(self.samples), 1))))
    #         self.features_labels.append(feature_label)
    #         self.samples[len(self.features) - 1][len(self.features_labels) - 1] = 1

          

samples_labels = ["bulbizarre", "salameche", "carapuce"]

features_labels = ["vert", "rouge", "bleu", "test"]

samples = [
    [1, 0, 0, 1], # bulbizarre
    [0, 1, 0, 1], # salameche
    [0, 0, 1, 0], # carapuce
]

features = [
    0, # bulbizarre
    1, # salameche
    2, # carapuce
]

# pa = PokemonAkinator(X, class_names, y, feature_names)

# pa.jouer()

p = Pokinator()
# p.add_sample_label("nicolas")
# p.add_feature_label("bipède")

# print(p.samples, p.samples_labels, p.features, p.features_labels)

while True:
    p.load_db()
    p.update_tree()
    p.show_tree()
    while not p.is_terminal():
        print(p.get_feature())
        yesno = input("yes / no\n")
        p.answer(yesno)

    print(p.guess())

    yesno = input("yes / no\n")
    if yesno == "no":
        sample = input("nom pokemon")
        p.add_sample(sample)

        feature = input("caractéristique pokémon")
        p.add_feature(feature)
        p.add_sample_feature(sample, feature)

    p.update_tree()
