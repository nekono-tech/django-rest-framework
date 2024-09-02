<template>
  <div>
    <header class="bg-gray-800 text-white py-4 px-8">
      <div class="container mx-auto flex">
        <div class="flex items-center space-x-4">
          <a href="/" class="flex items-center">nijisearch</a>
          <a href="/about" class="text-white hover:text-gray-300">
            About
          </a>
        </div>
      </div>
    </header>
    <main>
      <slot/>
    </main>
    <footer class="bg-gray-800 text-white py-4">
      <div class="container mx-auto text-center">
        <p class="text-sm">&copy; 2024 nijisearch</p>
        <p class="text-xs mt-2">
          本サイトは有志による二次創作であり、株式会社ANYCOLOR様には一切の関係がありません。
        </p>
      </div>
    </footer>
  </div>
</template>
