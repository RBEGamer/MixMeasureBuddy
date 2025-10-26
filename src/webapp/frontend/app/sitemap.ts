import { MetadataRoute } from 'next';
import { siteConfig } from '@/data/config/site.settings';
import { readFileSync } from 'fs';
import path from 'path';

const loadBlogs = () => {
  try {
    const filePath = path.join(
      process.cwd(),
      '.contentlayer',
      'generated',
      'Blog',
      '_index.json',
    );
    const raw = readFileSync(filePath, { encoding: 'utf8' });
    return JSON.parse(raw);
  } catch (_error) {
    return [];
  }
};

export default function sitemap(): MetadataRoute.Sitemap {
  const siteUrl = siteConfig.siteUrl;
  const allBlogs = loadBlogs();
  const blogRoutes = allBlogs
    .filter((post) => !post.draft)
    .map((post) => ({
      url: `${siteUrl}/${post.path}`,
      lastModified: post.lastmod || post.date,
    }));

  const routes = ['', 'overview', 'tags'].map((route) => ({
    url: `${siteUrl}/${route}`,
    lastModified: new Date().toISOString().split('T')[0],
  }));

  return [...routes, ...blogRoutes];
}
