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
    assert(trace_explorer(data)["label"] == "Cas N°4 : logement separe, l'adresse des parents est moins avantageuse")
    input_data={ valeur_point: 10.00,
      trajet_depuis_domicile_agent: Trajet {
        distance_km: 60, # trajet agent 2 points mais retire le C2
        durée_minutes: 50
      },
      trajet_depuis_domicile_étudiant: Présent contenu Trajet {
        distance_km: 32,# trajet etudiant 2 points
        durée_minutes: 20
      },
      montant_matériel_spécifique : 0€
      étudiant_en_filière_post_bac: faux
    }
