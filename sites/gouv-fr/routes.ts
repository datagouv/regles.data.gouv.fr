export const routes = {
  reference: '/referencer-ses-regles',
} as const

export type RouteName = keyof typeof routes

export const routeTitles: Record<RouteName, string> = {
  reference: 'Référencer ses règles',
}
