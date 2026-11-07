const SEPARATOR = ' . '
const KEY_SEPARATOR = '__'

// JSON Forms reads a dot in a property name as a path into nested objects
export function keyOf(dottedName: string): string {
  return dottedName.split(SEPARATOR).join(KEY_SEPARATOR)
}

export function dottedNameOf(key: string): string {
  return key.split(KEY_SEPARATOR).join(SEPARATOR)
}
