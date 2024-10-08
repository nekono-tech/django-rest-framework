<template>
  <div class="container mx-auto py-2 px-6 sm:px-2">
    <UProgress v-if="isLoading" animation="carousel" class="fixed top-0 left-0"/>

    <div class="mb-4 mt-4 flex flex-col items-center space-y-4">
      <div class="max-w-xl" v-if="selectedLivers.length > 0">
        <p>選択中のライバー</p>
        <UBadge v-for="liver in selectedLivers" :key="liver.value" :label="liver.label" color="gray"/>
      </div>

      <UButtonGroup orientation="horizontal" class="w-full max-w-xl" size="md">
        <UInput
          icon="i-heroicons-magnifying-glass-20-solid"
          class="flex-grow"
          v-model="model.q"
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
          <div class="flex flex-col pb-4">
            <label for="choosePattern" class="mb-1">キーワードの検索対象</label>
            <div class="flex gap-4">
              <UCheckbox v-model="selectedPatterns" :value="1" label="動画タイトル" />
              <UCheckbox v-model="selectedPatterns" :value="2" label="動画概要" />
              <UCheckbox v-model="selectedPatterns" :value="3" label="ライバー名" />
            </div>
          </div>
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
              <div class="flex gap-2">
                <ClientOnly>
                  <USelectMenu
                    searchable
                    searchable-placeholder="ライバー名で検索..."
                    id="chooseLiver"
                    v-model="selectedLivers"
                    multiple
                    size="md"
                    :options="filterLivers"
                    @change="filterByLiver"
                    class="min-w-[200px]"
                  />
                </ClientOnly>
                <div class="flex ">
                  <UButton @click="clearLivers" label="絞り込みをクリア"/>
                </div>
              </div>
            </div>
          </div>
        </template>
      </UAccordion>
    </div>

    <div class="mb-4">
      {{ displayedRange }} / {{ videos.count }} 件 を表示
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
  q: route.query.q || '',
  order: route.query.order || 'desc',
  livers: []
})

const selectedPatterns = ref([]);
const selectedLivers = ref([])

const filterPublishedDate = [{
  label: '公開日時が新しい順',
  value: 'desc'
}, {
  label: '公開日時が古い順',
  value: 'asc'
}]

const filterLivers = ref([])

const fetchLivers = async () => {
  livers.value = await $api.get('livers/')
}

const navigateWithQuery = () => {
  const joinLivers = model.value.livers.join(',')
  navigateTo({
    query: {
      ...model.value,
      livers: joinLivers,
      pattern: selectedPatterns.value.join(','),
    }
  })
}

const fetchVideos = async () => {
  isLoading.value = true

  const queryParams = {
    ...model.value,
    livers: model.value.livers.join(','),
    pattern: selectedPatterns.value.join(','),
  }

  videos.value = await $api.get('videos/', { params: queryParams })
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
  model.value.livers = selectedLivers.value.map(liver => liver.value).filter(value => value)
  navigateWithQuery()
}

const clearLivers = () => {
  selectedLivers.value = []
  filterByLiver()
}

await fetchLivers()
await fetchVideos(model.value.page)
filterLivers.value.push(...livers.value.map(liver => ({
  label: liver.name,
  value: liver.id
})))

selectedLivers.value = route.query.livers 
  ? route.query.livers.split(',').map(id => {
      const liver = filterLivers.value.find(l => l.value === parseInt(id))
      return liver || { label: '', value: parseInt(id) }
    })
  : []

const displayedRange = computed(() => {
  const start = (model.value.page - 1) * model.value.page_size + 1;
  const end = Math.min(model.value.page * model.value.page_size, videos.value.count);
  return `${start} ~ ${end}件`;
});

watch(
  () => route.query,
  (newQuery) => {
    model.value = {
      page: parseInt(newQuery.page) || 1,
      page_size: parseInt(newQuery.page_size) || 16,
      q: newQuery.q || '',
      order: newQuery.order || 'desc',
      livers: newQuery.livers ? newQuery.livers.split(',').map(id => parseInt(id)) : []
    }
    selectedLivers.value = newQuery.livers 
      ? newQuery.livers.split(',').map(id => {
          const liver = filterLivers.value.find(l => l.value === parseInt(id))
          return liver || { label: '', value: parseInt(id) }
        })
      : []

    selectedPatterns.value = newQuery.pattern ? newQuery.pattern.split(',').map(Number) : [1, 2, 3];
    fetchVideos(model.value.page)
  },
  { immediate: true }
)
</script>
