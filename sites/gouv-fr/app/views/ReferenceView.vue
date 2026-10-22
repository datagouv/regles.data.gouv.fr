<script setup lang="ts">
import { routeTitles } from '~~/routes'
import { CATALOGUE_TITLE } from '#layers/web/catalogue/record'
import { routes } from '#layers/web/routes'

const title = routeTitles.reference

useHead({ title })

const breadcrumb = { links: [{ label: CATALOGUE_TITLE, to: routes.catalogue }], current: title }
</script>

<template>
  <UiPageHeader
    :title="title"
    :breadcrumb="breadcrumb"
  />
</template>
