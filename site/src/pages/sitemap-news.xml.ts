import { getCollection } from "astro:content";
import { siteConfig } from "../../site.config";

// Google News sitemap : derniers 48h max, format <news:news>.
// Reference : https://developers.google.com/search/docs/crawling-indexing/sitemaps/news-sitemap
// Utilise par Google pour detecter rapidement les nouvelles publications editoriales.
// Les sites inscrits a Google News Publisher Center en beneficient le plus,
// mais il reste un signal positif hors inscription.

const NEWS_WINDOW_MS = 48 * 60 * 60 * 1000; // 48h

function escapeXml(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

export async function GET(context: { site?: URL }) {
  const siteUrl = (context.site?.toString() ?? siteConfig.url).replace(/\/$/, "");
  const now = Date.now();
  const cutoff = now - NEWS_WINDOW_MS;

  const recent = (await getCollection("actu", ({ data }) => !data.draft))
    .filter((p) => p.data.date.valueOf() >= cutoff)
    .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf())
    .slice(0, 1000);

  const urls = recent.map((p) => {
    const loc = `${siteUrl}/actu/${p.id}`;
    const pubDate = p.data.date.toISOString();
    const title = escapeXml(p.data.title);
    return `  <url>
    <loc>${escapeXml(loc)}</loc>
    <news:news>
      <news:publication>
        <news:name>Adapte-toi Décrypte</news:name>
        <news:language>fr</news:language>
      </news:publication>
      <news:publication_date>${pubDate}</news:publication_date>
      <news:title>${title}</news:title>
    </news:news>
  </url>`;
  }).join("\n");

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
${urls}
</urlset>`;

  return new Response(xml, {
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
      "Cache-Control": "public, max-age=600",
    },
  });
}
