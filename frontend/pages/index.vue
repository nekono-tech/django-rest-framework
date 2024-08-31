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

    <pagenation
      :totalPages="totalPages"
      :currentPage="currentPage"
      :hasNext="Boolean(videos.next)"
      :hasPrevious="Boolean(videos.previous)"
      @nextPage="nextPage"
      @prevPage="prevPage"
      @goToPage="goToPage"
    />
  </div>
</template>

<script setup>
const { $api } = useNuxtApp()
const router = useRouter()
const route = useRoute()

const videos = ref({
  results: [],
  next: null,
  previous: null,
  count: 0
})

const currentPage = ref(parseInt(route.query.page) || 1)
const pageSize = ref(parseInt(route.query.page_size) || 16)

const totalPages = computed(() => Math.ceil(videos.value.count / pageSize.value))

const fetchVideos = async (page = 1) => {
  videos.value = await $api.get('videos/', {
    params: {
      page: page,
      page_size: pageSize.value
    }
  })
}

onBeforeMount(() => {
  fetchVideos(currentPage.value)
})

watch(
  () => route.fullPath,  // ルートが変更されるたびに実行
  () => { // 実行される内容
    currentPage.value = parseInt(route.query.page) || 1
    fetchVideos(currentPage.value)
  }
)

const nextPage = async () => {
  if (videos.value.next) {
    currentPage.value++
    router.push({
      query: {
        ...route.query,
        page: currentPage.value,
        page_size: pageSize.value
      }
    })
  }
}

const prevPage = async () => {
  if (videos.value.previous) {
    currentPage.value--
    router.push({
      query: {
        ...route.query,
        page: currentPage.value,
        page_size: pageSize.value
      }
    })
  }
}

const goToPage = async (page) => {
  currentPage.value = page
  router.push({
    query: {
      ...route.query,
      page: currentPage.value,
      page_size: pageSize.value
    }
  })
}

const truncateText = (text, maxLength) => {
  if (text.length > maxLength) {
    return text.substring(0, maxLength) + '...'
  }
  return text
}
</script>
