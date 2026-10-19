<script setup lang="ts">
import cityHall from '@gouvfr/dsfr/dist/artwork/pictograms/buildings/city-hall.svg?url'
import contract from '@gouvfr/dsfr/dist/artwork/pictograms/document/contract.svg?url'
import justice from '@gouvfr/dsfr/dist/artwork/pictograms/institutions/justice.svg?url'
import { DsfrCallout } from '@gouvminint/vue-dsfr'
import { routeTitles } from '~~/routes'
import { CATALOGUE_TITLE } from '#layers/web/catalogue/record'
import { routes } from '#layers/web/routes'

const title = routeTitles.reference

useHead({ title })

const breadcrumb = { links: [{ label: CATALOGUE_TITLE, to: routes.catalogue }], current: title }

const steps = [
  { label: 'Vous décrivez la règle', description: 'Intitulé, base légale, organisme producteur, domaine. Le minimum pour la rendre découvrable.' },
  { label: 'Vous reliez les textes', description: 'Les articles de loi, décrets ou conventions qui la fondent, liés à leur source Légifrance.' },
  { label: 'Vous publiez ce que vous pouvez', description: 'Du simple référencement à la modélisation exécutable : chaque niveau apporte sa valeur, à votre rythme.' },
  { label: 'La règle est qualifiée', description: 'Sa fiche signale ce qu\'elle offre (découverte, traçabilité, calcul) selon les preuves apportées.' },
]

const levels = [
  { tag: 'Référencer', title: 'La règle existe et se trouve', body: 'Métadonnées et bases légales. La règle devient découvrable dans le catalogue et reliée à ses textes.', requirement: 'Accessible à toute administration, sans prérequis technique.' },
  { tag: 'Documenter', title: 'La règle s\'explique', body: 'La logique métier est décrite, éventuellement accompagnée de cas de test. La fiche gagne en traçabilité.', requirement: 'Demande de formaliser le barème ou les conditions, sans modèle exécutable obligatoire.' },
  { tag: 'Exécuter', title: 'La règle se calcule', body: 'La modélisation (Publicodes, OpenFisca, Catala ou moteur propriétaire) permet un calcul, exposé via API ou simulateur.', requirement: 'Suppose un moteur de calcul et une équipe pour le maintenir.' },
]

const ownership = [
  { icon: 'fr-icon-lock-line', title: 'Vous restez responsable', body: 'Le contenu de la règle, son exactitude et sa publication relèvent de votre administration. Le catalogue expose la règle telle que vous la décrivez.' },
  { icon: 'fr-icon-git-branch-line', title: 'Vous gardez la main', body: 'Vous publiez les versions à votre cadence, à chaque évolution réglementaire. L\'historique reste le vôtre.' },
  { icon: 'fr-icon-eye-line', title: 'Le catalogue rend visible', body: 'Découvrabilité, traçabilité jusqu\'au texte et réutilisation par d\'autres services : c\'est ce que le référencement ajoute.' },
]

const audiences = [
  { pictogram: cityHall, title: 'Administrations d\'État', body: 'CNAF, DGFiP, France Travail… Référencez les prestations et impôts que vous calculez pour les rendre traçables et réutilisables.', examples: ['prestations sociales', 'fiscalité', 'allocations'] },
  { pictogram: justice, title: 'Collectivités territoriales', body: 'Régions, départements, métropoles, communes : vos aides locales gagnent en visibilité et en lisibilité aux côtés des dispositifs nationaux.', examples: ['tarifs solidaires', 'aides à la mobilité', 'subventions'] },
  { pictogram: contract, title: 'Opérateurs et caisses', body: 'Organismes de sécurité sociale et opérateurs publics : référencez vos règles une fois, et chaque service réutilise la même version.', examples: ['caisses de retraite', 'opérateurs', 'agences'] },
]
</script>

