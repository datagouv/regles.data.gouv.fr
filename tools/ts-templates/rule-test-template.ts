/**
 * Cas de test attaché à une règle - l'ENVELOPPE de confiance.
 *
 * Doctrine (ontologie localisée) : le catalogue ne définit pas de format de situation
 * universel - décrire une situation exigerait les entités et périodes du moteur, donc son
 * ontologie. Chaque règle publie ses tests dans le format natif de son moteur, et le
 * catalogue norme l'ENVELOPPE sociale du test : intention, provenance, validateur, statut,
 * période législative et version du moteur.
 *
 * Format aligné sur `shared-test-cases` d'aides-simplifiées (branche `tests-personas` :
 * `shared-test-cases/schema.json`) : source de vérité unique, non-régression CI, snapshots
 * datés par période et version de moteur. C'est le versant « cas de test comme preuve » du
 * catalogue - pas un simulateur : on montre la preuve validée, on ne fait pas saisir un
 * usager pour lui rendre un droit.
 */

/** Valeur scalaire pouvant être passée en entrée d'une règle. */
export type RuleTestValue = string | number | boolean | null

/** Format natif du cas de test, dans l'espace de noms du moteur. */
export type RuleTestNativeFormat
  = | 'openfisca-yaml'
    | 'publicodes-yaml'
    | 'catala-assert'
    | 'pytest'
    | 'autre'

export interface RuleTest {
  id: string
  /** Identifiant de la règle parente */
  ruleId: string
  /** Libellé court du cas (par exemple « Lycéen 17 ans, premier achat ») */
  label: string
  /** Intention du test en langage naturel (l'hypothèse testée). */
  scenario: string
  /**
   * Entrées clés-valeurs à visée pédagogique (affichage). Optionnelles : la référence
   * qui fait foi est le test natif (`nativeRef`), pas cette projection plate.
   */
  inputs?: Record<string, RuleTestValue>
  /** Résultat attendu affiché (montant, booléen, statut). */
  expected?: RuleTestValue
  /** Unité du résultat attendu si numérique (par exemple `EUR`, `mois`) */
  expectedUnit?: string
  /**
   * Détail du résultat quand `expected` est un total obtenu par accumulation
   * de plusieurs critères (par exemple un barème à points). `expected` reste
   * le résumé affiché ; `expectedCriteria` porte le détail (quel critère a
   * rapporté quoi), à visée pédagogique — au même titre que `inputs`, ce
   * n'est pas la référence qui fait foi (`nativeRef`).
   */
  expectedCriteria?: { name: string, value: RuleTestValue }[]
  /** Provenance du cas. */
  source: 'administration' | 'communaute' | 'jurisprudence' | 'circulaire' | 'cas-reel-anonymise'
  /** Statut de validation du cas */
  status: 'valide' | 'en_revue' | 'echec'
  /** Qui a validé ce cas (administration compétente, CI du dépôt source...). */
  validatedBy?: string
  /** Date de validation (ISO 8601). */
  validatedAt?: string
  /** Ancre légale visée par le cas (version du texte). */
  legalAnchor?: string
  /** Tolérance d'écart acceptée sur le résultat, si numérique. */
  tolerance?: string
  /** Format natif du test dans l'espace de noms du moteur. */
  nativeFormat?: RuleTestNativeFormat
  /** Lien vers le test natif qui fait foi (dépôt source, idéalement pinné). */
  nativeRef?: string
  /** Période législative visée (YYYY-MM) : l'état du droit à une date donnée. */
  period?: string
  /** Version du moteur ayant produit le résultat attendu (ex. `france-169.15.0`, `prestagri 0.1.0`). */
  engineVersion?: string
  /** Référence du dossier réel anonymisé, si le cas en dérive (provenance forte). */
  realCaseSource?: string
  /** Tags de catégorisation du cas. */
  tags?: string[]
  /** Note ou contexte additionnel. */
  notes?: string
}