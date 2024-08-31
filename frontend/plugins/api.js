export default defineNuxtPlugin((nuxtApp) => {
  const api = $fetch.create({
    baseURL: import.meta.server ? 'http://backend:8888/api/' : '/api/',
    onRequest({ request, options, error }) {
        console.log('onRequest ----------------------------------------------------')
        console.log('request:', request)
        console.log('options:', options)
    },
    onResponse({ response, options, error }) {
        console.log('onResponse ----------------------------------------------------')
        console.log('response:', response)
        console.log('options:', options)
    },
  })

  return {
    provide: {
      api
    }
  }
})
