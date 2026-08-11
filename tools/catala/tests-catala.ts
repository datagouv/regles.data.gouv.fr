import type { RuleTest } from '~/types'

export const ruleTestsCatala: RuleTest[] = [
  {
    id: 'aide-scolarite-cas-4',
    ruleId: 'aide-scolarite',
    label: 'Cas N°4 : logement separe, l\'adresse des parents est moins avantageuse',
    scenario: 'Cas N°4 : logement separe, l\'adresse des parents est moins avantageuse',
    inputs: {
      trajet_depuis_domicile_agent: {
        distance_km: '60',
        'durée_minutes': '50',
      },
      'trajet_depuis_domicile_étudiant': {
        'Présent': {
          distance_km: '32',
          'durée_minutes': '20',
        },
      },
      'montant_matériel_spécifique': '0.00',
      valeur_point: '10.00',
      'étudiant_en_filière_post_bac': false,
    },
    expected: '4',
    expectedUnit: 'points',
    expectedCriteria: [
      {
        name: 'C2_domiciliation_séparée',
        value: '2',
      },
      {
        name: 'C3_éloignement_étudiant',
        value: '2',
      },
    ],
    source: 'administration',
    status: 'valide',
    validatedBy: 'Trace Catala (interpréteur, calcul réel)',
    engineVersion: 'catala (non renseigné)',
    nativeFormat: 'catala-assert',
    nativeRef: 'aide_scolarite.catala_fr#CalculPointsAideScolarite',
    tags: [],
  },
]
