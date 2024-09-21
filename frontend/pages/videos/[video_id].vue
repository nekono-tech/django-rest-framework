<template>
  <UContainer class="max-w-4xl">
    <div class="aspect-w-16 aspect-h-9">
      <iframe
        class="w-full h-full"
        :src="`https://www.youtube.com/embed/${video.video_id}`"
        allowfullscreen
      ></iframe>
    </div>
  </UContainer>
  <UContainer class="pt-6">
    <UCard>
      <div class="mt-4">
        <h1 class="text-xl  font-bold text-slate-900 dark:text-slate-200">{{ video.title }}</h1>
        <p class="text-sm">公開日時: {{ video.published_at }}</p>
      </div>
      <div class="mt-4">
        <pre class="whitespace-pre-wrap break-words overflow-x-auto">{{ isFullDescription ? video.description: $utils.truncateText(video.description, 40) }}</pre>
        <UButton 
          @click="toggleDescription"
          :label="isFullDescription ? '閉じる' : 'もっと見る'" 
          :disabled="isLoading"
        />
      </div>
    </UCard>
  </UContainer>
</template>

<script setup>
const isFullDescription = ref(false);
const { $api } = useNuxtApp()
const route = useRoute()
const videoId = route.params.video_id

const { data: video } = await useAsyncData(`video-${videoId}`, () => {
  return $api.get(`videos/${videoId}`)
})

const toggleDescription = () => {
  isFullDescription.value = !isFullDescription.value;
};
</script>
