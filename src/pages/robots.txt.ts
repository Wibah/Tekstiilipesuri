import type { APIRoute } from 'astro';

export const GET: APIRoute = ({ site }) => {
  return new Response(
    `User-agent: *\nAllow: /\nSitemap: ${new URL('sitemap-index.xml', site).href}`,
    { headers: { 'Content-Type': 'text/plain' } }
  );
};
