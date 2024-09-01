// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
  plugins: [
    '~/plugins/api.js',
  ],
  modules: [
    '@nuxtjs/tailwindcss',
    '@nuxt/eslint'
  ],
  tailwindcss: {
    cssPath: '~/assets/css/tailwind.css',
    exposeConfig: false,
    injectPosition: 0,
    viewer: false,
  },
})
