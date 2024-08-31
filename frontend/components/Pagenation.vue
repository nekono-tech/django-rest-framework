<template>
  <div class="flex justify-center mt-4 space-x-2">
    <button @click="$emit('prevPage')" :disabled="!hasPrevious" class="px-4 py-2 bg-gray-300 rounded">前へ</button>
    <button
      v-for="page in paginationPages"
      :key="page"
      @click="goToPage(page)"
      :class="['px-4 py-2 rounded', { 'bg-blue-500 text-white': currentPage === page, 'bg-gray-300': currentPage !== page }]"
      v-if="page !== '...'"
      :disabled="page === '...'"
    >
      {{ page }}
    </button>
    <span v-else class="px-2">...</span>

    <button @click="$emit('nextPage')" :disabled="!hasNext" class="px-4 py-2 bg-gray-300 rounded">次へ</button>
  </div>
</template>

<script setup>
const props = defineProps({
  totalPages: Number,
  currentPage: Number,
  hasNext: Boolean,
  hasPrevious: Boolean,
})

const emit = defineEmits(['nextPage', 'prevPage', 'goToPage'])

const paginationPages = computed(() => {
  const pages = []
  const maxPagesToShow = 7

  if (props.totalPages <= maxPagesToShow) {
    for (let i = 1; i <= props.totalPages; i++) {
      pages.push(i)
    }
  } else {
    if (props.currentPage <= 3) {
      for (let i = 1; i <= 4; i++) {
        pages.push(i)
      }
      pages.push('...')
      pages.push(props.totalPages)
    } else if (props.currentPage > 3 && props.currentPage < props.totalPages - 2) {
      pages.push(1)
      pages.push('...')
      for (let i = props.currentPage - 1; i <= props.currentPage + 1; i++) {
        pages.push(i)
      }
      pages.push('...')
      pages.push(props.totalPages)
    } else {
      pages.push(1)
      pages.push('...')
      for (let i = props.totalPages - 3; i <= props.totalPages; i++) {
        pages.push(i)
      }
    }
  }

  return pages
})

const goToPage = (page) => {
  emit('goToPage', page)
}
</script>
