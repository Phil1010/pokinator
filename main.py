class_names = ["bulbizarre", "salameche", "carapuce"]

feature_names = ["vert", "rouge", "bleu", "test"]

X = [
    [1, 0, 0, 1], # bulbizarre
    [0, 1, 0, 1], # salameche
    [0, 0, 1, 0], # carapuce
]

y = [
    0, # bulbizarre
    1, # salameche
    2, # carapuce
]

pa = PokemonAkinator(X, class_names, y, feature_names)

pa.jouer()