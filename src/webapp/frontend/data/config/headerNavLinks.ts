const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

export const headerNavLinks = [
  { href: '/', title: 'Home' },
  { href: '/editor', title: 'Recipe Editor' },
  { href: '/mixer', title: 'Mix Lab' },
  ...(backendUrl ? [{ href: '/manage', title: 'Manage' }] : []),
  { href: '/gallery', title: 'Recipe Gallery' }
]
