"""
Ce fichier a pour objectif de parser les fichiers en .catala_fr pour 
récupérer les inputs d'une fonction donnée, au format souhaité. 
Cela permettra à terme d'intégrer ces informations au cas-test automatiquement 
Approche : par regex. 
"""

import re


# --- Tokenizer (regex) 
TOKEN_RE = re.compile(r'''
    (?P<COMMENT>\#[^\n]*)                                  |
    (?P<NUM>\d+(?:[ ]\d{3})*(?:,\d+)?)                      |
    (?P<EURO>€)                                             |
    (?P<LBRACE>\{)                                          |
    (?P<RBRACE>\})                                          |
    (?P<LBRACK>\[)                                          |
    (?P<RBRACK>\])                                          |
    (?P<COLON>:)                                            |
    (?P<SEMI>;)                                             |
    (?P<DASHDASH>--)                                        |
    (?P<WORD>[A-Za-zÀ-ÖØ-öø-ÿ_][A-Za-zÀ-ÖØ-öø-ÿ0-9_'’]*)
''', re.VERBOSE)


class Token:
    __slots__ = ('type', 'value')

    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'{self.type}({self.value!r})'


def tokenize(text):
    tokens = []
    for m in TOKEN_RE.finditer(text):
        kind = m.lastgroup
        if kind == 'COMMENT':
            continue  # on ignore les commentaires "#..."
        tokens.append(Token(kind, m.group()))
    return tokens


# --- Extraction du bloc "avec { ... }" pour un test donné ---------------
def extract_input_block(catala_text, test_name):
    """
    Repere la definition du champ d'application `test_name` (celle qui
    contient "resultat de X avec {"), puis renvoie le contenu de ce
    "{...}" (bloc equilibre), sans les accolades englobantes.
    """
    header_re = re.compile(
        r"champ d'application\s+" + re.escape(test_name) + r"\s*:"
        r"(?!\s*\n\s*résultat)"          # exclut la ligne de "déclaration"
    )

    match = header_re.search(catala_text)
    if match is None:
        raise ValueError(f"Test '{test_name}' introuvable dans le fichier.")

    # A partir de la, on cherche le prochain "avec {"
    avec_match = re.search(r"avec\s*\{", catala_text[match.end():])
    if avec_match is None:
        raise ValueError(f"Bloc 'avec {{' introuvable pour '{test_name}'.")

    start = match.end() + avec_match.end()  # juste apres la '{' ouvrante

    # Equilibrage des accolades pour trouver la fermeture correspondante
    depth = 1
    i = start
    while depth > 0:
        if catala_text[i] == '{':
            depth += 1
        elif catala_text[i] == '}':
            depth -= 1
        i += 1
    end = i - 1  # position de la '}' fermante correspondante

    return catala_text[start:end]


# --- Parseur recursif sur la liste de tokens 
def _parse_number(tokens, i):
    tok = tokens[i]
    raw = tok.value.replace(' ', '')
    has_comma = ',' in raw
    i += 1
    is_euro = i < len(tokens) and tokens[i].type == 'EURO'
    if is_euro:
        i += 1

    if has_comma:
        value = float(raw.replace(',', '.'))
    elif is_euro:
        value = float(raw)
    else:
        value = int(raw)
    return value, i


def _parse_value(tokens, i):
    tok = tokens[i]

    if tok.type == 'NUM':
        return _parse_number(tokens, i)

    if tok.type == 'LBRACK':
        return _parse_list(tokens, i + 1)

    if tok.type == 'WORD':
        word = tok.value

        if word == 'vrai':
            return True, i + 1
        if word == 'faux':
            return False, i + 1
        if word == 'Absent':
            return None, i + 1

        if word == 'Présent':
            i += 1
            if tokens[i].type == 'WORD' and tokens[i].value == 'contenu':
                i += 1
            # nom du type (ex: Trajet), ignore, on veut juste le contenu
            if tokens[i].type == 'WORD':
                i += 1
            if tokens[i].type == 'LBRACE':
                obj, i = _parse_object(tokens, i + 1)
                return {'Présent': obj}, i
            # "Présent contenu <valeur simple>" (sans accolades)
            val, i = _parse_value(tokens, i)
            return {'Présent': val}, i

        # TypeName { ... }  -> ex: Trajet { -- distance_km: ... }
        if i + 1 < len(tokens) and tokens[i + 1].type == 'LBRACE':
            return _parse_object(tokens, i + 2)

        # NomDeCas contenu <valeur>  -> ex: C2_domiciliation_séparée contenu 2,0
        if i + 1 < len(tokens) and tokens[i + 1].type == 'WORD' and tokens[i + 1].value == 'contenu':
            val, i2 = _parse_value(tokens, i + 2)
            return {word: val}, i2

        # simple identifiant (enum sans valeur associee)
        return word, i + 1

    raise ValueError(f"Valeur inattendue: {tok}")


def _parse_list(tokens, i):
    items = []
    while tokens[i].type != 'RBRACK':
        val, i = _parse_value(tokens, i)
        items.append(val)
        if tokens[i].type == 'SEMI':
            i += 1
    return items, i + 1  # on saute le ']'


def _parse_object(tokens, i):
    obj = {}
    while tokens[i].type != 'RBRACE':
        if tokens[i].type == 'DASHDASH':
            i += 1
        key = tokens[i].value
        i += 1
        assert tokens[i].type == 'COLON', f"':' attendu apres la clef '{key}', trouve {tokens[i]}"
        i += 1
        val, i = _parse_value(tokens, i)
        obj[key] = val
        if i < len(tokens) and tokens[i].type == 'SEMI':
            i += 1
    return obj, i + 1  # on saute le '}'


# --- Fonction principale 
def extract_inputs(filepath, test_name):
    """
    Lit un fichier .catala_fr et renvoie un dictionnaire
    {nom_de_variable: valeur} correspondant aux entrees ("--")
    du test `test_name`.
    """
    with open(filepath, encoding='utf-8') as f:
        catala_text = f.read()

    block = extract_input_block(catala_text, test_name)
    tokens = tokenize(block)
    obj, _ = _parse_object(tokens + [Token('RBRACE', '}')], 0)
    return obj


if __name__ == '__main__':
    import sys
    import pprint

    filepath = sys.argv[1] if len(sys.argv) > 1 else 'tests_aide_scolarite.catala_fr'
    test_name = sys.argv[2] if len(sys.argv) > 2 else 'TestCalculPointsAideScolarite4'

    result = extract_inputs(filepath, test_name)
    pprint.pprint(result)