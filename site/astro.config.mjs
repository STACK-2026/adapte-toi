// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import tailwindcss from "@tailwindcss/vite";

import { siteConfig } from "./site.config.ts";

export default defineConfig({
  site: siteConfig.url,
  integrations: [
    sitemap({
      lastmod: new Date(),
      changefreq: "weekly",
      priority: 0.7,
      serialize(item) {
        // Homepage
        if (item.url === siteConfig.url + "/") {
          item.priority = 1.0;
          item.changefreq = "daily";
        }
        // Blog articles
        if (item.url.includes("/blog/")) {
          item.priority = 0.8;
          item.changefreq = "weekly";
        }
        // Fiches metier
        if (item.url.includes("/metiers/")) {
          item.priority = 0.9;
          item.changefreq = "monthly";
        }
        // Guides
        if (item.url.includes("/guides/")) {
          item.priority = 0.85;
          item.changefreq = "monthly";
        }
        // Outils
        if (item.url.includes("/outils/")) {
          item.priority = 0.8;
          item.changefreq = "monthly";
        }
        return item;
      },
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
  markdown: {
    smartypants: false,
    shikiConfig: {
      theme: "github-light",
    },
  },
});
