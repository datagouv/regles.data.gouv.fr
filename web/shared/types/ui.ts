export interface UiLink {
  label: string
  to: string
}

export interface UiCard {
  title: string
  description: string
  to: string
}

export interface UiCardListProps {
  cards: UiCard[]
}

export interface UiBreadcrumbProps {
  links: UiLink[]
  current: string
}
