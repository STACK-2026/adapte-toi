import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/blog" }),
  schema: z.object({
    title: z.string(),
    description: z.string().max(160),
    date: z.coerce.date(),
    author: z.string().optional(),
    category: z.string().optional(),
    tags: z.array(z.string()).default([]),
    image: z.string().optional(),
    imageAlt: z.string().optional(),
    draft: z.boolean().default(false),
    keywords: z.string().optional(),
    lastReviewed: z.coerce.date().optional(),
    reviewedBy: z.string().optional(),
  }),
});

const pages = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/pages" }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    lastUpdated: z.coerce.date().optional(),
  }),
});

const metiers = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/metiers" }),
  schema: z.object({
    title: z.string(),
    description: z.string().max(160),
    metier: z.string(),
    riskScore: z.number().min(1).max(10),
    riskLevel: z.enum(["faible", "moyen", "eleve", "tres-eleve"]),
    sector: z.string(),
    date: z.coerce.date(),
    lastReviewed: z.coerce.date().optional(),
    author: z.string().optional(),
    image: z.string().optional(),
    imageAlt: z.string().optional(),
    keywords: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

const guides = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/guides" }),
  schema: z.object({
    title: z.string(),
    description: z.string().max(160),
    date: z.coerce.date(),
    lastReviewed: z.coerce.date().optional(),
    author: z.string().optional(),
    category: z.string().optional(),
    readingTime: z.string().optional(),
    keywords: z.string().optional(),
    image: z.string().optional(),
    imageAlt: z.string().optional(),
    tldr: z.array(z.string()).optional(),
    draft: z.boolean().default(false),
  }),
});

const outils = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/outils" }),
  schema: z.object({
    title: z.string(),
    description: z.string().max(160),
    outil: z.string(),
    category: z.string(),
    pricing: z.string(),
    website: z.string().optional(),
    rating: z.number().min(1).max(10).optional(),
    date: z.coerce.date(),
    lastReviewed: z.coerce.date().optional(),
    author: z.string().optional(),
    keywords: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

const actu = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/actu" }),
  schema: z.object({
    title: z.string(),
    description: z.string().max(260),
    date: z.coerce.date(),
    category: z.enum(["menace", "etude", "annonce", "politique", "outil", "voix", "chiffre"]),
    impactLevel: z.number().min(1).max(5),
    author: z.string().default("Adapte-toi Décrypte"),
    keyQuote: z.object({
      text: z.string(),
      author: z.string(),
      context: z.string().optional(),
    }).optional(),
    tldr: z.array(z.string()).min(2).max(5),
    sources: z.array(z.object({
      title: z.string(),
      url: z.string().url(),
      outlet: z.string(),
      date: z.coerce.date().optional(),
    })).min(1),
    relatedMetiers: z.array(z.string()).default([]),
    relatedGuides: z.array(z.string()).default([]),
    relatedOutils: z.array(z.string()).default([]),
    image: z.string().optional(),
    imageAlt: z.string().optional(),
    keywords: z.string().optional(),
    lastReviewed: z.coerce.date().optional(),
    reviewedBy: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog, pages, metiers, guides, outils, actu };
