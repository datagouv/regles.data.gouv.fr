<script setup lang="ts">
const route = useRoute()
const { data: detail, error } = await useFetch(`/api/records/${route.params.identifier}`)
if (error.value || !detail.value) {
  throw createError({ ...error.value, fatal: true })
}

useHead({ title: detail.value.title })
</script>

<template>
  <article v-if="detail">
    <NuxtLink to="/">
      Catalogue des règles
    </NuxtLink>
    <h1>{{ detail.title }}</h1>
    <p>{{ detail.description }}</p>
    <dl>
      <dt>Version</dt>
      <dd>{{ detail.version }}</dd>
      <dt>Autorité compétente</dt>
      <dd>
        <a :href="detail.authority">{{ detail.authority }}</a>
      </dd>
      <template v-if="detail.validity">
        <dt>Validité</dt>
        <dd>{{ detail.validity }}</dd>
      </template>
      <template v-if="detail.source">
        <dt>Code source</dt>
        <dd>
          <a :href="detail.source.repository">{{ detail.source.repository }}</a><span v-if="detail.source.commit">, commit <code>{{ detail.source.commit }}</code></span>
        </dd>
      </template>
      <template v-if="detail.subjects.length > 0">
        <dt>Thématiques</dt>
        <dd>{{ detail.subjects.join(', ') }}</dd>
      </template>
      <template v-if="detail.updatedOn">
        <dt>Dernière mise à jour</dt>
        <dd>{{ detail.updatedOn }}</dd>
      </template>
    </dl>
  </article>
</template>
