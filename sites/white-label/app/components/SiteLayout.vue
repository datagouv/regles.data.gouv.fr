<script setup lang="ts">
const { siteName } = useAppConfig()
</script>

<template>
  <header>
    <NuxtLink to="/">
      {{ siteName }}
    </NuxtLink>
  </header>
  <main>
    <slot />
  </main>
</template>
