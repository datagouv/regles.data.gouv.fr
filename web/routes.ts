export const routes = {
  catalogue: '/',
  record: '/regles/:identifier',
} as const

export type RouteName = keyof typeof routes

export function recordPath(identifier: string): string {
  return routes.record.replace(':identifier', encodeURIComponent(identifier))
}
