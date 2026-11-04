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
    <UiPageHeader
      :title="detail.title"
      :lead="detail.description"
      :breadcrumb="detail.breadcrumb"
    />
    <UiPageBody>
      <dl>
        <dt>Version</dt>
        <dd>{{ detail.version }}</dd>
        <dt>Autorité compétente</dt>
        <dd>
          <a v-if="detail.authority.href" :href="detail.authority.href">{{ detail.authority.label }}</a>
          <span v-else>{{ detail.authority.label }}</span>
        </dd>
        <template v-if="detail.validity">
          <dt>Validité</dt>
          <dd>{{ detail.validity }}</dd>
        </template>
        <template v-if="detail.source">
          <dt>Code source</dt>
          <dd>
            <a v-if="detail.source.repository.href" :href="detail.source.repository.href">{{ detail.source.repository.label }}</a>
            <span v-else>{{ detail.source.repository.label }}</span><span v-if="detail.source.commit">, commit <code>{{ detail.source.commit }}</code></span>
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
    </UiPageBody>
  </article>
</template>
