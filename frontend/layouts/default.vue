<template>
  <div class="min-h-screen flex flex-col text-slate-500 dark:text-slate-400 bg-white dark:bg-slate-900">
    <header class="py-4 border-b border-slate-900/10 dark:border-slate-300/10">
      <UContainer>
        <div class="flex items-center space-x-4">
          <ULink 
            to="/"
            active-class="text-primary"
            class="hover:text-primary hover:dark:text-primary"
          >
            nijisearch
          </ULink>
          <ULink 
            to="/about"
            active-class="text-primary"
            class="hover:text-primary hover:dark:text-primary"
          >
            About
          </ULink>
        </div>
      </UContainer>
    </header>
    <main class="py-4 flex-grow">
      <slot/>
    </main>
    <footer class="py-12 border-t border-slate-900/10 dark:border-slate-300/10">
      <UContainer class="mx-auto text-center">
        <p class="text-sm">&copy; 2024 nijisearch</p>
        <p class="text-xs mt-2">
          本サイトは有志による二次創作であり、株式会社ANYCOLOR様には一切の関係がありません。
        </p>
      </UContainer>
    </footer>
  </div>
</template>
