<template>
  <a
    :href="`/videos/${video.video_id}/`"
    class="flex flex-row hover:bg-gray-300 transition-colors duration-100"
  >
    <div class="flex flex-col w-1/2 p-2">
      <img
        :src="video.thumbnail_high_url"
        alt="Thumbnail"
        class="aspect-video object-cover"
      >
      <p class="text-xs text-gray-500 mt-1">公開日時: {{ video.published_at }}</p>
    </div>
    <div class="flex flex-col justify-start w-1/2 p-2">
      <h3 class="text-sm font-medium mb-1">{{ truncateText(video.title, 40) }}</h3>
      <p class="text-xs text-gray-700">{{ truncateText(video.description, 40) }}</p>
    </div>
  </a>
</template>

<script setup>
defineProps({
  video: Object
})

const { truncateText } = useTextUtils()
</script>
