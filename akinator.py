import matplotlib.pyplot as plt
import numpy as np

from sklearn import tree

from database import Database

samples = []
samples_labels = []
features_labels = []
features = []

class Pokinator:
    def __init__(
        self, 
    ):

        self.classifier = tree.DecisionTreeClassifier()
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
       self.db = Database()
       (self.features, self.features_labels, self.samples, self.samples_labels) = self.db.get_samples()
       

    def update_tree(self):
        self.load_db()

        print(self.samples, self.features)

        self.classifier = self.classifier.fit(self.samples, self.features)
        self.tree = self.classifier.tree_

    def get_feature(self):
        samples_index = self.tree.value[self.current_node].argmax()
        feature_index = self.tree.feature[self.current_node]
        return self.features_labels[feature_index]
    
    def get_sample(self):
        samples_index = self.tree.value[self.current_node].argmax()
        return self.samples[samples_index]

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

    def insert_sample(self, pokemon_label: str, feature_label_list: list[str]):
        self.db.insert_sample(pokemon_label, feature_label_list)

# samples_labels = ["bulbizarre", "salameche", "carapuce"]

# features_labels = ["vert", "rouge", "bleu", "test"]

# samples = [
#     [1, 0, 0, 1], # bulbizarre
#     [0, 1, 0, 1], # salameche
#     [0, 0, 1, 0], # carapuce
# ]

# features = [
#     0, # bulbizarre
#     1, # salameche
#     2, # carapuce
# ]

# # pa = PokemonAkinator(X, class_names, y, feature_names)

# # pa.jouer()

p = Pokinator()
# # p.add_sample_label("nicolas")
# # p.add_feature_label("bipède")

# # print(p.samples, p.samples_labels, p.features, p.features_labels)

while True:
    p.load_db()
    p.update_tree()
    p.show_tree()
    while not p.is_terminal():
        print(p.get_feature())
        yesno = input("yes / no\n")
        p.answer(yesno)

    print(p.guess())
    print(p.get_sample())

    yesno = input("yes / no\n")
    if yesno == "no":
        feature_label_list = []
        for i, sample in enumerate(p.get_sample()):
            if (sample == 1):
                feature_label_list.append(p.features_labels[i])

        sample_label = input("nom pokemon\n")
        feature_label_list.append(input("caractéristique pokémon\n"))
        p.insert_sample(sample_label, feature_label_list)

    
    p.update_tree()
