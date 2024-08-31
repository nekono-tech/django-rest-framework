<template>
  <div>
    <button @click="fetch">Fetch data</button>
  </div>
</template>

<script setup>
const url = import.meta.server ? 'http://backend:8888/api/videos/' : '/api/videos/'
const { data, error } = useAsyncData('videos', async () => {
  const response = await $fetch(url)
  console.log(response)
  return response
})

if (error.value) {
  console.error(error.value)
}

const fetch = async () => {
  const response = await $fetch(url)
  console.log(response)
}
</script>
