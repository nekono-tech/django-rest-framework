<template>
  <a
    :href="`/videos/${video.video_id}/`"
    class="flex flex-row bg-white overflow-hidden hover:bg-gray-300 transition-colors duration-100"
  >
    <div class="w-1/2 flex flex-col p-2">
      <img
        :src="video.thumbnail_high_url"
        alt="Thumbnail"
        class="w-full aspect-video object-cover"
      >
      <p class="text-xs text-gray-500 mt-1">公開日時: {{ video.published_at }}</p>
    </div>
    <div class="flex flex-col justify-start p-2 w-1/2">
      <h3 class="text-sm font-medium mb-1">{{ truncateText(video.title, 60) }}</h3>
      <p class="text-gray-700 text-xs">{{ truncateText(video.description, 60) }}</p>
    </div>
  </a>
</template>

<script setup>
defineProps({
  video: Object
})

const { truncateText } = useTextUtils()
</script>
