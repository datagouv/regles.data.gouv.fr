import type { PublicodesRule } from '../src/index.ts'
// the model of betagouv/publicodes-entreprise-innovation at fc8e9a8 (MIT), compiled by publicodes compile
import innovation from './fixtures/entreprise-innovation.model.json' with { type: 'json' }

const INNOVATION = innovation as Record<string, unknown>

export const CIR_AMOUNT: PublicodesRule = {
  model: INNOVATION,
  outputs: ['cir . montant'],
  inputs: ['cir . depensesMetropole', 'cir . depensesDom'],
}

export const CIR_ELIGIBILITY: PublicodesRule = {
  model: INNOVATION,
  outputs: ['cir . eligibilite'],
  inputs: [
    'natureActivite . industrielle',
    'natureActivite . commerciale',
    'natureActivite . agricole',
    'natureActivite . artisanale',
    'regimeFiscal',
    'typeImposition',
    'typeDeRevenus',
  ],
}

// a model written for the types that the model of innovation lacks
export const TYPES_MODEL = {
  'début': { 'type': 'date', 'par défaut': '01/02/2024' },
  'nom': { 'type': 'texte', 'description': 'Nom d\'usage', 'par défaut': '\'x\'' },
  'motif': { type: 'texte' },
  'salarié': { 'question': 'Êtes-vous salarié ?', 'par défaut': 'non' },
  'taux': { 'une possibilité': { 'choix obligatoire': 'oui', 'possibilités': [5, 10] } },
  'prime': { 'applicable si': 'salarié', 'type': 'nombre', 'par défaut': 1 },
  'contrat': { 'une possibilité': ['CDI', 'CDD'] },
  'contrat . CDI': { titre: 'Contrat à durée indéterminée' },
  'contrat . CDD': { titre: 'Contrat à durée déterminée' },
  'fin': { valeur: 'début' },
  'bonus': { 'applicable si': 'salarié', 'valeur': 'taux' },
  'reste': { valeur: 'inconnu' },
  'inconnu': { type: 'nombre' },
}

export const TYPES: PublicodesRule = {
  model: TYPES_MODEL,
  outputs: ['fin', 'bonus'],
  inputs: ['début', 'nom', 'motif', 'salarié', 'taux', 'prime', 'contrat'],
}

// the situations of the cases of app/mocks/rule-tests.ts in ShallowRed/regles.data.gouv.fr-frontend-poc
export const EXECUTIONS: Array<[string, PublicodesRule, Record<string, unknown>, Record<string, unknown>]> = [
  ['the research credit of 100 000 €', CIR_AMOUNT, { cir__depensesMetropole: 100000, cir__depensesDom: 0 }, { cir__montant: 30000 }],
  ['the research credit of 150 M€', CIR_AMOUNT, { cir__depensesMetropole: 150000000, cir__depensesDom: 0 }, { cir__montant: 32500000 }],
  ['a craft company in BNC', CIR_ELIGIBILITY, {
    natureActivite__industrielle: false,
    natureActivite__commerciale: false,
    natureActivite__agricole: false,
    natureActivite__artisanale: true,
    regimeFiscal: 'reel-normal',
    typeImposition: 'ir',
    typeDeRevenus: 'bnc',
  }, { cir__eligibilite: false }],
  ['an industrial company taxed on its real profit', CIR_ELIGIBILITY, {
    natureActivite__industrielle: true,
    regimeFiscal: 'reel-normal',
    typeImposition: 'is',
    typeDeRevenus: 'bic',
  }, { cir__eligibilite: true }],
]
