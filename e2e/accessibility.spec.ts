import type { Page } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'
import { expect, test } from '@playwright/test'

const WCAG_21_AA = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']

async function findViolations(page: Page) {
  const results = await new AxeBuilder({ page }).withTags(WCAG_21_AA).analyze()
  return results.violations
}

test('the catalogue has no axe violation of WCAG 2.1 AA', async ({ page }) => {
  await page.goto('/')
  expect(await findViolations(page)).toEqual([])
})

test('a record page has no axe violation of WCAG 2.1 AA', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('main').getByRole('heading', { level: 2 }).first().getByRole('link').click()
  await expect(page).toHaveURL(/\/regles\//)
  expect(await findViolations(page)).toEqual([])
})

test('the pages of the main navigation have no axe violation of WCAG 2.1 AA', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name === 'white-label', 'the white-label site has no main navigation')
  await page.goto('/')
  const links = page.getByRole('navigation', { name: 'Menu principal' }).getByRole('link')
  const paths = await links.evaluateAll(anchors => anchors.map(anchor => (anchor as HTMLAnchorElement).pathname))
  expect(paths).not.toHaveLength(0)
  for (const path of paths) {
    await page.goto(path)
    expect(await findViolations(page), path).toEqual([])
  }
})
