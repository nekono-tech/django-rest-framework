<template>
  <div class="container mx-auto py-2 px-1">

    <!-- Search -->
    <div class="mb-4 mt-4 flex flex-col items-center space-y-4">
      <div class="flex w-full max-w-xl">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="動画を検索..."
          class="flex-grow p-2 border border-gray-300 rounded-l"
        >
        <button
          @click="searchVideos"
          class="px-6 bg-blue-500 text-white rounded-r"
        >
          検索
        </button>
      </div>

      <!-- Filters -->
      <button
        @click="toggleFilters"
        class="w-full max-w-xl text-left p-2 border border-gray-300 rounded-md bg-gray-100 hover:bg-gray-200"
      >
        {{ showFilters ? 'フィルターを隠す' : 'フィルターを表示' }}
      </button>

      <div v-if="showFilters" class="w-full max-w-xl p-4 border border-t-0 border-gray-300 rounded-b-md transition-all duration-300 ease-in-out">
        <div class="flex flex-col sm:flex-row sm:space-x-4">
          
          <div class="flex flex-col mb-4 sm:mb-0">
            <label for="sortOrder" class="text-sm font-medium text-gray-700 mb-1">日付で並び替え</label>
            <select
              id="sortOrder"
              v-model="sortOrder"
              class="p-2 border border-gray-300 rounded"
              @change="sortVideos"
            >
              <option value="desc">公開日時が新しい順</option>
              <option value="asc">公開日時が古い順</option>
            </select>
          </div>

          <div class="flex flex-col">
            <label for="liverSelect" class="text-sm font-medium text-gray-700 mb-1">ライバーで絞り込み</label>
            <select
              id="liverSelect"
              v-model="selectedLiverId"
              class="p-2 border border-gray-300 rounded"
              @change="filterByLiver"
            >
              <option value="">すべてのライバー</option>
              <option v-for="liver in livers" :key="liver.id" :value="liver.id">
                {{ liver.name }}
              </option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Videos -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2">
      <a
        v-for="video in videos.results"
        :key="video.video_id"
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
          <client-only>
            <p class="text-gray-700 text-xs">{{ truncateText(video.description, 60) }}</p>
          </client-only>
        </div>
      </a>
    </div>

    <pagenation
      :total-pages="totalPages"
      :current-page="currentPage"
      :has-next="Boolean(videos.next)"
      :has-previous="Boolean(videos.previous)"
      @next-page="nextPage"
      @prev-page="prevPage"
      @go-to-page="goToPage"
    />
  </div>
</template>

<script setup>
const { $api } = useNuxtApp()
const route = useRoute()

const livers = ref([])
const fetchLivers = async () => {
  livers.value = await $api.get('livers/')
}

const videos = ref({
  results: [],
  next: null,
  previous: null,
  count: 0
})

const currentPage = ref(parseInt(route.query.page) || 1)
const pageSize = ref(parseInt(route.query.page_size) || 16)
const searchQuery = ref(route.query.search || '')
const sortOrder = ref(route.query.order || 'desc')
const selectedLiverId = ref(route.query.liver || '')

const totalPages = computed(() => Math.ceil(videos.value.count / pageSize.value))

const showFilters = ref(false)
const toggleFilters = () => {
  showFilters.value = !showFilters.value
}

const getQueryParams = (page) => {
  return {
    page: page,
    page_size: pageSize.value,
    search: searchQuery.value,
    order: sortOrder.value,
    liver: selectedLiverId.value || undefined
  }
}

const updateQueryParams = (newParams) => {
  navigateTo({
    query: {
      ...route.query,
      ...newParams
    }
  })
}

const fetchVideos = async (page = 1) => {
  videos.value = await $api.get('videos/', {
    params: getQueryParams(page)
  })
}

const watchRouteChanges = () => {
  watch(
    () => route.fullPath,
    () => {
      currentPage.value = parseInt(route.query.page) || 1
      searchQuery.value = route.query.search || ''
      sortOrder.value = route.query.order || 'desc'
      selectedLiverId.value = route.query.liver || ''
      fetchVideos(currentPage.value)
    }
  )
}

onBeforeMount(async () => {
  await fetchLivers()
  await fetchVideos(currentPage.value)
  watchRouteChanges()
})

const nextPage = () => {
  if (videos.value.next) {
    currentPage.value++
    updateQueryParams(getQueryParams(currentPage.value))
  }
}

const prevPage = () => {
  if (videos.value.previous) {
    currentPage.value--
    updateQueryParams(getQueryParams(currentPage.value))
  }
}

const goToPage = (page) => {
  currentPage.value = page
  updateQueryParams(getQueryParams(currentPage.value))
}

const searchVideos = () => {
  currentPage.value = 1
  updateQueryParams(getQueryParams(currentPage.value))
}

const sortVideos = () => {
  currentPage.value = 1
  updateQueryParams(getQueryParams(currentPage.value))
}

const filterByLiver = () => {
  currentPage.value = 1
  updateQueryParams(getQueryParams(currentPage.value))
}

const truncateText = (text, maxLength) => {
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}
</script>
