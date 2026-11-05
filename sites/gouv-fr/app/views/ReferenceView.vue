<script setup lang="ts">
import { routeTitles } from '#layers/gouv-fr/routes'
import { catalogueBreadcrumb } from '#layers/web/catalogue/record'

const title = routeTitles.reference

useHead({ title })

const breadcrumb = catalogueBreadcrumb(title)
</script>

<template>
  <UiPageHeader
    :title="title"
    :breadcrumb="breadcrumb"
  />
</template>
