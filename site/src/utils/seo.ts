import { siteConfig, fullUrl } from "./config";

const policies = siteConfig.policies ?? {};
const socialLinks = (siteConfig.socialLinks ?? []).filter(Boolean);
const knowsAbout = siteConfig.media?.knowsAbout ?? [];

/** JSON-LD for the publishing entity (NewsMediaOrganization).
 *  Used on the homepage and as `publisher` on every Article/NewsArticle.
 *  Includes the governance signals Google Publisher Center looks for:
 *  publishingPrinciples, ethicsPolicy, correctionsPolicy, ownership/funding,
 *  diversity, unnamed sources. */
export function jsonLdNewsMediaOrganization() {
  const founder = siteConfig.founder;
  return {
    "@context": "https://schema.org",
    "@type": "NewsMediaOrganization",
    "@id": `${siteConfig.url}#publisher`,
    name: siteConfig.name,
    legalName: siteConfig.legal.companyName || siteConfig.name,
    url: siteConfig.url,
    logo: {
      "@type": "ImageObject",
      url: fullUrl("/og-default.png"),
      width: 1200,
      height: 630,
    },
    description: siteConfig.description,
    slogan: siteConfig.tagline,
    inLanguage: siteConfig.locale,
    ...(founder?.foundingDate && { foundingDate: founder.foundingDate }),
    ...(founder?.founderName && {
      founder: {
        "@type": "Person",
        name: founder.founderName,
      },
    }),
    ...(siteConfig.legal.email && {
      contactPoint: {
        "@type": "ContactPoint",
        email: siteConfig.legal.email,
        contactType: "editorial",
        availableLanguage: ["French"],
      },
    }),
    ...(socialLinks.length && { sameAs: socialLinks }),
    ...(knowsAbout.length && { knowsAbout }),
    ...(policies.publishing && {
      publishingPrinciples: fullUrl(policies.publishing),
    }),
    ...(policies.ethics && { ethicsPolicy: fullUrl(policies.ethics) }),
    ...(policies.corrections && {
      correctionsPolicy: fullUrl(policies.corrections),
    }),
    ...(policies.feedback && {
      actionableFeedbackPolicy: fullUrl(policies.feedback),
    }),
    ...(policies.diversity && {
      diversityPolicy: fullUrl(policies.diversity),
    }),
    ...(policies.unnamedSources && {
      unnamedSourcesPolicy: fullUrl(policies.unnamedSources),
    }),
    ...(policies.funding && {
      ownershipFundingInfo: fullUrl(policies.funding),
    }),
    ...(policies.masthead && {
      masthead: fullUrl(policies.masthead),
    }),
  };
}

/** Lightweight reference to the publisher entity by @id.
 *  Use inside articles to avoid duplicating the full NewsMediaOrganization. */
export function publisherRef() {
  return {
    "@type": "NewsMediaOrganization",
    "@id": `${siteConfig.url}#publisher`,
    name: siteConfig.name,
    url: siteConfig.url,
    logo: {
      "@type": "ImageObject",
      url: fullUrl("/og-default.png"),
    },
  };
}

/** JSON-LD for the homepage: NewsMediaOrganization + WebSite + FAQPage (if FAQ).
 *  The Organization-type entity here means BaseLayout MUST NOT inject another. */
export function jsonLdHomepage(opts?: {
  faq?: Array<{ question: string; answer: string }>;
}) {
  const blocks: object[] = [
    jsonLdNewsMediaOrganization(),
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "@id": `${siteConfig.url}#website`,
      name: siteConfig.name,
      url: siteConfig.url,
      description: siteConfig.tagline,
      inLanguage: siteConfig.locale,
      publisher: { "@id": `${siteConfig.url}#publisher` },
      potentialAction: {
        "@type": "SearchAction",
        target: {
          "@type": "EntryPoint",
          urlTemplate: `${siteConfig.url}/blog?q={search_term_string}`,
        },
        "query-input": "required name=search_term_string",
      },
    },
  ];
  if (opts?.faq?.length) {
    blocks.push(jsonLdFaq(opts.faq));
  }
  return blocks;
}

/** Internal helper: resolve an author value into a schema.org author node.
 *  Collective signatures ("La Rédaction Adapte-toi", "Adapte-toi Décrypte",
 *  "Rédaction Adapte-toi") map to the publishing Organization entity, NOT
 *  a Person. This matches the editorial decision to publish under a single
 *  collective brand. Individual names, if any, still resolve to Person. */
function resolveAuthorNode(authorName?: string) {
  const name = (authorName || siteConfig.blog.defaultAuthor || "").trim();
  const collectivePatterns = [
    /^la\s+r[eé]daction\s+adapte-toi$/i,
    /^r[eé]daction\s+adapte-toi$/i,
    /^adapte-toi(\s+d[eé]crypte)?$/i,
    /^équipe\s+adapte-toi$/i,
    /^equipe\s+adapte-toi$/i,
  ];
  if (!name || collectivePatterns.some((re) => re.test(name))) {
    return {
      "@type": "NewsMediaOrganization",
      "@id": `${siteConfig.url}#publisher`,
      name: siteConfig.name,
      url: siteConfig.url,
    };
  }
  return {
    "@type": "Person",
    name,
  };
}

