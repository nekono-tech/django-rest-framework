<template>
  <div class="container mx-auto py-8 px-4">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div v-for="video in videos" :key="video.video_id" class="flex flex-col md:flex-row bg-white shadow-md rounded-lg overflow-hidden">
        <div class="md:w-1/2 p-4">
          <img
            :src="video.thumbnail_high_url"
            alt="Thumbnail"
            class="w-full aspect-w-16 aspect-h-9 object-cover"
          />
          <p class="text-sm text-gray-500 mt-2 px-4 py-2">投稿日時: {{ video.published_at }}</p>
        </div>
        <div class="md:w-1/2 p-4">
          <h3 class="text-lg font-bold mb-2">{{ video.title }}</h3>
          <p class="text-gray-700 text-sm">{{ truncateText(video.description, 100) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const { $api } = useNuxtApp()
const { data: videos } = await useAsyncData('videos', () =>
    $api.get('videos/')
)

const truncateText = (text, maxLength) => {
  if (text.length > maxLength) {
    return text.substring(0, maxLength) + '...'
  }
  return text
}
</script>
