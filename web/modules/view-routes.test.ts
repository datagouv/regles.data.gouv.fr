import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'
import { routes } from '../routes.ts'
import { readLayerPages } from './view-routes.ts'

function layer(path: string) {
  const root = fileURLToPath(new URL(path, import.meta.url))
  return { root, app: `${root}app/` }
}

const web = layer('../')
const site = (fixture: string) => layer(`fixtures/${fixture}/`)

describe('readLayerPages', () => {
  it('serves a page of the site by the view of the site, next to the pages of the shared layer', async () => {
    const legalNotice = site('legal-notice')
    const pages = await readLayerPages([legalNotice, web])
    expect(pages).toContainEqual({ name: 'legalNotice', path: '/mentions-legales', file: `${legalNotice.app}views/LegalNoticeView.vue` })
    expect(pages.map(page => page.name)).toEqual(expect.arrayContaining(Object.keys(routes)))
  })

  it('rejects a site that redeclares a route name of the shared layer, and names both files', async () => {
    await expect(readLayerPages([site('redeclared-name'), web])).rejects.toThrow(
      /fixtures\/redeclared-name\/routes\.ts declares the route catalogue at \/catalogue, already declared by .*web\/routes\.ts as catalogue at \/$/,
    )
  })

  it('rejects a site that redeclares an address of the shared layer', async () => {
    await expect(readLayerPages([site('redeclared-path'), web])).rejects.toThrow(/route home at \/, already declared by .*web\/routes\.ts as catalogue/)
  })

  it('rejects a routes.ts that exports its routes under another name', async () => {
    await expect(readLayerPages([site('no-routes'), web])).rejects.toThrow(/no-routes\/routes\.ts exports no routes/)
  })
})
