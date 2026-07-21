// ============================================
// SITE CONFIG - adapte-toi.com
// Media éditorial indépendant : reconversion professionnelle x IA
// ============================================

export const siteConfig = {
  // Identite
  name: "Adapte-toi",
  tagline: "Le média qui te prépare au monde du travail de demain",
  description:
    "Adapte-toi est le média francophone de référence sur la reconversion professionnelle à l'ère de l'intelligence artificielle. Guides, fiches métier, outils, témoignages : tout pour comprendre l'impact de l'IA sur ton emploi et agir avant qu'il ne soit trop tard.",
  url: "https://adapte-toi.com",
  appUrl: "", // pas d'app separee, outils intégrés dans le site
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
  ogImage: "/og-default.png",
  keywords: [
    "reconversion professionnelle IA",
    "métiers menacés intelligence artificielle",
    "formation IA",
    "emploi IA 2026",
    "impact IA travail",
    "reconversion IA France",
    "outils IA par métier",
    "se former à l'IA",
  ],

  // GEO (Generative Engine Optimization)
  llmsDescription:
    "Adapte-toi.com est le premier média francophone indépendant dédié à la reconversion professionnelle à l'ère de l'intelligence artificielle. Il propose des fiches métier analysant l'impact de l'IA, des guides pratiques de reconversion, un annuaire d'outils IA par profession, et des articles d'actualité sur les mutations du marché du travail. Adapte-toi ne vend pas de formation : il informe, il outille, il dit la vérité.",

  // Navigation
  navLinks: [
    { label: "Métiers", href: "/metiers/" },
    { label: "Diagnostic", href: "/diagnostic/" },
    { label: "Guides", href: "/guides/" },
    { label: "Outils IA", href: "/outils/" },
    { label: "Actu", href: "/actu/" },
    { label: "Baromètre", href: "/barometre/" },
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
      question: "L'IA va-t-elle vraiment remplacer mon métier ?",
      answer:
        "Ça dépend du métier. Selon l'étude Anthropic de mars 2026, les centres d'appels ont perdu 67% de leurs offres d'emploi, la rédaction publicitaire 53%, et la gestion de projets 48%. En revanche, les métiers manuels, créatifs et relationnels sont peu impactés. Consulte nos fiches métier pour connaître l'impact précis sur ta profession.",
    },
    {
      question: "Adapte-toi est-il un organisme de formation ?",
      answer:
        "Non. Adapte-toi est un media éditorial indépendant. On ne vend aucune formation. On informe, on analyse, on outille. Quand on recommande une formation, c'est en toute transparence, avec un avis honnête et sans conflit d'intérêt caché.",
    },
    {
      question: "Comment savoir si je dois me reconvertir ou me former ?",
      answer:
        "Utilise notre outil de diagnostic gratuit : en quelques minutes, tu obtiens une analyse personnalisée de l'impact de l'IA sur ton métier, avec des recommandations concrètes. Formation complémentaire, pivot de carrière, ou montée en compétences : on t'aide à y voir clair.",
    },
    {
      question: "Quels sont les métiers les plus menacés par l'IA en 2026 ?",
      answer:
        "Les métiers les plus exposés sont les métiers intellectuels répétitifs : comptabilité, traduction, support client, rédaction marketing, gestion de projets, saisie de données. Les métiers les plus résilients combinent créativité, relations humaines et compétences physiques.",
    },
    {
      question: "Est-ce qu'il faut savoir coder pour se reconvertir dans l'IA ?",
      answer:
        "Non. La majorité des métiers liés à l'IA ne demandent pas de savoir coder. Prompt engineering, automatisation no-code avec Make ou Zapier, utilisation avancée de ChatGPT ou Claude : tu peux devenir opérationnel en quelques semaines. Nos guides t'expliquent comment.",
    },
    {
      question: "Tes sources sont-elles fiables ?",
      answer:
        "Toutes nos analyses s'appuient sur des études publiées par des institutions reconnues : OCDE, McKinsey, Anthropic, FMI, INSEE, France Travail, PwC, Cognizant. Chaque chiffre est sourcé et vérifiable. On ne fait pas dans le sensationnalisme.",
    },
  ],

  // Features/avantages
  features: [
    {
      title: "Fiches métier IA",
      description:
        "Analyse détaillée de l'impact de l'IA sur 50+ métiers. Ce qui change, ce qui reste, les compétences a acquérir, le plan d'action concret.",
      icon: "users",
    },
    {
      title: "Guides pratiques",
      description:
        "Des guides complets de 3 000+ mots pour te reconvertir, te former, ou booster ta productivité avec l'IA. Zéro bullshit, que du concret.",
      icon: "chart",
    },
    {
      title: "Annuaire d'outils IA",
      description:
        "Les meilleurs outils IA classés par métier et par usage. Tests, comparatifs, tutoriels. Pour savoir exactement quoi utiliser dans ta situation.",
      icon: "search",
    },
    {
      title: "Veille hebdomadaire",
      description:
        "Chaque semaine, le résumé des actualités IA qui impactent le marché de l'emploi. Les études, les chiffres, les tendances. En 5 minutes.",
      icon: "zap",
    },
    {
      title: "Diagnostic personnalisé",
      description:
        "Un outil interactif qui analyse ton métier, ton expérience et tes compétences pour te donner des recommandations sur mesure face à l'IA.",
      icon: "shield",
    },
    {
      title: "Baromètre mensuel",
      description:
        "Chaque mois, nos indicateurs propriétaires : indice d'exposition IA France, tendances offres d'emploi, métiers résilients. Données libres de citation.",
      icon: "star",
    },
  ],

  // Blog auto pipeline
  blog: {
    enabled: true,
    name: "Le Signal",
    postsPerPage: 12,
    // Signature collective : tous les contenus sont signés au nom de la
    // rédaction. Décision éditoriale (mai 2026) pour éviter les pen names
    // individuels et porter une voix de média plutôt que de personnalités.
    defaultAuthor: "La Rédaction Adapte-toi",
    catégories: [
      "reconversion",
      "métiers-ia",
      "formation",
      "outils-ia",
      "actu-emploi",
      "témoignages",
      "freelance-ia",
      "études-rapports",
    ],
    editorialBoard: [],
  },

  // Identité & gouvernance éditoriale (utilisée par NewsMediaOrganization).
  // Décommenter founderName si tu acceptes l'attribution publique du
  // fondateur dans le schéma JSON-LD (signal E-E-A-T plus fort pour Google
  // mais expose ton identité dans Knowledge Graph / Publisher Center).
  founder: {
    // founderName: "Augustin Foucheres",
    foundingDate: "2026-04",
  },

  // URLs des pages de politique éditoriale.
  // Ces pages sont obligatoires pour Google Publisher Center et
  // pour le schéma NewsMediaOrganization.
  policies: {
    publishing: "/politique-editoriale/",
    ethics: "/charte-editoriale/",
    corrections: "/politique-de-correction/",
    feedback: "/a-propos/",
    diversity: "/charte-editoriale/#diversite",
    unnamedSources: "/charte-editoriale/#sources-anonymes",
    funding: "/sources-financement/",
    masthead: "/a-propos/",
  },

  // Liens sociaux pour sameAs (autorité)
  socialLinks: [
    // "https://x.com/adaptetoi",
    // "https://linkedin.com/company/adapte-toi",
    // "https://www.youtube.com/@adapte-toi",
  ],

  // Pour knowsAbout (signal sémantique au knowledge graph)
  media: {
    knowsAbout: [
      "Reconversion professionnelle",
      "Intelligence artificielle",
      "Marché du travail",
      "Formation professionnelle",
      "Métiers menacés par l'IA",
      "Compte personnel de formation",
      "ChatGPT",
      "Claude",
      "Outils IA",
      "Anthropic Economic Index",
      "OCDE emploi",
      "France Travail",
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
