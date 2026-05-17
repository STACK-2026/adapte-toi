import { siteConfig } from "../../site.config";

export { siteConfig };

/** Full URL for a path. Adds trailing slash for HTML pages (matching Astro
 *  trailingSlash: "always"), but leaves asset files (with extension) and
 *  fragment/query-bearing URLs untouched so anchors and asset filenames
 *  are preserved. */
export function fullUrl(path: string): string {
  const base = siteConfig.url.replace(/\/$/, "");
  const clean = path.startsWith("/") ? path : `/${path}`;
  // If the path carries a fragment, a query string, or looks like a static
  // asset (`.png`, `.jpg`, `.xml`, `.txt`, `.pdf`, `.json`, `.svg`, …),
  // emit it verbatim — never append a trailing slash to those.
  const isAssetOrAnchor = /[#?]/.test(clean) || /\.[a-z0-9]{2,5}$/i.test(clean);
  if (isAssetOrAnchor) return `${base}${clean}`;
  const withSlash = clean.endsWith("/") ? clean : `${clean}/`;
  return `${base}${withSlash}`;
}

/** Get Google Fonts URL */
export function fontsUrl(): string {
  const display = siteConfig.fonts.display.replace(/ /g, "+");
  const body = siteConfig.fonts.body.replace(/ /g, "+");
  return `https://fonts.googleapis.com/css2?family=${display}:wght@600;700;800&family=${body}:wght@400;500;600&display=swap`;
}
