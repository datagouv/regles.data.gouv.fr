import antfu from '@antfu/eslint-config'

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
    files: ['web/catalogue/**'],
    rules: {
      'no-restricted-imports': ['error', {
        patterns: [{
          regex: '^(vue|nuxt|#|~|h3|node:)',
          message: 'The catalogue holds pure presenters from a record to a view model, kept out of the framework: it imports @datagouv/regles-core and its own files.',
        }],
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
        }],
      }],
    },
  },
)
