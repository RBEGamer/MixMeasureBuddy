type HeaderNavLink = {
  id: string;
  href: string;
  title: string;
  requiresBackend?: boolean;
};

export const headerNavLinks: HeaderNavLink[] = [
  { id: 'home', href: '/', title: 'Home' },
  { id: 'editor', href: '/editor', title: 'Recipe Editor' },
  { id: 'mixer', href: '/mixer', title: 'Mix Lab' },
  { id: 'manage', href: '/manage', title: 'Manage', requiresBackend: true },
  { id: 'gallery', href: '/gallery', title: 'Recipe Gallery' },
];
