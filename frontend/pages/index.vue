<template>
  <div class="container mx-auto py-2 px-1">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2">
      <div v-for="video in videos.results" :key="video.video_id" class="flex flex-row bg-white overflow-hidden">
        <div class="w-1/2 flex flex-col p-2">
          <img
            :src="video.thumbnail_high_url"
            alt="Thumbnail"
            class="w-full aspect-w-16 aspect-h-9 object-cover"
          />
          <p class="text-xs text-gray-500 mt-1">投稿日時: {{ video.published_at }}</p>
        </div>
        <div class="flex flex-col justify-start p-2 w-1/2">
          <h3 class="text-sm font-medium mb-1">{{ video.title }}</h3>
          <client-only>
            <p class="text-gray-700 text-xs">{{ truncateText(video.description, 60) }}</p>
          </client-only>
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
