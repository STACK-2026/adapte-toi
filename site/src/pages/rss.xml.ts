import rss from "@astrojs/rss";
import { getCollection } from "astro:content";
import { siteConfig } from "../../site.config";

const CATEGORY_LABELS: Record<string, string> = {
  menace: "Menace",
  etude: "Étude",
  annonce: "Annonce",
  politique: "Politique",
  outil: "Outil",
  voix: "Voix",
  chiffre: "Chiffre",
};

export async function GET(context: { site?: URL }) {
  const site = context.site?.toString() ?? siteConfig.url;
  const actu = (await getCollection("actu", ({ data }) => !data.draft))
    .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf())
    .slice(0, 50);
  const blog = (await getCollection("blog", ({ data }) => !data.draft))
    .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf())
    .slice(0, 20);

  const items = [
    ...actu.map((p) => ({
      title: p.data.title,
      pubDate: p.data.date,
      description: p.data.description,
      link: `/actu/${p.id}`,
      categories: [CATEGORY_LABELS[p.data.category] ?? "Décryptage"],
      author: p.data.author ?? "Rédaction Adapte-toi",
    })),
    ...blog.map((p) => ({
      title: p.data.title,
      pubDate: p.data.date,
      description: p.data.description,
      link: `/blog/${p.id}`,
      categories: ["Blog"],
      author: p.data.author ?? "Rédaction Adapte-toi",
    })),
  ]
    .sort((a, b) => b.pubDate.valueOf() - a.pubDate.valueOf())
    .slice(0, 50);

  return rss({
    title: "Adapte-toi Décrypte — IA x emploi x reconversion",
    description:
      "Chaque jour, on décrypte les vraies actualités IA x emploi x reconversion. Études, annonces, voix, menaces : les faits, les chiffres, la citation, ce que ça change pour toi.",
    site,
    items,
    customData: "<language>fr-FR</language>",
    stylesheet: false,
  });
}