<template>
  <UiPageHeader
    title="Référencez vos règles, gardez-en la maîtrise"
    lead="Votre administration applique des règles de calcul. Les référencer dans le catalogue les rend découvrables, traçables et réutilisables par les autres services publics."
    :breadcrumb="breadcrumb"
  />
  <UiPageBody>
    <section aria-labelledby="process">
      <h2 id="process">
        Comment se passe un référencement
      </h2>
      <p class="fr-text--lg">
        Le référencement commence par une fiche minimale, enrichie ensuite selon ce que vous pouvez publier.
      </p>
      <ol class="fr-raw-list fr-grid-row fr-grid-row--gutters">
        <li
          v-for="(step, index) in steps"
          :key="step.label"
          class="fr-col-12 fr-col-sm-6 fr-col-lg-3"
        >
          <div class="block fr-p-3w">
            <p
              class="step-number fr-mb-2w"
              aria-hidden="true"
            >
              {{ index + 1 }}
            </p>
            <h3 class="fr-h6 fr-mb-1w">
              {{ step.label }}
            </h3>
            <p class="fr-text--sm fr-mb-0">
              {{ step.description }}
            </p>
          </div>
        </li>
      </ol>
    </section>

    <section
      aria-labelledby="levels"
      class="fr-mt-8w"
    >
      <h2 id="levels">
        Jusqu'où vous voulez aller
      </h2>
      <p class="fr-text--lg">
        Une règle apporte déjà de la valeur dès qu'elle est référencée. Documenter puis rendre exécutable sont des étapes facultatives, franchies quand vous êtes prêts.
      </p>
      <ol class="fr-raw-list fr-grid-row fr-grid-row--gutters">
        <li
          v-for="level in levels"
          :key="level.tag"
          class="fr-col-12 fr-col-md-4"
        >
          <div class="block fr-p-3w">
            <p class="fr-badge fr-badge--sm fr-badge--blue-cumulus fr-mb-2w">
              {{ level.tag }}
            </p>
            <h3 class="fr-h6 fr-mb-1w">
              {{ level.title }}
            </h3>
            <p class="fr-text--sm">
              {{ level.body }}
            </p>
            <p class="fr-text--xs fr-mb-0 requirement">
              {{ level.requirement }}
            </p>
          </div>
        </li>
      </ol>
    </section>

    <section
      aria-labelledby="ownership"
      class="fr-mt-8w"
    >
      <h2 id="ownership">
        Ce que vous gardez, ce que le catalogue ajoute
      </h2>
      <p class="fr-text--lg">
        L'administration productrice reste maîtresse de sa règle ; le catalogue l'expose.
      </p>
      <ul class="fr-raw-list fr-grid-row fr-grid-row--gutters">
        <li
          v-for="item in ownership"
          :key="item.title"
          class="fr-col-12 fr-col-md-4"
        >
          <div class="block fr-p-3w">
            <span
              :class="item.icon"
              class="fr-icon--lg icon"
              aria-hidden="true"
            />
            <h3 class="fr-h6 fr-mt-2w fr-mb-1w">
              {{ item.title }}
            </h3>
            <p class="fr-text--sm fr-mb-0">
              {{ item.body }}
            </p>
          </div>
        </li>
      </ul>
    </section>

    <section
      aria-labelledby="audiences"
      class="fr-mt-8w"
    >
      <h2 id="audiences">
        Qui peut référencer
      </h2>
      <p class="fr-text--lg">
        Toute administration ou organisme qui produit des règles de calcul opposables aux usagers peut les référencer.
      </p>
      <ul class="fr-raw-list fr-grid-row fr-grid-row--gutters">
        <li
          v-for="audience in audiences"
          :key="audience.title"
          class="fr-col-12 fr-col-md-4"
        >
          <div class="block fr-p-3w">
            <img
              :src="audience.pictogram"
              alt=""
              width="64"
              height="64"
            >
            <h3 class="fr-h6 fr-mt-2w fr-mb-1w">
              {{ audience.title }}
            </h3>
            <p class="fr-text--sm">
              {{ audience.body }}
            </p>
            <ul class="fr-tags-group">
              <li
                v-for="example in audience.examples"
                :key="example"
              >
                <p class="fr-tag fr-tag--sm">
                  {{ example }}
                </p>
              </li>
            </ul>
          </div>
        </li>
      </ul>
      <p class="fr-text--sm fr-mt-3w">
        L'équipe du catalogue vous accompagne pour le référencement : elle cadre avec vous le périmètre, la base légale et le niveau de publication visé.
      </p>
    </section>

    <DsfrCallout
      class="fr-mt-8w"
      title="Vous appliquez des règles de calcul ?"
      title-tag="h2"
      content="Parlons de leur référencement : l'équipe du catalogue vous accompagne, de la fiche minimale à la règle exécutable."
    >
      <ul class="fr-btns-group fr-btns-group--inline-md fr-mt-3w fr-mb-0">
        <li>
          <a
            class="fr-btn"
            href="https://github.com/datagouv/regles.data.gouv.fr/issues/new"
          >
            Proposer une règle
          </a>
        </li>
        <li>
          <NuxtLink
            class="fr-btn fr-btn--secondary"
            :to="routes.catalogue"
          >
            Voir les règles déjà référencées
          </NuxtLink>
        </li>
      </ul>
    </DsfrCallout>
  </UiPageBody>
</template>

<style scoped>
.block {
  height: 100%;
  border: 1px solid var(--border-default-grey);
}

.step-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50%;
  background: var(--background-action-high-blue-france);
  color: var(--text-inverted-blue-france);
  font-weight: 700;
}

.requirement {
  color: var(--text-mention-grey);
}

.icon {
  color: var(--text-action-high-blue-france);
}
</style>
