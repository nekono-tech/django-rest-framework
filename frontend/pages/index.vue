<template>
  <div class="container mx-auto py-2 px-1">
    <UProgress v-if="isLoading" animation="carousel" class="fixed top-0 left-0"/>

    <div class="mb-4 mt-4 flex flex-col items-center space-y-4">
      <UButtonGroup orientation="horizontal" class="w-full max-w-xl" size="md">
        <UInput
          icon="i-heroicons-magnifying-glass-20-solid"
          class="flex-grow"
          v-model="model.search"
          color="primary"
          variant="outline"
          placeholder="動画を検索..."
          @keydown.enter="searchVideos"
        />
        <UButton 
          @click="searchVideos"
          label="検索" 
          :disabled="isLoading"
        />
      </UButtonGroup>

      <UAccordion :items="[{ label: '検索フィルター', slot: 'filter' }]" class="w-full max-w-xl">
        <template #filter>
          <div class="flex flex-col md:flex-row gap-4">
            <div class="flex flex-col">
              <label for="sortOrder" class="mb-1">日付で並び替え</label>
              <USelect
                id="sortOrder"
                v-model="model.order"
                size="md"
                :options="filterPublishedDate"
                @change="sortVideos"
              />
            </div>

            <div class="flex flex-col">
              <label for="chooseLiver" class="mb-1">ライバーで絞り込み</label>
              <ClientOnly>
                <USelect
                  id="chooseLiver"
                  v-model="model.liver"
                  size="md"
                  :options="filterLivers"
                  @change="filterByLiver"
                />
              </ClientOnly>
            </div>
          </div>
        </template>
      </UAccordion>
    </div>

    <VideoCards :videos="videos.results"/>

    <UPagination 
      v-model="model.page"
      :total="pageItems.length"
      :page-count="model.page_size"
      :to="(page) => ({ 
          query: { ...route.query, page } 
        })"
      size="md"
      class="justify-center mt-6"
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
const pageItems = ref([])

const model = ref({
  page: parseInt(route.query.page) || 1,
  page_size: parseInt(route.query.page_size) || 16,
  search: route.query.search || '',
  order: route.query.order || 'desc',
  liver: route.query.liver || ''
})

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

const fetchLivers = async () => {
  livers.value = await $api.get('livers/')
}

const getQueryParams = () => ({
  ...model.value,
  liver: model.value.liver || undefined
})

const navigateWithQuery = () => {
  navigateTo({
    query: { ...route.query, ...model.value }
  })
}

const fetchVideos = async () => {
  isLoading.value = true
  videos.value = await $api.get('videos/', { params: getQueryParams() })
  pageItems.value = Array.from({ length: videos.value.count }, (_, i) => i + 1)
  isLoading.value = false

  if (import.meta.client) {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    })
  }
}

const searchVideos = () => {
  model.value.page = 1
  navigateWithQuery()
}

const sortVideos = () => {
  model.value.page = 1
  navigateWithQuery()
}

const filterByLiver = () => {
  model.value.page = 1
  navigateWithQuery()
}

await fetchLivers()
await fetchVideos(model.value.page)
filterLivers.value.push(...livers.value.map(liver => ({
  label: liver.name,
  value: liver.id
})))

watch(
  () => route.query,
  (newQuery) => {
    model.value = {
      page: parseInt(newQuery.page) || 1,
      page_size: parseInt(newQuery.page_size) || 16,
      search: newQuery.search || '',
      order: newQuery.order || 'desc',
      liver: newQuery.liver || ''
    }
    fetchVideos(model.value.page)
  },
  { immediate: true }
)
</script>
