type SearchLink = {
  id: string;
  name: string;
  keywords: string;
  section: string;
  href: string;
  requiresBackend?: boolean;
};

export const searchLinks: SearchLink[] = [
  {
    id: 'home',
    name: 'Home',
    keywords: '',
    section: 'Navigation',
    href: '/',
  },
  {
    id: 'editor',
    name: 'Recipe Editor',
    keywords: '',
    section: 'Navigation',
    href: '/editor',
  },
  {
    id: 'mixer',
    name: 'Mix Lab',
    keywords: '',
    section: 'Navigation',
    href: '/mixer',
  },
  {
    id: 'manage',
    name: 'Manage',
    keywords: '',
    section: 'Navigation',
    href: '/manage',
    requiresBackend: true,
  },
  {
    id: 'gallery',
    name: 'Recipe Gallery',
    keywords: '',
    section: 'Navigation',
    href: '/gallery',
  },
];
