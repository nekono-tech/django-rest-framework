<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2">
    <VideoCard v-for="video in videos" :video="video"/>
  </div>
</template>

<script setup>
defineProps({
  videos: Object
})
</script>