/** Google requires Article/NewsArticle `headline` ≤110 chars for rich-result
 * eligibility. We cap on a word boundary; the visible <h1>/<title> keep the full title. */
function clampHeadline(title: string): string {
  if (title.length <= 110) return title;
  const cut = title.slice(0, 110);
  const lastSpace = cut.lastIndexOf(" ");
  return (lastSpace > 60 ? cut.slice(0, lastSpace) : cut).trimEnd();
}

/** JSON-LD for a generic Article (guides, blog, fiches métier). */
export function jsonLdArticle(article: {
  title: string;
  description: string;
  url: string;
  datePublished: string;
  dateModified?: string;
  image?: string;
  author?: string;
  keywords?: string[];
}) {
  return {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: clampHeadline(article.title),
    description: article.description,
    url: article.url,
    datePublished: article.datePublished,
    dateModified: article.dateModified || article.datePublished,
    image: article.image
      ? article.image.startsWith("http")
        ? article.image
        : fullUrl(article.image)
      : undefined,
    author: resolveAuthorNode(article.author),
    publisher: publisherRef(),
    mainEntityOfPage: { "@type": "WebPage", "@id": article.url },
    keywords: article.keywords?.join(", "),
    inLanguage: siteConfig.locale,
    isAccessibleForFree: true,
    speakable: {
      "@type": "SpeakableSpecification",
      cssSelector: ["h1", "h2", "[data-speakable]"],
    },
  };
}

/** JSON-LD for NewsArticle (used on /actu/ entries, Google News-eligible). */
export function jsonLdNewsArticle(article: {
  title: string;
  description: string;
  url: string;
  datePublished: string;
  dateModified?: string;
  image?: string;
  author?: string;
  keywords?: string[];
  section?: string;
  articleBody?: string;
}) {
  return {
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    headline: clampHeadline(article.title),
    description: article.description,
    url: article.url,
    datePublished: article.datePublished,
    dateModified: article.dateModified || article.datePublished,
    image: article.image
      ? article.image.startsWith("http")
        ? article.image
        : fullUrl(article.image)
      : undefined,
    author: resolveAuthorNode(article.author),
    publisher: publisherRef(),
    mainEntityOfPage: { "@type": "WebPage", "@id": article.url },
    ...(article.section && { articleSection: article.section }),
    ...(article.keywords && { keywords: article.keywords.join(", ") }),
    inLanguage: siteConfig.locale,
    isAccessibleForFree: true,
    speakable: {
      "@type": "SpeakableSpecification",
      cssSelector: ["h1", "h2", "[data-speakable]"],
    },
  };
}

/** Extract FAQ Q&A pairs from a raw markdown body.
 *  Recognises two styles inside a `## FAQ` (or equivalent) section:
 *  - Style 1: questions as h3 headings (### Question)
 *  - Style 2: questions as bold paragraphs (**Question ?**)
 *  Returns an empty array when no ## FAQ section is found. */
export function extractFaqFromMarkdown(
  md: string | undefined
): Array<{ question: string; answer: string }> {
  if (!md) return [];
  const m = md.match(
    /^##\s+(FAQ|Foire aux questions|Questions fr[ée]quentes)[^\n]*$/im
  );
  if (!m || m.index === undefined) return [];
  let section = md.slice(m.index + m[0].length);
  const nextH2 = section.match(/^##\s+/m);
  if (nextH2 && nextH2.index !== undefined)
    section = section.slice(0, nextH2.index);

  const clean = (s: string) =>
    s
      .replace(/\*\*/g, "")
      .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
      .replace(/\s+/g, " ")
      .trim();

  const pairs: Array<{ question: string; answer: string }> = [];

  // Style 1: questions as h3 headings (### Question)
  const reH3 = /^###\s+([^\n]+)\n+([\s\S]*?)(?=^###\s+|$)/gm;
  let m2: RegExpExecArray | null;
  while ((m2 = reH3.exec(section)) !== null) {
    const question = m2[1]
      .replace(/\s*\{#[^}]+\}\s*$/, "")
      .replace(/\*\*/g, "")
      .trim();
    const answer = clean(m2[2]);
    if (question && answer) pairs.push({ question, answer });
  }

  // Style 2 (fallback): questions as bold paragraphs (**Question ?**)
  if (pairs.length === 0) {
    const reBold =
      /^\*\*(.+?\?)\*\*\s*$\n+([\s\S]*?)(?=^\*\*.+?\?\*\*\s*$|^##\s+|$)/gm;
    let m3: RegExpExecArray | null;
    while ((m3 = reBold.exec(section)) !== null) {
      const question = m3[1].replace(/\*\*/g, "").trim();
      const answer = clean(m3[2]);
      if (question && answer) pairs.push({ question, answer });
    }
  }

  return pairs;
}

/** JSON-LD for FAQPage */
export function jsonLdFaq(
  faq: Array<{ question: string; answer: string }>
) {
  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: faq.map((item) => ({
      "@type": "Question",
      name: item.question,
      acceptedAnswer: {
        "@type": "Answer",
        text: item.answer,
      },
    })),
  };
}

/** JSON-LD for BreadcrumbList */
export function jsonLdBreadcrumbs(
  items: Array<{ name: string; url: string }>
) {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: items.map((item, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: item.name,
      item: item.url,
    })),
  };
}

/** JSON-LD for SoftwareApplication (used on outils/ pages and comparators) */
export function jsonLdSoftwareApplication(app: {
  name: string;
  description: string;
  url: string;
  applicationCategory?: string;
  operatingSystem?: string;
  offerPriceCurrency?: string;
  offerPrice?: string;
  ratingValue?: number;
  ratingCount?: number;
  reviewedAt?: string;
}) {
  const node: Record<string, unknown> = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    name: app.name,
    description: app.description,
    url: app.url,
    applicationCategory: app.applicationCategory || "BusinessApplication",
    operatingSystem: app.operatingSystem || "Web, iOS, Android",
  };
  if (app.offerPrice !== undefined) {
    node.offers = {
      "@type": "Offer",
      price: app.offerPrice,
      priceCurrency: app.offerPriceCurrency || "EUR",
    };
  }
  if (app.ratingValue && app.ratingCount) {
    node.aggregateRating = {
      "@type": "AggregateRating",
      ratingValue: app.ratingValue.toFixed(1),
      bestRating: "10",
      worstRating: "1",
      ratingCount: app.ratingCount,
    };
  }
  if (app.reviewedAt) {
    node.dateModified = app.reviewedAt;
  }
  return node;
}

