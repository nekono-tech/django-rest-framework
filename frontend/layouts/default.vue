<template>
  <div>
    <header class="bg-gray-800 text-white py-4 px-8">
      <div class="container mx-auto flex">
        <div class="flex items-center space-x-4">
          <nuxt-link to="/" class="flex items-center">
            <img src="https://i.ytimg.com/vi/JtV0PdXyjeE/maxresdefault.jpg" alt="Logo" class="h-8 w-auto" />
          </nuxt-link>
          <nuxt-link to="/about" class="text-white hover:text-gray-300">
            About
          </nuxt-link>
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
