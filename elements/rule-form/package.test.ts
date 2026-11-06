import { readFileSync } from 'node:fs'
import { expect, it } from 'vitest'

// npm installs the dependencies, peer dependencies and optional dependencies of an installed archive
it('declares nothing that npm would install with the archive', () => {
  const manifest = JSON.parse(readFileSync(new URL('package.json', import.meta.url), 'utf8'))

  expect(manifest).not.toHaveProperty('dependencies')
  expect(manifest).not.toHaveProperty('peerDependencies')
  expect(manifest).not.toHaveProperty('optionalDependencies')
})
