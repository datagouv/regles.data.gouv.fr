import pytest 
import json
from catala.trace_retrieval import trace_explorer, parse_resultat_input
#Formalisme : test_nom_fichier - les fichier test détectables par pytest 
# décorateurs, configuration de tests - avec conftest - remplir des données, etc. -- pour les bdd 

def test_trace_explorer():
    file_path = "test-aide4.json"
    with open(file_path, "r") as file:
        data = json.load(file)
    # s.q. sort le test complet. On veut que la fonction renvoie le label en entier 
   
    assert(trace_explorer(data)["label"] == "Cas N°4 : logement separe, l'adresse des parents est moins avantageuse")

    input_data={ 
        "valeur_point": 10.00,
        "trajet_depuis_domicile_agent": {
            "distance_km": 60,
            "durée_minutes": 50
            },
        "trajet_depuis_domicile_étudiant": {
            "distance_km": 32,
            "durée_minutes": 20
        },
        "montant_matériel_spécifique" : 0.0,
        "étudiant_en_filière_post_bac": False
    }
    tmp = trace_explorer(data)
    print(tmp)

    tmp_parse = parse_resultat_input(tmp, {})
    print(tmp_parse)
   
  
    #breakpoint()
    assert(tmp_parse == input_data)
# OK besoin de changer les types - ils sont tous en STR au moment de récupération des données vs float / bool dans le dictionnaire inputs 
# Est-ce que si les infos ne sont pas dans le même ordre dans le dico ça peut quand même le faire pour assert ? 