import json
import re

def fetch_label(data: dict):
    return data.get("element").get("decl_pos").get("law_headings")[0]

def trace_explorer(trace : dict, resultat: dict = {}, path = None) -> dict : 
    """ 
    Une fonction qui explore l'arbre de la trace 
    et extrait les valeurs selon le predicat donné (d'abord conçu pour "only_input")
    Exploration se fait grâce à la trace 
    NON TESTE 
    """
    #eviter le fait que ça reinitialise tout le temps - car c'est une fonction recursive !
    trace = trace[0]

    if path == None :
        resultat = {
            "inputs": [],
        }
        path = []
        resultat["label"] = fetch_label(trace)
    #breakpoint()
    predicate = lambda el: el.get("input") == "only_input"
    # parcourt les élements de la trace - à chaque niveau.
    # check si c'est un dictionnaire ou pas et si ça contient element - sinon pas de value
    if "element" in trace:
        ele = trace["element"]
        name = ele.get("name") or ele.get("kind") # donner le nom du element
        # nom du élément constitue le chemin - pour rémonter dans l'arbre / mieux comprendre 
        current_path = path + [name] 
        # TODO recupe le kind pour savoir si c'est une var ou une fonction
        if predicate(ele):
            #pos = trace.get("pos", {})
            # je voulais recup la position - mais je ne sais pas si c'est utile ?
            resultat['inputs'].append({
                "path": current_path,
                "value": trace.get("value"),
                #"file": pos.get("file"),
                #"start" : pos.get("start")
            }) # rajout dico qui contient le path, la valeur, et la position 
        for child in trace.get("trace", []) : 
            #car il existe une trace au sein de chaque niveau -- > on peut naviguer avec ! 
            if 'element' in child:
                trace_explorer([child], resultat, current_path) #ok 
                #resultat['inputs'].extend(trace_explorer(child['trace'], resultat, current_path))
    return resultat

def parse_resultat_input(resultat : dict, parsed : dict ) -> dict : 
    """
    Fonction qui permet de parser l'entrée 'input' du dictionnaire résultat pour le remettre au bon format
    """
    inputs = resultat.get("inputs")
    # pour chaque élement dans cette liste
    for inp in inputs : 
        path = inp.get("path")
        key = path[-1]
        parsed[key] = inp["value"]
    # en faire un set pour que ce soit compatible avec l'output qu'on veut
    return parsed

def extract_catala_test_inputs(content: str, test_name: str) -> list[str]:
    """
    Extracts all inputs (lines starting with '--') for a specific Catala test.
    
    Args:
        content (str): The full text of the .catala_fr file or snippet.
        test_name (str): The exact name of the test/function.
        
    Returns:
        list[str]: A list of input strings found within that test block.
    """
    # 1. Match the test declaration block until the next test declaration or end of file
    pattern = rf"(?:déclaration )?champ d'application {re.escape(test_name)}:[\s\S]*?(?=(?:déclaration )?champ d'application\s|#[\n\r]|\Z)"
    
    match = re.search(pattern, content)
    breakpoint()
    if not match:
        breakpoint()
        return []
        
    # 2. Remove the declaration line itself to focus only on the inputs/block
    block = "\n".join(match.group(0).split('\n')[1:])
    
    # 3. Extract all lines starting with '--' (ignoring leading whitespace)
    inputs = re.findall(r'^\s*--\s*(.+)$', block, re.MULTILINE)
    
    return [inp.strip() for inp in inputs if inp.strip()]

def main():
    file_path = "test-aide4.json"
    with open(file_path, "r") as file:
        trace = json.load(file)[0]
    
    file_path = "tests_aide_scolarite.catala_fr"
    with open(file_path, "r") as file_cat:
        text = file_cat.read()
        print(text)
    inputs = extract_catala_test_inputs(text, "TestCalculPointsAideScolarite4") 
    print(inputs)
    # matcher sur le predicat (apparemment la meilleure façon de faire ? )
    #matches = []
    #matches.extend(trace_explorer(trace, path = None))
    #breakpoint()
    #print(matches)
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