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
];

export function storiesForArticle(slug: string): ArticleStory[] {
  return ARTICLE_STORIES.filter((s) => s.articleSlug === slug);
}

export function homeFeaturedStories(): ArticleStory[] {
  return ARTICLE_STORIES.filter((s) => s.isHomeFeatured === true);
}
