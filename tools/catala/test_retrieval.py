import json
def trace_explorer(trace : dict, predicate, path = None) -> dict : 
    """ 
    Une fonction qui explore l'arbre de la trace 
    et extrait les valeurs selon le predicat donné (d'abord conçu pour "only_input")
    Exploration se fait grâce à la trace 
    NON TESTE 
    """
    resultat = []
    #eviter le fait que ça reinitialise tout le temps - car c'est une fonction recursive !
    if path == None :
        path = []
    
    # parcourt les élements de la trace - à chaque niveau.
    # check si c'est un dictionnaire ou pas et si ça contient element - sinon pas de value
    if isinstance(trace, dict) and "element" in trace:
        ele = trace["element"]
        name = ele.get("name") or ele.get("kind") # donner le nom du element
        # nom du élément constitue le chemin - pour rémonter dans l'arbre / mieux comprendre 
        current_path = path + [name]
        if predicate(ele):
            #pos = trace.get("pos", {})
            # je voulais recup la position - mais je ne sais pas si c'est utile ?
            resultat.append({
                "path": current_path,
                "value": trace.get("value"),
                #"file": pos.get("file"),
                #"start" : pos.get("start")
            }) # rajout dico qui contient le path, la valeur, et la position 
        for child in trace.get("trace", []) : 
            #car il existe une trace au sein de chaque niveau -- > on peut naviguer avec ! 
            resultat.extend(trace_explorer(child, predicate, current_path)
            )
    return resultat
    



def main():
    file_path = "test-aide4.json"
    with open(file_path, "r") as file:
        trace = json.load(file)

    # matcher sur le predicat (apparemment la meilleure façon de faire ? )
    matches = []
    for item in trace:
        matches.extend(trace_explorer(item, lambda el: el.get("input") == "only_input"))

    print(matches)


main()



"""
# ANCIENNES FONCTIONS  
def trace_explorer(trace : dict, output: dict) -> dict : 
  
    # parcourt les élements de la trace - à chaque niveau. 
    ele = trace["element"]
    
    if ele["input"] == "only_input" :
        value = trace["value"] 
        output[f"name_{ele["dec1_pos"]["start"]["line"]}_{ele["dec1_pos"]["start"]["character"]}"] = value
    

    # Si input - recupere et continue l'exploration
    trace_explorer(trace["trace"], output)
    # si jamais l'objet trace - si jamais on voit trace n+1 - explorer de trace n+1, sinon sort

def input_retrieval(trace: dict) -> dict:
    trace = trace[0]["trace"]
    # Methode 1 - reccursive soit boucle - dès que detecte only input - profondeur puis lecture du champ value - différents niveaux d'imbrication


    # Methode 2 regex qui detecte les only_input --> lit la variable plus bas. 
    pass

def main():
    file_path = "test-aide4.json"
    with open(file_path, "r") as file:
        trace = json.load(file)
    input_retrieval(trace)

"""