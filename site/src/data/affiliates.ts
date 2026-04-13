/**
 * Programmes d'affiliation - données
 * Remplacer les URLs par les liens affiliés quand les comptes sont créés
 * Format : slug de la fiche outil -> infos affiliation
 */

export const affiliates: Record<string, {
  url: string;
  commission: string;
  cookie: string;
  cta: string;
  note?: string;
}> = {
  "make": {
    url: "https://www.make.com/en/register?promo=adaptetoi", // TODO: remplacer par lien affilié
    commission: "35% récurrent pendant 12 mois",
    cookie: "—",
    cta: "Essayer Make.com gratuitement",
    note: "1 000 opérations gratuites par mois",
  },
  "jasper": {
    url: "https://www.jasper.ai/free-trial", // TODO: remplacer par lien affilié FirstPromoter
    commission: "25-30% récurrent pendant 12 mois",
    cookie: "45 jours",
    cta: "Essayer Jasper gratuitement",
    note: "7 jours d'essai gratuit",
  },
  "surfer-seo": {
    url: "https://surferseo.com/", // TODO: remplacer par lien affilié PartnerStack
    commission: "15-25% récurrent",
    cookie: "60 jours",
    cta: "Essayer Surfer SEO",
    note: "Essai gratuit disponible",
  },
  "copy-ai": {
    url: "https://www.copy.ai/", // TODO: remplacer par lien affilié
    commission: "45% récurrent pendant 12 mois",
    cookie: "60 jours",
    cta: "Essayer Copy.ai gratuitement",
    note: "2 000 mots gratuits par mois",
  },
  "writesonic": {
    url: "https://writesonic.com/", // TODO: remplacer par lien affilié
    commission: "30% récurrent",
    cookie: "30 jours",
    cta: "Essayer Writesonic gratuitement",
    note: "10 000 mots offerts",
  },
  "hubspot": {
    url: "https://www.hubspot.com/products/get-started", // TODO: remplacer par lien affilié
    commission: "30% récurrent pendant 12 mois",
    cookie: "180 jours",
    cta: "Créer un compte HubSpot gratuit",
    note: "CRM gratuit à vie, pas de carte requise",
  },
  "canva-ai": {
    url: "https://www.canva.com/", // TODO: remplacer par lien affilié
    commission: "Programme actif (variable)",
    cookie: "30 jours",
    cta: "Essayer Canva gratuitement",
    note: "Version gratuite très généreuse",
  },
  "notion-ai": {
    url: "https://www.notion.so/", // TODO: vérifier programme affilié
    commission: "Programme en attente",
    cookie: "—",
    cta: "Essayer Notion gratuitement",
  },
};
