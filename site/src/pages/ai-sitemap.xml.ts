import type { APIRoute } from "astro";
import { getCollection } from "astro:content";
import { siteConfig } from "../../site.config";

// ai-sitemap.xml : sitemap simplifie dedie aux crawlers IA (pattern STACK-2026).
// Liste flat des URLs prioritaires avec lastmod, sans changefreq/priority.
// Ne remplace pas sitemap-index.xml mais le complete pour ChatGPT/Perplexity/Claude.

const STATIC_PAGES = [
  "/",
  "/a-propos/",
  "/metiers/",
  "/outils/",
  "/guides/",
  "/actu/",
  "/diagnostic/",
  "/barometre/",
  "/glossaire/",
  "/temoignages/",
  "/newsletter/",
];

const today = () => new Date().toISOString().split("T")[0];

const lastmodOf = (post: { data: { lastReviewed?: Date; date: Date } }) =>
  (post.data.lastReviewed ?? post.data.date).toISOString().split("T")[0];

export const GET: APIRoute = async () => {
  const [metiers, outils, guides, actu] = await Promise.all([
    getCollection("metiers", ({ data }) => !data.draft),
    getCollection("outils", ({ data }) => !data.draft),
    getCollection("guides", ({ data }) => !data.draft),
    getCollection("actu", ({ data }) => !data.draft),
  ]);

  const entries: string[] = [];

  for (const page of STATIC_PAGES) {
    entries.push(
      `  <url><loc>${siteConfig.url}${page}</loc><lastmod>${today()}</lastmod></url>`
    );
  }

  for (const post of metiers) {
    entries.push(
      `  <url><loc>${siteConfig.url}/metiers/${post.id}/</loc><lastmod>${lastmodOf(post)}</lastmod></url>`
    );
  }
  for (const post of outils) {
    entries.push(
      `  <url><loc>${siteConfig.url}/outils/${post.id}/</loc><lastmod>${lastmodOf(post)}</lastmod></url>`
    );
  }
  for (const post of guides) {
    entries.push(
      `  <url><loc>${siteConfig.url}/guides/${post.id}/</loc><lastmod>${lastmodOf(post)}</lastmod></url>`
    );
  }
  for (const post of actu.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf())) {
    entries.push(
      `  <url><loc>${siteConfig.url}/actu/${post.id}/</loc><lastmod>${lastmodOf(post)}</lastmod></url>`
    );
  }

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${entries.join("\n")}
</urlset>
`;

  return new Response(xml, {
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
};
