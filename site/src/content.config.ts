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

export const collections = { blog, pages, metiers };
