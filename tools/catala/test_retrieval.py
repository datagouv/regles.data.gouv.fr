import json
def trace_explorer(trace : dict, output: dict) -> dict : 
    """ 
    Une fonction qui explore l'arbre de la trace 
    et extrait les valeurs et les noms des inputs avec le tag "only_input"

    Hypothèse : Un seul Scope Call par niveau de trace 
    """
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

main()