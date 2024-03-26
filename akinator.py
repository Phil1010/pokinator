import matplotlib.pyplot as plt
import numpy as np

from sklearn import tree

class Pokinator:
    def __init__(
            self, 
            samples, 
            samples_labels, 
            features, 
            features_labels
        ):

        self.classifier = tree.DecisionTreeClassifier()
        self.classifier = self.classifier.fit(samples, features)

        self.tree = self.classifier.tree_

        self.samples = samples 
        self.samples_labels = samples_labels
        self.features = features
        self.features_labels = features_labels

        self.current_node = 0

    def update_tree(self):
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
            filled=True
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

    def add_sample_label(self, sample_label):
        try: # si le nom du pokemon est déjà dans la liste
            index = self.samples_labels.index(sample_label)
            self.features.append(index)

        except: # s'il ne l'est pas encore
            self.samples_labels.append(sample_label)
            self.features.append(len(self.features))


    def add_feature_label(self, feature_label):
        try: 
            index = self.features_labels.index(feature_label) # on vérifie si la feature existe

            samples_labels_index = self.tree.value[self.current_node].argmax()
            sample = self.samples[samples_labels_index].copy()
            sample[index] = 1
            self.samples.append(sample) # on ajoute un exemple d'individu
            
    
        except: 
            samples_labels_index = self.tree.value[self.current_node].argmax()
            self.samples.append(self.samples[samples_labels_index]) # on ajoute un exemple d'individu
            self.samples = np.hstack((self.samples, np.zeros((len(self.samples), 1))))
            self.features_labels.append(feature_label)
            self.samples[len(self.features) - 1][len(self.features_labels) - 1] = 1

          

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

p = Pokinator(samples, samples_labels, features, features_labels)
# p.add_sample_label("nicolas")
# p.add_feature_label("bipède")

# print(p.samples, p.samples_labels, p.features, p.features_labels)

while True:
    p.show_tree()
    while not p.is_terminal():
        print(p.get_feature())
        yesno = input("yes / no\n")
        p.answer(yesno)

    print(p.guess())

    yesno = input("yes / no\n")
    if yesno == "no":
        sample = input("nom pokemon")
        p.add_sample_label(sample)

        feature = input("caractéristique pokémon")
        p.add_feature_label(feature)

    p.update_tree()
