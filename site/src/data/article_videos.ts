/**
 * Stories vidéo curées manuellement, attachées à un article actu (slug = filename .md sans extension).
 * Vérification "officiel" via oEmbed author_name = chaîne du protagoniste / média grand public légitime.
 * Pour les articles éditoriaux long-format (politique, culture), on relâche la règle "duration < 20 min" :
 * le contenu de référence cité par l'article reste pertinent même en long format.
 * Last curated : 2026-04-25.
 */

export type StoryType = "decryptage" | "context" | "extrait" | "analyse";

export interface ArticleStory {
  /** Slug-style id, ex "ruffin-claude-conversation-officielle" */
  id: string;
  /** Matche le filename (sans .md) dans src/content/actu/ */
  articleSlug: string;
  type: StoryType;
  youtubeId: string;
  /** Titre FR affiché sur la card (line-clamp 2) */
  title: string;
  /** "mm:ss" extrait de lengthSeconds de la watch page */
  duration: string;
  /** Affiché aussi dans la home rail si true (cap à 4-5) */
  isHomeFeatured?: boolean;
  /** Si "en" et locale visiteur != en, badge "EN" sur la card */
  audioLocale?: "en" | "fr";
  /** Nom de la chaîne YouTube source, affiché en bottom-left de la card (remplace le logo bot) */
  channelName: string;
  /** Hex override du halo/accent (sinon var(--color-primary)) */
  accent?: string;
}

export const ARTICLE_STORIES: ArticleStory[] = [
  // === Article : ruffin-tiktok-claude-politique-rencontre-ia ===
  {
    id: "ruffin-claude-conversation-officielle",
    articleSlug: "ruffin-tiktok-claude-politique-rencontre-ia",
    type: "decryptage",
    youtubeId: "OSAHTpRaKtw",
    title: "Une conversation avec Claude (chaîne officielle Ruffin)",
    duration: "33:07",
    isHomeFeatured: true,
    audioLocale: "fr",
    channelName: "FRANÇOIS RUFFIN",
    accent: "#e63946",
  },
  {
    id: "ruffin-blast-ia-fin-emploi",
    articleSlug: "ruffin-tiktok-claude-politique-rencontre-ia",
    type: "context",
    youtubeId: "zJqx2lfi58o",
    title: "IA : la fin de l'emploi ? (mais pas des profits pour les patrons)",
    duration: "22:05",
    audioLocale: "fr",
    channelName: "BLAST",
    accent: "#f77f00",
  },
  {
    id: "ruffin-blast-au-boulot",
    articleSlug: "ruffin-tiktok-claude-politique-rencontre-ia",
    type: "extrait",
    youtubeId: "PmMMAtN5oQw",
    title: "Au boulot ! Portrait d'une France brisée par le travail",
    duration: "44:45",
    audioLocale: "fr",
    channelName: "BLAST",
    accent: "#f77f00",
  },

  // === Article : skibidi-tentafruit-266-millions-vues-2-etudiants-metiers-audiovisuel ===
  // Article encore en queue (blog-auto/queue-actu/), entrée prête pour activation au passage live.
  {
    id: "skibidi-tentafruit-m6-analyse",
    articleSlug: "skibidi-tentafruit-266-millions-vues-2-etudiants-metiers-audiovisuel",
    type: "analyse",
    youtubeId: "gKrluGYTC5s",
    title: "Pourquoi Skibidi Tentafruit fait des millions de vues sur TikTok",
    duration: "1:39",
    isHomeFeatured: true,
    audioLocale: "fr",
    channelName: "M6 Info",
    accent: "#1d3557",
  },

  // === Article : ocde-27-pourcent-emplois-france-automatisation ===
  {
    id: "france24-metiers-ia-disparaissent-emergent",
    articleSlug: "ocde-27-pourcent-emplois-france-automatisation",
    type: "decryptage",
    youtubeId: "ASwu-QcRRmk",
    title: "IA : ces metiers qui disparaissent, et ceux qui emergent",
    duration: "07:38",
    isHomeFeatured: true,
    audioLocale: "fr",
    channelName: "FRANCE 24",
    accent: "#0a4d8c",
  },

  // === Article : lia-en-entreprise-le-vrai-bilan-des-suppressions-demplois-en-2026 ===
  {
    id: "hugodecrypte-chute-ia-crise-economique",
    articleSlug: "lia-en-entreprise-le-vrai-bilan-des-suppressions-demplois-en-2026",
    type: "context",
    youtubeId: "IOMAn8Beybs",
    title: "La chute dans l'IA qui fait craindre une crise economique",
    duration: "15:01",
    isHomeFeatured: true,
    audioLocale: "fr",
    channelName: "HugoDécrypte - Actus du jour",
    accent: "#111111",
  },

  // === Article : meta-8000-licenciements-mai-2026-pari-ia-zuckerberg-decrypte ===
  {
    id: "radiocanada-inquietude-licenciements-ia",
    articleSlug: "meta-8000-licenciements-mai-2026-pari-ia-zuckerberg-decrypte",
    type: "analyse",
    youtubeId: "rCzgU3eRCr0",
    title: "Inquietude face aux licenciements lies a l'essor de l'IA",
    duration: "02:19",
    isHomeFeatured: true,
    audioLocale: "fr",
    channelName: "Radio-Canada Info",
    accent: "#c8102e",
  },

  // === Article : 5-millions-demplois-menaces-par-lia-en-france-le-vrai-decryptage-des-chiffres-qu ===
  {
    id: "radiocanada-quels-emplois-disparaissent-ia",
    articleSlug: "5-millions-demplois-menaces-par-lia-en-france-le-vrai-decryptage-des-chiffres-qu",
    type: "decryptage",
    youtubeId: "I_BI3lJUnq8",
    title: "Quels emplois vont disparaitre avec l'IA ?",
    duration: "06:00",
    isHomeFeatured: true,
    audioLocale: "fr",
    channelName: "Radio-Canada Info",
    accent: "#c8102e",
  },

  // === Article : gemini-20-debarque-google-lance-lere-des-agents-ia-qui-vont-te-remplacer-ou-taid ===
  {
    id: "scienceetonnante-fonctionnement-chatgpt",
    articleSlug: "gemini-20-debarque-google-lance-lere-des-agents-ia-qui-vont-te-remplacer-ou-taid",
    type: "context",
    youtubeId: "7ell8KEbhJo",
    title: "Ce qui se cache derriere le fonctionnement de ChatGPT",
    duration: "27:23",
    isHomeFeatured: true,
    audioLocale: "fr",
    channelName: "ScienceEtonnante",
    accent: "#3a86ff",
  },

  // === Article : ipsos-47-pourcent-actifs-reconversion-ia ===
  {
    id: "monsieurphi-chatgpt-vraiment-capable",
    articleSlug: "ipsos-47-pourcent-actifs-reconversion-ia",
    type: "analyse",
    youtubeId: "R2fjRbc9Sa0",
    title: "De quoi ChatGPT est-il vraiment capable ?",
    duration: "37:22",
    isHomeFeatured: true,
    audioLocale: "fr",
    channelName: "Monsieur Phi",
    accent: "#6a4c93",
  },
];

export function storiesForArticle(slug: string): ArticleStory[] {
  return ARTICLE_STORIES.filter((s) => s.articleSlug === slug);
}

export function homeFeaturedStories(): ArticleStory[] {
  return ARTICLE_STORIES.filter((s) => s.isHomeFeatured === true);
}
