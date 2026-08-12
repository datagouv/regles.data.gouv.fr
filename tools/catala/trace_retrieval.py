import json
import re
import os

def fetch_label(data: dict):
    return data.get("element").get("decl_pos").get("law_headings")[0]


def trace_explorer(trace : dict, resultat: dict = {}, path = None, level = -1, host_var = None) -> dict : 
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
            "outputs" : [],
            "scope_calls": []
        }
        path = []
        resultat["label"] = fetch_label(trace)
    #breakpoint()
    predicate_inp = lambda el: el.get("input") == "only_input"
    predicate_out = lambda el: el.get("output") == True
    # parcourt les élements de la trace - à chaque niveau.
    # check si c'est un dictionnaire ou pas et si ça contient element - sinon pas de value
    if "element" in trace:
        ele = trace["element"]
        kind = ele.get("kind")
        name = ele.get("name") or kind # donner le nom du element
        # nom du élément constitue le chemin - pour rémonter dans l'arbre / mieux comprendre 
        current_path = path + [name] 
        if predicate_inp(ele):
            #pos = trace.get("pos", {})
            # je voulais recup la position - mais je ne sais pas si c'est utile ?
            resultat['inputs'].append({
                "path": current_path,
                "value": trace.get("value"),
                #"file": pos.get("file"),
                #"start" : pos.get("start")
            }) # rajout dico qui contient le path, la valeur, et la position 
        if predicate_out(ele):  # <-- ajouté, même logique que pour input
            resultat['outputs'].append({
                    "path": current_path,
                    "value": trace.get("value"),
                })
        # niveau et scope_var "hôte" pour les scope_calls intermediaires -
        # on ne change host_var que quand on croise un vrai scope_var (pas un local_var)
        current_level = level
        current_host_var = host_var
        if kind == "scope_call":
            current_level = level + 1
            resultat['scope_calls'].append({
                "path": current_path,
                "scope_call": name,
                "scope_var": host_var,
                "level": current_level,
            })
            current_host_var = None  # on repart de zero a l'interieur du nouvel appel
        elif kind == "scope_var":
            current_host_var = name
        for child in trace.get("trace", []) : 
            #car il existe une trace au sein de chaque niveau -- > on peut naviguer avec ! 
            if 'element' in child:
                trace_explorer([child], resultat, current_path, current_level, current_host_var) #ok 
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

def resultat_to_json(resultat: dict, filepath: str = None) -> str:
    """
    Convertit le dictionnaire renvoyé par trace_explorer en une chaine JSON.
    Si un filepath est fourni, écrit également le résultat dans ce fichier.
    """
    texte_json = json.dumps(resultat, indent=2, ensure_ascii=False)
    if filepath is not None:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(texte_json)
    return texte_json
 
def _slugify(text: str) -> str:
    """ Transforme un texte en identifiant simple (minuscules, tirets). """
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")
 
def to_rule_test(resultat: dict, rule_id: str) -> dict:
    """
    Construit un cas-test au format RuleTest (cf rule-test.ts) à partir du
    dictionnaire renvoyé par trace_explorer.
 
    On se base sur le scope_call principal (level == 1 dans "scope_calls") :
    ses inputs et outputs directs (path juste sous le sien) alimentent
    "inputs" / "expected" / "expectedCriteria". Les appels intermediaires
    (level >= 2) ne sont pas repris ici (réservés à la partie fonction générale).
    """
    main_call = next((c for c in resultat.get("scope_calls", []) if c.get("level") == 1), None)
    if main_call is None:
        raise ValueError("Aucun scope_call de niveau 1 trouvé dans le résultat.")
    main_path = main_call["path"]
 
    inputs = {}
    for inp in resultat.get("inputs", []):
        if inp["path"][:-1] == main_path:
            inputs[inp["path"][-1]] = inp["value"]
 
    expected = None
    expected_criteria = []
    for out in resultat.get("outputs", []):
        if out["path"][:-1] != main_path:
            continue
        key = out["path"][-1]
        if key == "nb_points":
            expected = out["value"]
        elif key == "critères_applicables#études_supérieures":
            for item in out["value"]:
                if isinstance(item, dict):
                    for name, value in item.items():
                        expected_criteria.append({"name": name, "value": value})
        else:
            expected = out["value"]  # <-- fonctionne pour "nb_points", "aide_scolarite", etc.
 
    label = resultat.get("label")
    case_match = re.search(r"Cas N°(\d+)", label)
    case_id = case_match.group(1) if case_match else _slugify(label)
 
    return {
        "id": f"{rule_id}-cas-{case_id}",
        "ruleId": "prestagri",
        "label": label,
        "scenario": label,
        "inputs": inputs,
        "expected": expected,
        "expectedUnit": "points",
        "expectedCriteria": expected_criteria,
        "source": "administration",
        "status": "valide",
        "validatedBy": "TO BE VALIDATED",
        "engineVersion": "catala 1.2.1",
        "nativeFormat": "catala-assert",
        "nativeRef": f"aide_scolarite.catala_fr#{main_call['scope_call']}",
        "tags": [],
    }

def _is_valid_ts_key(key: str) -> bool:
    return re.match(r"^[A-Za-z_$][A-Za-z0-9_$]*$", key) is not None
 
def _ts_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace("'", "\\'")
    return f"'{escaped}'"
 
def _ts_key(key: str) -> str:
    return key if _is_valid_ts_key(key) else _ts_string(key)
 
def _to_ts_literal(value, indent: int = 0) -> str:
    """ Convertit une valeur Python (dict/list/str/bool/None/nombre) en littéral TS. """
    pad = "  " * indent
    pad_in = "  " * (indent + 1)
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return _ts_string(value)
    if isinstance(value, list):
        if not value:
            return "[]"
        items = ",\n".join(f"{pad_in}{_to_ts_literal(v, indent + 1)}" for v in value)
        return "[\n" + items + f",\n{pad}]"
    if isinstance(value, dict):
        if not value:
            return "{}"
        items = ",\n".join(f"{pad_in}{_ts_key(k)}: {_to_ts_literal(v, indent + 1)}" for k, v in value.items())
        return "{\n" + items + f",\n{pad}}}"
    raise TypeError(f"Type non gere pour la conversion TS: {type(value)}")
 
def write_rule_tests_ts(rule_tests: list, filepath: str, const_name: str = "ruleTestsCatala") -> None:
    """
    Ecrit une liste de cas-tests (format RuleTest, cf rule-test.ts) dans un
    fichier .ts, au même format que rule-tests.ts.
    """
    items = ",\n".join(f"  {_to_ts_literal(rt, 1)}" for rt in rule_tests)
    contenu = (
        "import type { RuleTest } from '~/types'\n\n"
        f"export const {const_name}: RuleTest[] = [\n{items},\n]\n"
    )
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(contenu)
 
 

def main():
    
    folder = "trace_files"
    rule_tests = []
    for filename in sorted(os.listdir(folder)):
        if not filename.endswith(".json"):
            continue
        with open(os.path.join(folder, filename)) as file:
            trace = json.load(file)
        resultat = trace_explorer(trace)
        rule_tests.append(to_rule_test(resultat, "aide-scolarite"))
        if filename =="test-aide-full.json" : 
            print(resultat)
 
    write_rule_tests_ts(rule_tests, "tests-catala.ts")
    print(f"{len(rule_tests)} cas-tests écrits dans tests-catala.ts")
 

 
if __name__ == "__main__":
    main()
    # matcher sur le predicat (apparemment la meilleure façon de faire ? )
    #matches = []
    #matches.extend(trace_explorer(trace, path = None))
    #breakpoint()
    #print(matches)




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