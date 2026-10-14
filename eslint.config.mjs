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
)
