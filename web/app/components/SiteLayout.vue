<script setup lang="ts">
useHead({
  titleTemplate: title => title
    ? `${title} - regles.data.gouv.fr`
    : 'regles.data.gouv.fr',
})
</script>

<template>
  <header>
    <NuxtLink to="/">
      regles.data.gouv.fr
    </NuxtLink>
  </header>
  <main>
    <slot />
  </main>
</template>
