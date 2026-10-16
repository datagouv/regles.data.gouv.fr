<script setup lang="ts">
const { siteName } = useAppConfig()
</script>

<template>
  <a
    class="skip-link"
    href="#content"
  >
    Accéder au contenu
  </a>
  <header class="site-header">
    <NuxtLink
      class="site-name"
      to="/"
    >
      {{ siteName }}
    </NuxtLink>
  </header>
  <main
    id="content"
    class="site-main"
    tabindex="-1"
  >
    <slot />
  </main>
</template>

<style scoped>
.skip-link {
  position: absolute;
  top: var(--space-1);
  left: var(--space-1);
  padding: var(--space-1) var(--space-2);
  border: 1px solid var(--color-border);
  background: var(--color-background);
  transform: translateY(-200%);
}

.skip-link:focus {
  transform: none;
}

.site-header {
  padding: var(--space-2) max(var(--space-2), (100% - var(--width-page)) / 2);
  border-bottom: 1px solid var(--color-border);
}

.site-name {
  color: var(--color-text);
  font-size: var(--font-size-large);
  font-weight: 700;
  text-decoration: none;
}

.site-main {
  max-width: var(--width-page);
  margin: 0 auto;
  padding: var(--space-4) var(--space-2);
}
</style>
