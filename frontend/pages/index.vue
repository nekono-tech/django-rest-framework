<template>
  <div class="container mx-auto py-2 px-1">

    <!-- Search -->
    <div class="mb-4 mt-4 flex flex-col items-center space-y-4">
      <UButtonGroup orientation="horizontal" class="w-full max-w-xl" size="md">
        <UInput
          icon="i-heroicons-magnifying-glass-20-solid"
          class="flex-grow"
          v-model="searchQuery"
          color="primary"
          variant="outline"
          placeholder="動画を検索..."
        />
        <UButton 
          @click="searchVideos"
          label="検索" 
          :disabled="isLoading"
          :loading="isLoading" 
        />
      </UButtonGroup>

      <UAccordion :items="[{ label: '検索フィルター', slot: 'filter' }]" class="w-full max-w-xl">
        <template #filter>
          <div class="flex flex-col md:flex-row gap-4">
            <div class="flex flex-col">
              <label for="sortOrder" class="mb-1">日付で並び替え</label>
              <USelect
                id="sortOrder"
                v-model="sortOrder"
                size="md"
                :options="filterPublishedDate"
                @change="sortVideos"
              />
            </div>

            <div class="flex flex-col">
              <label for="chooseLiver" class="mb-1">ライバーで絞り込み</label>
              <USelect
                id="chooseLiver"
                v-model="selectedLiverId"
                size="md"
                :options="filterLivers"
                @change="filterByLiver"
              />
            </div>
          </div>
        </template>
      </UAccordion>
    </div>

    <VideoCards :videos="videos"/>

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

const isLoading = ref(false)
const livers = ref([])
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

const filterPublishedDate = [{
  label: '公開日時が新しい順',
  value: 'desc'
}, {
  label: '公開日時が古い順',
  value: 'asc'
}]

const filterLivers = ref([
  {
    label: 'すべてのライバー',
    value: ''
  },
])

// Computed
const totalPages = computed(() => Math.ceil(videos.value.count / pageSize.value))

// Methods
const fetchLivers = async () => {
  livers.value = await $api.get('livers/')
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
  isLoading.value = true
  try {
    videos.value = await $api.get('videos/', {
      params: getQueryParams(page)
    })
  } finally {
    isLoading.value = false
  }
}

const watchRouteChanges = () => {

}

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

await fetchLivers()
await fetchVideos(currentPage.value)
filterLivers.value.push(...livers.value.map(liver => ({
  label: liver.name,
  value: liver.id
})))

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
</script>

<style scoped>
.loader {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
