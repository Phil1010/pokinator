from flask import Flask, render_template, request, redirect, url_for
from akinator import create_pokinator 
import numpy as np
import matplotlib.pyplot as plt
from sklearn import tree

app = Flask(__name__)

# Fonction pour initialiser le pokinator
def initialize_pokinator():
    global p
    p = create_pokinator()

@app.route('/')
def index():    
    initialize_pokinator()
    p.show_tree()
    return render_template('index.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        answer = request.form['answer']
        if answer == 'Oui':
            p.current_node = p.get_yes_node()
        else:
            p.current_node = p.get_no_node()

        if p.is_terminal():
            print("noeud terminal")
            return redirect(url_for('result'))
        else:
            return render_template('question.html', feature=p.get_feature())
    else:
        return render_template('question.html', feature=p.get_feature())

@app.route('/result')
def result():
    return render_template('result.html', guess=p.guess())


@app.route('/add_pokemon', methods=['GET', 'POST'])
def add_pokemon():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        sample = request.form['sample']
        feature = request.form['feature']

        # Ajouter le nouvel individu dans l'arbre
        p.add_sample_label(sample)
        p.add_feature_label(feature)
        
        p.update_tree()

        # Rediriger vers la page d'accueil
        return render_template('index.html')
    else:
        return render_template('add_pokemon.html')

if __name__ == '__main__':
    app.run(debug=True)
