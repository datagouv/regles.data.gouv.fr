import json 

def type_de(valeur) -> str:
    """ Deduit un type lisible pour une valeur simple (pas un objet/liste). """
    return "booléen" if isinstance(valeur, bool) else "texte/nombre"
 

def function_overview(resultats : list, scope_call : str) -> dict : 
    """
    Une fonction qui prend en entrée le fichier de resultats.json (qui est une liste) pour aggréger les tests d'une fonction donnée (scope_call = fonction en catala) et en récupérer : 
    - tous les inputs possibles - union des noms de variables d'entrée 
    - tous les outputs : de même que les inputs 
    - appels intermédiaires et les variables associaées (scope call / scope var)
    """
    inputs = dict()
    outputs = dict()
    intermediaires = dict()
    # initialisation 
    cas_retenus = 0 
    for resultat in resultats : 
        main_call = None 
        for appel in resultat.get("scope_calls", []): 
            if appel.get("level") ==1: 
                main_call = appel 
                break 
        if main_call is None or main_call["scope_call"]!= scope_call : 
            continue 
        cas_retenus+=1
        main_path = main_call["path"]

        # chercher dans les inputs les paths et recup la dernière variable pour le nom de la variable input. 
        for inp in resultat.get("inputs", []):
            if inp["path"][:-1] == main_path:
                nom = inp["path"][-1]
                valeur = inp["value"]
                # on deplie l'optionnel a la Catala ({"Présent": {...}})
                if isinstance(valeur, dict) and "Présent" in valeur:
                    valeur = valeur["Présent"]
                if isinstance(valeur, dict):
                    inputs.setdefault(nom, {})
                    for sous_nom, sous_valeur in valeur.items():
                        inputs[nom][sous_nom] = type_de(sous_valeur)
                elif valeur != "Absent":
                    inputs[nom] = type_de(valeur)
 
        for out in resultat.get("outputs", []):
            if out["path"][:-1] == main_path:
                nom = out["path"][-1]
                valeur = out["value"]
                if isinstance(valeur, list):
                    outputs.setdefault(nom, {})
                    for item in valeur:
                        if isinstance(item, dict):
                            for sous_nom, sous_valeur in item.items():
                                outputs[nom][sous_nom] = type_de(sous_valeur)
                else:
                    outputs[nom] = type_de(valeur)
# recup les fonctions intermediaires - surtout leurs variables 
        for c in resultat.get("scope_calls", []):
            if c.get("level", 0) >= 2:
                entry = intermediaires.setdefault(c["scope_call"], {"vars": set(), "count": 0})
                entry["vars"].add(c["scope_var"])
                entry["count"] += 1

    appels_intermediaires = [
        {"scope_call": nom, "depend_de": sorted(info["vars"]), "occurrences": info["count"]}
        for nom, info in intermediaires.items()]
    for dico in (inputs, outputs):
        for entree in dico.values():
            if "valeurs" in entree:
                entree["valeurs"] = sorted(entree["valeurs"], key=str)

    return {
        "scope_call": scope_call,
        "nb_cas_analyses": cas_retenus,
        "inputs": inputs,
        "outputs": outputs,
        "appels_intermediaires": appels_intermediaires,
    }
 


def main():
    with open("resultats.json", encoding="utf-8") as f:
        resultats = json.load(f)
 
    overview = function_overview(resultats, "CalculPointsAideScolarite")
    print(json.dumps(overview, indent=2, ensure_ascii=False))
 
 
if __name__ == "__main__":
    main()
 

