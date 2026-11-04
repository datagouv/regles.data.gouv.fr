export const routes = {
  catalogue: '/',
  record: '/regles/:identifier',
} as const

export function recordPath(identifier: string): string {
  return routes.record.replace(':identifier', encodeURIComponent(identifier))
}

// useFetch infers the response type of the server route from this template literal type
export function recordApiPath(identifier: string): `/api/records/${string}` {
  return `/api/records/${encodeURIComponent(identifier)}`
}
