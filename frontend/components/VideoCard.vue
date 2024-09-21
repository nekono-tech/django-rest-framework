<template>
  <a :href="`/videos/${video.video_id}/`" class="rounded-lg">
    <UCard 
      class="hover:bg-slate-300 dark:hover:bg-slate-700 transition-colors duration-300"
      :ui="{
        header: { padding: 'px-2 py-2 sm:px-4' },
        body: { padding: 'px-2 py-3 sm:p-4'}, 
        footer: { padding: 'px-2 py-2 sm:px-4' }
      }"
    >
      <template #header>
        <p class="font-semi-bold text-primary">{{ video.liver_name }}</p>
      </template>
      <div class="flex gap-2">
        <div class="w-1/2">
          <img :src="video.thumbnail_high_url" alt="video thumbnail">
        </div>
        <div class="flex flex-col w-1/2 gap-1">
          <h3 class="text-sm text-slate-900 dark:text-slate-200 font-medium break-words">{{ $utils.truncateText(video.title, 40) }}</h3>
          <p class="text-xs break-words">{{ $utils.truncateText(video.description, 40) }}</p>
        </div>
      </div>
      <template #footer>
        <p class="text-xs">公開日時: {{ video.published_at }}</p>
      </template>
    </UCard>
  </a>
</template>

<script setup>
defineProps({
  video: Object
})
</script>
