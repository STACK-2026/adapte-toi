// ============================================
// SITE CONFIG - adapte-toi.com
// Media editorial independant : reconversion professionnelle x IA
// ============================================

export const siteConfig = {
  // Identite
  name: "Adapte-toi",
  tagline: "Le media qui te prepare au monde du travail de demain",
  description:
    "Adapte-toi est le media francophone de reference sur la reconversion professionnelle a l'ere de l'intelligence artificielle. Guides, fiches metier, outils, temoignages : tout pour comprendre l'impact de l'IA sur ton emploi et agir avant qu'il ne soit trop tard.",
  url: "https://adapte-toi.com",
  appUrl: "", // pas d'app separee, outils integres dans le site
  locale: "fr-FR",
  language: "fr",

  // Branding
  colors: {
    primary: "#E63946", // rouge signal - urgence, attention, "adapte-toi maintenant"
    secondary: "#1D3557", // bleu marine - confiance, autorite, serieux media
    accent: "#F77F00", // orange vif - energie, transformation, opportunite
    background: "#FAFBFC", // blanc casse - lisibilite longue lecture
    text: "#1A1A2E", // quasi-noir - contraste max
  },

  // Typographie (Google Fonts)
  fonts: {
    display: "Space Grotesk", // moderne, tech, distinctive, pas "AI slop"
    body: "DM Sans", // lisible, neutre, parfait pour longs articles
  },

  // SEO
  author: "Adapte-toi",
  twitterHandle: "",
  ogImage: "/og-default.svg",
  keywords: [
    "reconversion professionnelle IA",
    "metiers menaces intelligence artificielle",
    "formation IA",
    "emploi IA 2026",
    "impact IA travail",
    "reconversion IA France",
    "outils IA par metier",
    "se former a l'IA",
  ],

  // GEO (Generative Engine Optimization)
  llmsDescription:
    "Adapte-toi.com est le premier media francophone independant dedie a la reconversion professionnelle a l'ere de l'intelligence artificielle. Il propose des fiches metier analysant l'impact de l'IA, des guides pratiques de reconversion, un annuaire d'outils IA par profession, et des articles d'actualite sur les mutations du marche du travail. Adapte-toi ne vend pas de formation : il informe, il outille, il dit la verite.",

  // Navigation
  navLinks: [
    { label: "Metiers", href: "/metiers" },
    { label: "Guides", href: "/guides" },
    { label: "Outils IA", href: "/outils" },
    { label: "Actu", href: "/actu" },
    { label: "Temoignages", href: "/temoignages" },
    { label: "Le Signal", href: "/blog" },
    { label: "A propos", href: "/a-propos" },
  ],

  // Sections landing page
  sections: {
    hero: true,
    problem: true,
    stats: true,
    features: true,
    metiers: true,
    howItWorks: true,
    testimonials: true,
    blogPreview: true,
    newsletter: true,
    faq: true,
    cta: true,
  },

  // FAQ (landing + schema FAQPage)
  faq: [
    {
      question: "L'IA va-t-elle vraiment remplacer mon metier ?",
      answer:
        "Ca depend du metier. Selon l'etude Anthropic de mars 2026, les centres d'appels ont perdu 67% de leurs offres d'emploi, la redaction publicitaire 53%, et la gestion de projets 48%. En revanche, les metiers manuels, creatifs et relationnels sont peu impactes. Consulte nos fiches metier pour connaitre l'impact precis sur ta profession.",
    },
    {
      question: "Adapte-toi est-il un organisme de formation ?",
      answer:
        "Non. Adapte-toi est un media editorial independant. On ne vend aucune formation. On informe, on analyse, on outille. Quand on recommande une formation, c'est en toute transparence, avec un avis honnete et sans conflit d'interet cache.",
    },
    {
      question: "Comment savoir si je dois me reconvertir ou me former ?",
      answer:
        "Utilise notre outil de diagnostic gratuit : en quelques minutes, tu obtiens une analyse personnalisee de l'impact de l'IA sur ton metier, avec des recommandations concretes. Formation complementaire, pivot de carriere, ou montee en competences : on t'aide a y voir clair.",
    },
    {
      question: "Quels sont les metiers les plus menaces par l'IA en 2026 ?",
      answer:
        "Les metiers les plus exposes sont les metiers intellectuels repetitifs : comptabilite, traduction, support client, redaction marketing, gestion de projets, saisie de donnees. Les metiers les plus resilients combinent creativite, relations humaines et competences physiques.",
    },
    {
      question: "Est-ce qu'il faut savoir coder pour se reconvertir dans l'IA ?",
      answer:
        "Non. La majorite des metiers lies a l'IA ne demandent pas de savoir coder. Prompt engineering, automatisation no-code avec Make ou Zapier, utilisation avancee de ChatGPT ou Claude : tu peux devenir operationnel en quelques semaines. Nos guides t'expliquent comment.",
    },
    {
      question: "Tes sources sont-elles fiables ?",
      answer:
        "Toutes nos analyses s'appuient sur des etudes publiees par des institutions reconnues : OCDE, McKinsey, Anthropic, FMI, INSEE, France Travail, PwC, Cognizant. Chaque chiffre est source et verifiable. On ne fait pas dans le sensationnalisme.",
    },
  ],

  // Features/avantages
  features: [
    {
      title: "Fiches metier IA",
      description:
        "Analyse detaillee de l'impact de l'IA sur 50+ metiers. Ce qui change, ce qui reste, les competences a acquerir, le plan d'action concret.",
      icon: "users",
    },
    {
      title: "Guides pratiques",
      description:
        "Des guides complets de 3 000+ mots pour te reconvertir, te former, ou booster ta productivite avec l'IA. Zero bullshit, que du concret.",
      icon: "chart",
    },
    {
      title: "Annuaire d'outils IA",
      description:
        "Les meilleurs outils IA classes par metier et par usage. Tests, comparatifs, tutoriels. Pour savoir exactement quoi utiliser dans ta situation.",
      icon: "search",
    },
    {
      title: "Veille hebdomadaire",
      description:
        "Chaque semaine, le resume des actualites IA qui impactent le marche de l'emploi. Les etudes, les chiffres, les tendances. En 5 minutes.",
      icon: "zap",
    },
    {
      title: "Diagnostic personnalise",
      description:
        "Un outil interactif qui analyse ton metier, ton experience et tes competences pour te donner des recommandations sur mesure face a l'IA.",
      icon: "shield",
    },
    {
      title: "Temoignages reels",
      description:
        "Des histoires de reconversion reussies, des avant/apres par metier, des retours d'experience bruts. Pour voir que c'est possible.",
      icon: "star",
    },
  ],

  // Blog auto pipeline
  blog: {
    enabled: true,
    name: "Le Signal",
    postsPerPage: 12,
    defaultAuthor: "La redaction Adapte-toi",
    categories: [
      "reconversion",
      "metiers-ia",
      "formation",
      "outils-ia",
      "actu-emploi",
      "temoignages",
      "freelance-ia",
      "etudes-rapports",
    ],
    authors: [
      {
        name: "Camille Renard",
        role: "Journaliste emploi et reconversion",
        bio: "10 ans de veille sur les mutations du marche du travail. Ancienne RH reconvertie en journaliste specialisee.",
      },
      {
        name: "Theo Marchand",
        role: "Analyste IA et donnees emploi",
        bio: "Data analyst passionne par l'impact economique de l'IA. Decrypte les etudes et les chiffres pour les rendre accessibles.",
      },
      {
        name: "Sarah Bellamy",
        role: "Coach carriere et formatrice",
        bio: "Accompagne les actifs en reconversion depuis 8 ans. Specialisee dans les transitions vers les metiers du numerique.",
      },
    ],
  },

  // Legal
  legal: {
    companyName: "Adapte-toi",
    siret: "",
    address: "",
    email: "contact@adapte-toi.com",
    phone: "",
  },
};
