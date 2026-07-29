import pytest 
import json
from catala.trace_retrieval import trace_explorer
#Formalisme : test_nom_fichier - les fichier test détectables par pytest 
# décorateurs, configuration de tests - avec conftest - remplir des données, etc. -- pour les bdd 

def test_trace_explorer():
    file_path = "test-aide4.json"
    with open(file_path, "r") as file:
        data = json.load(file)
    # s.q. sort le test complet. On veut que la fonction renvoie le label en entier 
    assert(label == trace_explorer(data, lambda el: el.get("input") == "only_input")["label"])