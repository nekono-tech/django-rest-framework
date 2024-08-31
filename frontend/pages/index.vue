<template>
  <div>
    <button @click="fetch">Fetch data</button>
  </div>
</template>

<script setup>
const { $api } = useNuxtApp()
const { data, error } = useAsyncData('videos', async () => {
  const response = await $api('videos/')
  console.log(response)
  return response
})

if (error.value) {
  console.error(error.value)
}

const fetch = async () => {
  const response = await $api('videos/')
  console.log(response)
}
</script>
