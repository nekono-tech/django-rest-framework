<template>
  <div class="container mx-auto py-4 px-2">
    <div class="video-container">
      <iframe
        :src="`https://www.youtube.com/embed/${video.video_id}`"
        allowfullscreen
        class="w-full h-full"
      ></iframe>
    </div>
    <div class="mb-4">
      <h1 class="text-xl font-bold">{{ video.title }}</h1>
      <p class="text-sm text-gray-500">公開日時: {{ video.published_at }}</p>
    </div>
    <div class="mt-4">
      <p class="text-gray-700">{{ video.description }}</p>
    </div>
  </div>
</template>

<script setup>
const { $api } = useNuxtApp()
const route = useRoute()

const videoId = route.params.video_id

const { data: video } = await useAsyncData(`video-${videoId}`, () => {
  return $api.get(`videos/${videoId}`)
})
</script>

<style scoped>
.video-container {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%;
  height: 0;
}
.video-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
