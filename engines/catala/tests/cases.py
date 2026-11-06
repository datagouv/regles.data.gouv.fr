MODULES = "prestagri.generated"

# Inputs and outputs of the compiled scopes of Prest'Agri, recorded with the Catala adapter of datapi at commit a195ad6
EXECUTABLE = {
    f"{MODULES}.Quotient_familial:calcul_quotient_familial": (
        {
            "menage": {
                "beneficiaire_porteur_handicap": False,
                "garde_alternee": False,
                "parent_isole": True,
                "outre_mer": False,
                "membres_du_foyer": [{"revenu_fiscal_reference": 32000, "nombre_personnes": 3}],
            }
        },
        {
            "nombre_personnes_vivants_au_foyer": 3.0,
            "revenu_fiscal_reference": 32000.0,
            "criteres_applicables": [{"code": "Parent_isole", "payload": 1.0}],
            "nombre_unites": 4.0,
            "quotient_familial": 666.67,
        },
    ),
    f"{MODULES}.Aide_scolarite:calcul_quotient_familial_aide_scolarite": (
        {
            "foyer_fiscal_agent": {
                "beneficiaire_porteur_handicap": False,
                "garde_alternee": False,
                "parent_isole": True,
                "outre_mer": False,
                "membres_du_foyer": [{"revenu_fiscal_reference": 32000, "nombre_personnes": 3}],
            },
            "etudiants_fiscalement_independants": [{"revenu_fiscal_reference": 6000, "nombre_personnes": 1}],
        },
        {
            "revenu_fiscal_reference": 38000.0,
            "criteres_applicables": [{"code": "Parent_isole", "payload": 1.0}],
            "nombre_personnes_vivants_au_foyer": 4.0,
            "nombre_unites": 5.0,
            "quotient_familial": 633.33,
        },
    ),
    f"{MODULES}.Aide_scolarite:calcul_points_trajet": (
        {"trajet": {"distance_km": 120, "duree_minutes": 90}},
        {"nb_points": 4.0},
    ),
    f"{MODULES}.Aide_scolarite:calcul_points_aide_scolarite": (
        {
            "trajet_depuis_domicile_agent": {"distance_km": 120, "duree_minutes": 90},
            "trajet_depuis_domicile_etudiant": None,
            "montant_materiel_specifique": 300,
            "valeur_point": 10,
            "etudiant_en_filiere_post_bac": True,
        },
        {
            "criteres_applicables": [
                {"code": "C3_eloignement_agent", "payload": 4.0},
                {"code": "C4_materiel", "payload": 2.0},
                {"code": "C5_etudes_superieures", "payload": 1.0},
            ],
            "nb_points": 7.0,
        },
    ),
    f"{MODULES}.Aide_scolarite:calcul_aide_scolarite": (
        {
            "foyer_fiscal_agent": {
                "beneficiaire_porteur_handicap": False,
                "garde_alternee": False,
                "parent_isole": True,
                "outre_mer": False,
                "membres_du_foyer": [{"revenu_fiscal_reference": 32000, "nombre_personnes": 3}],
            },
            "etudiants_fiscalement_independants": [{"revenu_fiscal_reference": 6000, "nombre_personnes": 1}],
            "trajet_depuis_domicile_agent": {"distance_km": 120, "duree_minutes": 90},
            "trajet_depuis_domicile_etudiant": {"distance_km": 40, "duree_minutes": 35},
            "montant_materiel_specifique": 300,
            "etudiant_en_filiere_post_bac": True,
        },
        {
            "revenu_fiscal_reference": 38000.0,
            "nombre_personnes_vivants_au_foyer": 4.0,
            "nombre_unites": 5.0,
            "criteres_applicables_quotient_familial": [{"code": "Parent_isole", "payload": 1.0}],
            "quotient_familial": 633.33,
            "valeur_point": 100.0,
            "criteres_applicables": [
                {"code": "C2_domiciliation_separee", "payload": 2.0},
                {"code": "C3_eloignement_etudiant", "payload": 2.0},
                {"code": "C4_materiel", "payload": 2.0},
                {"code": "C5_etudes_superieures", "payload": 1.0},
            ],
            "nb_points": 7.0,
            "aide_scolarite": 700.0,
        },
    ),
}

# Scopes with a CatalaEnum input, which has no generic conversion from JSON
UNSUPPORTED = [f"{MODULES}.Aide_scolarite:retrait_critere_c2"]
