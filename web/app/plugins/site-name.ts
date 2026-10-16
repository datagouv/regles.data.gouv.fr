export default defineNuxtPlugin(() => {
  const { siteName } = useAppConfig()

  useHead({
    titleTemplate: title => title
      ? `${title} - ${siteName}`
      : siteName,
  })
})
