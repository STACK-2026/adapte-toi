import { getCollection } from "astro:content";
import { siteConfig } from "../../site.config";

type Entry = {
  id: string;
  data: {
    title: string;
    description: string;
    date?: Date;
    draft?: boolean;
  };
};

function clean(value: string): string {
  return value.replace(/\s+/g, " ").trim();
}

function listSection(label: string, path: string, entries: Entry[]): string {
  const ordered = [...entries].sort((a, b) => {
    const ad = a.data.date?.valueOf() ?? 0;
    const bd = b.data.date?.valueOf() ?? 0;
    return bd - ad || a.data.title.localeCompare(b.data.title, "fr");
  });
  return [
    `## ${label}`,
    "",
    ...ordered.flatMap((entry) => [
      `- [${clean(entry.data.title)}](${siteConfig.url}/${path}/${entry.id}/)`,
      `  ${clean(entry.data.description)}`,
    ]),
    "",
  ].join("\n");
}

export async function GET() {
  const [actus, metiers, guides, outils, blogs] = await Promise.all([
    getCollection("actu", ({ data }) => !data.draft),
    getCollection("metiers", ({ data }) => !data.draft),
    getCollection("guides", ({ data }) => !data.draft),
    getCollection("outils", ({ data }) => !data.draft),
    getCollection("blog", ({ data }) => !data.draft),
  ]);

  const body = [
    "# Adapte-toi : index éditorial complet",
    "",
    "> Média francophone indépendant consacré à l'impact de l'intelligence artificielle sur le travail, les métiers et la reconversion professionnelle.",
    "",
    "Ce fichier est un index de commodité pour les agents et outils qui choisissent de le lire. Les pages HTML, les liens canoniques, robots.txt et les sitemaps restent les sources de vérité.",
    "",
    "## Identité et politiques",
    "",
    `- [À propos](${siteConfig.url}/a-propos/)`,
    `- [Politique éditoriale](${siteConfig.url}/politique-editoriale/)`,
    `- [Charte éditoriale](${siteConfig.url}/charte-editoriale/)`,
    `- [Politique de correction](${siteConfig.url}/politique-de-correction/)`,
    `- [Sources de financement](${siteConfig.url}/sources-financement/)`,
    `- [Baromètre et méthodologie](${siteConfig.url}/barometre/)`,
    "",
    listSection("Actualités et décryptages", "actu", actus as Entry[]),
    listSection("Fiches métier", "metiers", metiers as Entry[]),
    listSection("Guides pratiques", "guides", guides as Entry[]),
    listSection("Outils IA", "outils", outils as Entry[]),
    listSection("Analyses longues", "blog", blogs as Entry[]),
    "## Flux et index",
    "",
    `- [RSS](${siteConfig.url}/rss.xml)`,
    `- [Sitemap principal](${siteConfig.url}/sitemap-index.xml)`,
    `- [Sitemap Google News](${siteConfig.url}/sitemap-news.xml)`,
    `- [Index IA](${siteConfig.url}/ai-sitemap.xml)`,
    "",
  ].join("\n");

  return new Response(body, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
}
