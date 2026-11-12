import antfu from '@antfu/eslint-config'

const designSystemImports = {
  regex: '^(@gouv(fr|minint)/|@shallowred/jsonforms-vue-dsfr)',
  message: 'The DSFR is reserved for the sites of the French State: only sites/gouv-fr and elements/ import it.',
}

const engineImports = {
  regex: '^@datagouv/regles-engine-',
  message: 'The input form of a rule runs it through a Calculator of web/calculation/calculator.ts: a project outside web/ and sites/ builds a local calculator from an engine adapter.',
}

const frameworkImports = '^(vue|nuxt|#|~|h3|node:)'

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
      'no-restricted-imports': ['error', { patterns: [designSystemImports, engineImports] }],
    },
  },
  {
    files: ['sites/gouv-fr/**'],
    rules: {
      'no-restricted-imports': ['error', { patterns: [engineImports] }],
    },
  },
  {
    files: ['web/catalogue/**'],
    rules: {
      'no-restricted-imports': ['error', {
        patterns: [{
          regex: frameworkImports,
          message: 'The catalogue holds pure presenters from a record to a view model, kept out of the framework: it imports @datagouv/regles-core and its own files.',
        }, designSystemImports, engineImports],
      }],
    },
  },
  {
    files: ['web/calculation/**'],
    rules: {
      'no-restricted-imports': ['error', {
        patterns: [{
          regex: frameworkImports,
          message: 'The calculation runs a rule through a calculator, a calculation service or an engine in the page, and presents its results out of the framework: it imports its own files.',
        }, designSystemImports, engineImports],
      }],
    },
  },
  {
    files: ['**/routes.ts'],
    rules: {
      'no-restricted-imports': ['error', {
        patterns: [{
          regex: frameworkImports,
          message: 'A routes.ts file declares the routes of its layer out of the framework: the presenters and modules/view-routes.ts import it.',
        }, designSystemImports, engineImports],
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
        }, designSystemImports, engineImports],
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