/** JSON-LD ItemList (comparators, top-N curations) */
export function jsonLdItemList(list: {
  name: string;
  description?: string;
  url: string;
  items: Array<{ name: string; url: string; description?: string }>;
}) {
  return {
    "@context": "https://schema.org",
    "@type": "ItemList",
    name: list.name,
    description: list.description,
    url: list.url,
    numberOfItems: list.items.length,
    itemListElement: list.items.map((item, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: item.name,
      url: item.url,
      ...(item.description && { description: item.description }),
    })),
  };
}

/** JSON-LD HowTo (used on /guides/ step-by-step articles).
 *  steps: ordered list of action items. */
export function jsonLdHowTo(howto: {
  name: string;
  description: string;
  url: string;
  totalTime?: string; // ISO 8601 duration e.g. "PT3H"
  estimatedCost?: { currency: string; value: string };
  steps: Array<{ name: string; text: string; url?: string; image?: string }>;
}) {
  return {
    "@context": "https://schema.org",
    "@type": "HowTo",
    name: howto.name,
    description: howto.description,
    url: howto.url,
    ...(howto.totalTime && { totalTime: howto.totalTime }),
    ...(howto.estimatedCost && {
      estimatedCost: {
        "@type": "MonetaryAmount",
        currency: howto.estimatedCost.currency,
        value: howto.estimatedCost.value,
      },
    }),
    step: howto.steps.map((s, i) => ({
      "@type": "HowToStep",
      position: i + 1,
      name: s.name,
      text: s.text,
      ...(s.url && { url: s.url }),
      ...(s.image && {
        image: s.image.startsWith("http") ? s.image : fullUrl(s.image),
      }),
    })),
  };
}

/** JSON-LD OccupationalCategory + Occupation summary for /metiers/ pages.
 *  Helps Google connect the fiche to ESCO/O*NET-style entities and may
 *  surface enriched "career/job" knowledge panels in AI Overviews. */
export function jsonLdOccupation(o: {
  name: string; // e.g. "Avocat"
  description: string;
  url: string;
  category?: string; // ROME / ESCO ID if known
  responsibilities?: string[];
  skills?: string[];
  estimatedSalary?: {
    currency: string;
    minValue: number;
    maxValue: number;
    unitText?: "YEAR" | "MONTH";
  };
  occupationLocation?: string; // e.g. "France"
}) {
  return {
    "@context": "https://schema.org",
    "@type": "Occupation",
    name: o.name,
    description: o.description,
    url: o.url,
    ...(o.category && { occupationalCategory: o.category }),
    ...(o.responsibilities?.length && {
      responsibilities: o.responsibilities,
    }),
    ...(o.skills?.length && { skills: o.skills.join(", ") }),
    ...(o.estimatedSalary && {
      estimatedSalary: {
        "@type": "MonetaryAmountDistribution",
        currency: o.estimatedSalary.currency,
        minValue: o.estimatedSalary.minValue,
        maxValue: o.estimatedSalary.maxValue,
        ...(o.estimatedSalary.unitText && {
          unitText: o.estimatedSalary.unitText,
        }),
      },
    }),
    ...(o.occupationLocation && {
      occupationLocation: {
        "@type": "Country",
        name: o.occupationLocation,
      },
    }),
  };
}
