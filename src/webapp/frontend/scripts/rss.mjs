import { writeFileSync, mkdirSync, readFileSync } from 'fs';
import path from 'path';
import GithubSlugger from 'github-slugger';
import { escape } from '@shipixen/pliny/utils/htmlEscaper.js';
import { siteConfig } from '../data/config/site.settings.js';
import { fileURLToPath } from 'url';

const moduleDir = path.dirname(fileURLToPath(import.meta.url));

const loadJson = (relativePath) => {
  const absolutePath = path.join(moduleDir, relativePath);
  const raw = readFileSync(absolutePath, { encoding: 'utf8' });
  return JSON.parse(raw);
};

const tagData = loadJson('../app/tag-data.json');

const loadBlogs = () => {
  try {
    const blogsPath = path.join(
      moduleDir,
      '../.contentlayer/generated/Blog/_index.json',
    );
    const raw = readFileSync(blogsPath, { encoding: 'utf8' });
    return JSON.parse(raw);
  } catch (error) {
    console.warn(
      '[rss] Skipped RSS generation because contentlayer output was unavailable:',
      error instanceof Error ? error.message : error,
    );
    return [];
  }
};

const BLOG_URL = siteConfig.blogPath ? `/${siteConfig.blogPath}` : '';

const generateRssItem = (config, post) => `
  <item>
    <guid>${config.siteUrl}${BLOG_URL}/${post.slug}</guid>
    <title>${escape(post.title)}</title>
    <link>${config.siteUrl}${BLOG_URL}/${post.slug}</link>
    ${post.summary && `<description>${escape(post.summary)}</description>`}
    <pubDate>${new Date(post.date).toUTCString()}</pubDate>
    <author>${config.email} (${config.author})</author>
    ${post.tags && post.tags.map((t) => `<category>${t}</category>`).join('')}
  </item>
`;

const generateRss = (config, posts, page = 'feed.xml') => `
  <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
      <title>${escape(config.title)}</title>
      <link>${config.siteUrl}${BLOG_URL}</link>
      <description>${escape(config.description)}</description>
      <language>${config.language}</language>
      <managingEditor>${config.email} (${config.author})</managingEditor>
      <webMaster>${config.email} (${config.author})</webMaster>
      <lastBuildDate>${new Date(posts[0].date).toUTCString()}</lastBuildDate>
      <atom:link href="${
        config.siteUrl
      }/${page}" rel="self" type="application/rss+xml"/>
      ${posts.map((post) => generateRssItem(config, post)).join('')}
    </channel>
  </rss>
`;

async function generateRSS(config, allBlogs, page = 'feed.xml') {
  const publishPosts = allBlogs.filter((post) => post.draft !== true);
  // RSS for post
  if (publishPosts.length > 0) {
    const rss = generateRss(config, publishPosts);
    writeFileSync(`./public/${page}`, rss);
  }

  if (publishPosts.length > 0) {
    for (const tag of Object.keys(tagData)) {
      const filteredPosts = allBlogs.filter((post) =>
        post.tags.map((t) => GithubSlugger.slug(t)).includes(tag),
      );
      const rss = generateRss(config, filteredPosts, `tags/${tag}/${page}`);
      const rssPath = path.join('public', 'tags', tag);
      mkdirSync(rssPath, { recursive: true });
      writeFileSync(path.join(rssPath, page), rss);
    }
  }
}

const rss = async () => {
  const blogs = loadBlogs();
  if (blogs.length === 0) {
    console.warn('[rss] No blog posts found; RSS feeds were not written.');
    return;
  }

  generateRSS(siteConfig, blogs);
  console.log('RSS feed generated...');
};
export default rss;
