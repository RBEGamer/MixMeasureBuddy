const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

export const searchLinks = [
  {
    id: '',
    name: 'Home',
    keywords: '',
    section: 'Navigation',
    href: '/'
  },
  {
    id: 'editor',
    name: 'Recipe Editor',
    keywords: '',
    section: 'Navigation',
    href: '/editor'
  },
  {
    id: 'mixer',
    name: 'Mix Lab',
    keywords: '',
    section: 'Navigation',
    href: '/mixer'
  },
  ...(backendUrl
    ? [
        {
          id: 'manage',
          name: 'Manage',
          keywords: '',
          section: 'Navigation',
          href: '/manage',
        },
      ]
    : []),
  {
    id: 'gallery',
    name: 'Recipe Gallery',
    keywords: '',
    section: 'Navigation',
    href: '/gallery'
  }
]
