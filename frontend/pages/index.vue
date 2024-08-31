<template>
  <div class="container mx-auto py-2 px-1">
    <div class="mb-4 mt-4 flex flex-col sm:flex-row justify-center items-center space-y-2 sm:space-y-0 sm:space-x-4">
      <div class="flex flex-col sm:flex-row max-w-xl w-full">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="動画を検索..."
          class="flex-grow p-2 border border-gray-300 rounded-t sm:rounded-l sm:rounded-t-none"
          @input="searchVideos"
        />
        <select v-model="sortOrder" @change="sortVideos" class="p-2 border border-gray-300 rounded-b sm:rounded-r sm:rounded-b-none sm:w-auto">
          <option value="desc">公開日時が新しい順</option>
          <option value="asc">公開日時が古い順</option>
        </select>
      </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2">
      <div v-for="video in videos.results" :key="video.video_id" class="flex flex-row bg-white overflow-hidden">
        <div class="w-1/2 flex flex-col p-2">
          <img
            :src="video.thumbnail_high_url"
            alt="Thumbnail"
            class="w-full aspect-w-16 aspect-h-9 object-cover"
          />
          <p class="text-xs text-gray-500 mt-1">公開日時: {{ video.published_at }}</p>
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
const route = useRoute()

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

const totalPages = computed(() => Math.ceil(videos.value.count / pageSize.value))

const getQueryParams = (page) => {
  return {
    page: page,
    page_size: pageSize.value,
    search: searchQuery.value,
    order: sortOrder.value
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
      fetchVideos(currentPage.value)
    }
  )
}

onBeforeMount(() => {
  fetchVideos(currentPage.value)
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

const truncateText = (text, maxLength) => {
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}
</script>
