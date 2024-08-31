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

    <div class="flex justify-center mt-4 space-x-2">
      <button @click="prevPage" :disabled="!videos.previous" class="px-4 py-2 bg-gray-300 rounded">前へ</button>

      <button
        v-for="page in paginationPages"
        :key="page"
        @click="goToPage(page)"
        :disabled="page === '...'"
        :class="['px-4 py-2 rounded', { 'bg-blue-500 text-white': currentPage === page, 'bg-gray-300': currentPage !== page }]"
        v-if="page !== '...'"
      >
        {{ page }}
      </button>
      <span v-else class="px-2">...</span>

      <button @click="nextPage" :disabled="!videos.next" class="px-4 py-2 bg-gray-300 rounded">次へ</button>
    </div>
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

const paginationPages = computed(() => {
  const pages = []
  const maxPagesToShow = 7
  const startPage = Math.max(1, currentPage.value - 2)
  const endPage = Math.min(totalPages.value, currentPage.value + 2)

  if (totalPages.value <= maxPagesToShow) {
    for (let i = 1; i <= totalPages.value; i++) {
      pages.push(i)
    }
  } else {
    if (currentPage.value <= 3) {
      for (let i = 1; i <= 4; i++) {
        pages.push(i)
      }
      pages.push('...')
      pages.push(totalPages.value)
    } else if (currentPage.value > 3 && currentPage.value < totalPages.value - 2) {
      pages.push(1)
      pages.push('...')
      for (let i = currentPage.value - 1; i <= currentPage.value + 1; i++) {
        pages.push(i)
      }
      pages.push('...')
      pages.push(totalPages.value)
    } else {
      pages.push(1)
      pages.push('...')
      for (let i = totalPages.value - 3; i <= totalPages.value; i++) {
        pages.push(i)
      }
    }
  }
  return pages
})

const fetchVideos = async (page = 1) => {
  videos.value = await $api.get(`videos/?page=${page}&page_size=${pageSize.value}`)
}
await fetchVideos(currentPage.value)

watch(() => route.query.page, (newPage) => {
  if (newPage) {
    currentPage.value = parseInt(newPage)
    fetchVideos(currentPage.value)
  }
})

const nextPage = async () => {
  if (videos.value.next) {
    currentPage.value++
    router.push({query: {...route.query, page: currentPage.value}})  // URLを更新
    await fetchVideos(currentPage.value)
  }
}

const prevPage = async () => {
  if (videos.value.previous) {
    currentPage.value--
    router.push({query: {...route.query, page: currentPage.value}})  // URLを更新
    await fetchVideos(currentPage.value)
  }
}

const goToPage = async (page) => {
  currentPage.value = page
  router.push({query: {...route.query, page: currentPage.value}})
  await fetchVideos(currentPage.value)
}

const truncateText = (text, maxLength) => {
  if (text.length > maxLength) {
    return text.substring(0, maxLength) + '...'
  }
  return text
}
</script>
