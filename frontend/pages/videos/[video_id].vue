<template>
  <div class="container mx-auto py-4 px-2 max-w-4xl">
    <div class="w-full">
      <div class="w-full h-full aspect-video">
        <iframe
          :src="`https://www.youtube.com/embed/${video.video_id}`"
          allowfullscreen
          class="w-full h-full"
        />
      </div>
    </div>
    <div class="mt-4">
      <h1 class="text-xl font-bold">{{ video.title }}</h1>
      <p class="text-sm text-gray-500">公開日時: {{ video.published_at }}</p>
    </div>
    <div class="mt-4">
      <pre class="text-gray-700">{{ video.description }}</pre>
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
