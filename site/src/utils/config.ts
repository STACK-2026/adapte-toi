import { siteConfig } from "../../site.config";

export { siteConfig };

/** Keep search-result titles concise without changing the visible H1 or the
 * social headline. When a title carries the site-name suffix, preserve it and
 * shorten only the editorial portion on a word boundary. */
export function searchTitle(title: string, maxLength = 70): string {
  if (title.length <= maxLength) return title;

  const suffix = ` | ${siteConfig.name}`;
  const hasSuffix = title.endsWith(suffix);
  const base = hasSuffix ? title.slice(0, -suffix.length) : title;
  const available = maxLength - (hasSuffix ? suffix.length : 0);
  const rawCut = base.slice(0, available + 1);
  const boundary = rawCut.lastIndexOf(" ");
  const cut = (boundary >= Math.floor(available * 0.65)
    ? rawCut.slice(0, boundary)
    : base.slice(0, available)
  ).replace(/[\s,;:!?()[\]-]+$/g, "");

  return `${cut}${hasSuffix ? suffix : ""}`;
}

/** Full URL for a path. Adds trailing slash for HTML pages (matching Astro
 *  trailingSlash: "always"), but leaves asset files (with extension) and
 *  fragment/query-bearing URLs untouched so anchors and asset filenames
 *  are preserved. */
export function fullUrl(path: string): string {
  const base = siteConfig.url.replace(/\/$/, "");
  const clean = path.startsWith("/") ? path : `/${path}`;
  // If the path carries a fragment, a query string, or looks like a static
  // asset (`.png`, `.jpg`, `.xml`, `.txt`, `.pdf`, `.json`, `.svg`, …),
  // emit it verbatim; never append a trailing slash to those.
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
