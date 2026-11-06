import process from 'node:process'
import { defineConfig, devices } from '@playwright/test'

const sites = [
  { name: 'gouv-fr', port: 4101 },
  { name: 'white-label', port: 4102 },
]

export default defineConfig({
  testDir: 'e2e',
  forbidOnly: Boolean(process.env.CI),
  reporter: process.env.CI
    ? 'github'
    : 'list',
  projects: sites.map(site => ({
    name: site.name,
    use: { ...devices['Desktop Chrome'], baseURL: `http://localhost:${site.port}` },
  })),
  // the generated site, as it is deployed
  webServer: sites.map(site => ({
    command: `pnpm exec serve --no-clipboard --listen ${site.port} sites/${site.name}/.output/public`,
    url: `http://localhost:${site.port}`,
  })),
})
