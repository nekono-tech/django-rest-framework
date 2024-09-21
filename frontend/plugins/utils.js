export default defineNuxtPlugin((nuxtApp) => {
  const truncateText = (text, maxLength) => {
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
  }

  nuxtApp.provide('utils', {
    truncateText
  })
})
