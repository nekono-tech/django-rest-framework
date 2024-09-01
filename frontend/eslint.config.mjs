// @ts-check
import withNuxt from './.nuxt/eslint.config.mjs'

export default withNuxt({
  files: ['**/*.{js,vue,ts}', 'nuxt.config.ts'],
  rules: {
    'indent': ['error', 2],
    'vue/multi-word-component-names': 'off',
  }
})
