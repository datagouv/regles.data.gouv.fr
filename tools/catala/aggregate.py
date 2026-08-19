import json 

def profondeur(valeur) -> int:
    """
    Calcule la profondeur d'une valeur : 1 pour une valeur simple (texte,
    nombre, booleen), et 1 de plus a chaque niveau de dict ou de liste
 
    """
    if isinstance(valeur, dict):
        return 1 + max((profondeur(v) for v in valeur.values()), default=1)
    if isinstance(valeur, list):
        return 1 + max((profondeur(v) for v in valeur), default=1)
    return 1

def noms(valeur) -> dict:
    """
    Recupere les noms associes a une valeur, selon sa forme :
    dict -> ses cles ; si une valeur associee est elle-meme un dict/liste, on descend dedans pour recuperer ses noms aussi (recursif)
    liste -> ses elements simples, ou les noms de ses elements s'ils sont eux-memes des dict/liste
    """
    if isinstance(valeur, dict) and len(valeur) == 1:
        contenu = next(iter(valeur.values()))
        return noms(contenu) if isinstance(contenu, (dict, list)) else {}

    resultat = {}
    if isinstance(valeur, dict):
        for cle, sous_valeur in valeur.items():
            resultat[cle] = noms(sous_valeur) if isinstance(sous_valeur, (dict, list)) else type_de(sous_valeur)
    elif isinstance(valeur, list):
        for item in valeur:
            if isinstance(item, dict):
                for cle, sous_valeur in item.items():
                    resultat[cle] = noms(sous_valeur) if isinstance(sous_valeur, (dict, list)) else type_de(sous_valeur)
            elif isinstance(item, list):
                resultat.update(noms(item))
            else:
                resultat[item] = type_de(item)
    return resultat
 


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
                if profondeur(valeur) == 1:
                    inputs.setdefault(nom, type_de(valeur))
                else:
                    if not isinstance(inputs.get(nom), dict):
                        inputs[nom] = {}
                    inputs[nom].update(noms(valeur))
 
        for out in resultat.get("outputs", []):
            if out["path"][:-1] == main_path:
                nom = out["path"][-1]
                valeur = out["value"]
                if profondeur(valeur) == 1:
                    outputs.setdefault(nom, type_de(valeur))
                else:
                    if not isinstance(outputs.get(nom), dict):
                        outputs[nom] = {}
                    outputs[nom].update(noms(valeur))
 
        # recup les fonctions intermediaires - surtout leurs variables
        for c in resultat.get("scope_calls", []):
            if c.get("level", 0) >= 2:
                entry = intermediaires.setdefault(c["scope_call"], {"vars": set(), "count": 0})
                entry["vars"].add(c["scope_var"])
                entry["count"] += 1
 
    appels_intermediaires = [
        {"scope_call": nom, "depend_de": sorted(info["vars"]), "occurrences": info["count"]}
        for nom, info in intermediaires.items()
    ]
    return {
        "scope_call": scope_call,
        "nb_cas_analyses": cas_retenus,
        "inputs": inputs,
        "outputs": outputs,
        "appels_intermediaires": appels_intermediaires,
    }
 

def write_html_overview(overview: dict, filepath: str = "vue-fonction.html", template_path: str = "template.html") -> None:
    """
    Ecrit une page HTML autonome (CSS + JS inclus, aucune dependance externe)
    affichant "overview" (le dict renvoye par to_function_overview) sous
    forme de 3 boîtes : Entrées / Fonctions appelées / Sorties.
 
    Le template HTML vit dans un fichier a part (template.html), avec un
    marqueur __OVERVIEW_JSON__ a l'endroit ou les donnees doivent s'inserer.
    """
    with open(template_path, encoding="utf-8") as f:
        template = f.read()
 
    overview_json = json.dumps(overview, ensure_ascii=False, indent=2)
    html = template.replace("__OVERVIEW_JSON__", overview_json)
 
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
 


def main():
    with open("resultats.json", encoding="utf-8") as f:
        resultats = json.load(f)
 
    overview = function_overview(resultats, "CalculPointsAideScolarite")
    
    with open("function-overview.json", "w", encoding="utf-8") as f:
        json.dump(overview, f, indent=2, ensure_ascii=False)
 
    write_html_overview(overview, "vue-fonction.html")
 
    print("Écrit dans function-overview.json et vue-fonction.html")
 
 
 
if __name__ == "__main__":
    main()
 

