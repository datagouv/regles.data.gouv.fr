import antfu from '@antfu/eslint-config'

const designSystemImports = {
  regex: '^@gouv(fr|minint)/',
  message: 'The DSFR is reserved for the sites of the French State: only sites/gouv-fr imports it.',
}

const noStyle = 'The shared layer holds no style: compose the UI components whose props are declared in web/shared/types/ui.ts.'

export default antfu(
  {
    typescript: true,
    vue: true,
    stylistic: {
      overrides: {
        'antfu/curly': 'off',
        'curly': ['error', 'all'],
        'style/brace-style': ['error', 'stroustrup', { allowSingleLine: false }],
        'style/multiline-ternary': ['error', 'always'],
      },
    },
    toml: false,
    pnpm: false,
    markdown: false,
    ignores: ['contract/', 'data/', 'docs/', '.github/'],
  },
  {
    files: ['web/**', 'sites/white-label/**'],
    rules: {
      'no-restricted-imports': ['error', { patterns: [designSystemImports] }],
    },
  },
  {
    files: ['web/catalogue/**'],
    rules: {
      'no-restricted-imports': ['error', {
        patterns: [{
          regex: '^(vue|nuxt|#|~|h3|node:)',
          message: 'The catalogue holds pure presenters from a record to a view model, kept out of the framework: it imports @datagouv/regles-core and its own files.',
        }, designSystemImports],
      }],
    },
  },
  {
    files: ['web/app/**'],
    rules: {
      'no-restricted-imports': ['error', {
        patterns: [{
          regex: '^@datagouv/regles-core',
          message: 'Pages and components read view models from the server routes, prepared by web/catalogue.',
        }, designSystemImports],
      }],
      'vue/no-restricted-block': ['error', {
        element: 'style',
        message: 'The shared layer holds no style: each site under sites/ styles its UI components.',
      }],
      'vue/no-restricted-static-attribute': ['error', ...['class', 'style'].map(key => ({ key, message: noStyle }))],
      'vue/no-restricted-v-bind': ['error', ...['class', 'style'].map(argument => ({ argument, message: noStyle }))],
    },
  },
)
