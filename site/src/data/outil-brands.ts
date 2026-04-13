/**
 * Données visuelles des outils IA
 * Couleurs brand, gradient, icône emoji, tagline courte
 */

export const outilBrands: Record<string, {
  gradient: string;
  textColor: string;
  svgPath?: string;
  logoFile?: string;
  tagline: string;
}> = {
  "chatgpt": {
    gradient: "linear-gradient(135deg, #10A37F, #0D8C6C)",
    textColor: "white",
    logoFile: "/logos/chatgpt.svg",
    tagline: "L'assistant IA le plus utilisé au monde",
  },
  "claude": {
    gradient: "linear-gradient(135deg, #D4A574, #B8860B)",
    textColor: "white",
    svgPath: "M17.3041 3.541h-3.6718l6.696 16.918H24Zm-10.6082 0L0 20.459h3.7442l1.3693-3.5527h7.0052l1.3693 3.5528h3.7442L10.5363 3.5409Zm-.3712 10.2232 2.2914-5.9456 2.2914 5.9456Z",
    tagline: "Le meilleur pour les textes longs et l'analyse",
  },
  "make": {
    gradient: "linear-gradient(135deg, #6B2FBE, #9B59B6)",
    textColor: "white",
    svgPath: "M13.38 3.498c-.27 0-.511.19-.566.465L9.85 18.986a.578.578 0 0 0 .453.678l4.095.826a.58.58 0 0 0 .682-.455l2.963-15.021a.578.578 0 0 0-.453-.678l-4.096-.826a.589.589 0 0 0-.113-.012zm-5.876.098a.576.576 0 0 0-.516.318L.062 17.697a.575.575 0 0 0 .256.774l3.733 1.877a.578.578 0 0 0 .775-.258l6.926-13.781a.577.577 0 0 0-.256-.776L7.762 3.658a.571.571 0 0 0-.258-.062zm11.74.115a.576.576 0 0 0-.576.576v15.426c0 .318.258.578.576.578h4.178a.58.58 0 0 0 .578-.578V4.287a.578.578 0 0 0-.578-.576Z",
    tagline: "Automatise ton travail sans coder",
  },
  "midjourney": {
    gradient: "linear-gradient(135deg, #1A1A2E, #16213E)",
    textColor: "white",
    logoFile: "/logos/midjourney.svg",
    tagline: "Génère des images professionnelles en 30 secondes",
  },
  "notion-ai": {
    gradient: "linear-gradient(135deg, #000000, #2D2D2D)",
    textColor: "white",
    svgPath: "M4.459 4.208c.746.606 1.026.56 2.428.466l13.215-.793c.28 0 .047-.28-.046-.326L17.86 1.968c-.42-.326-.981-.7-2.055-.607L3.01 2.295c-.466.046-.56.28-.374.466zm.793 3.08v13.904c0 .747.373 1.027 1.214.98l14.523-.84c.841-.046.935-.56.935-1.167V6.354c0-.606-.233-.933-.748-.887l-15.177.887c-.56.047-.747.327-.747.933zm14.337.745c.093.42 0 .84-.42.888l-.7.14v10.264c-.608.327-1.168.514-1.635.514-.748 0-.935-.234-1.495-.933l-4.577-7.186v6.952L12.21 19s0 .84-1.168.84l-3.222.186c-.093-.186 0-.653.327-.746l.84-.233V9.854L7.822 9.76c-.094-.42.14-1.026.793-1.073l3.456-.233 4.764 7.279v-6.44l-1.215-.139c-.093-.514.28-.887.747-.933zM1.936 1.035l13.31-.98c1.634-.14 2.055-.047 3.082.7l4.249 2.986c.7.513.934.653.934 1.213v16.378c0 1.026-.373 1.634-1.68 1.726l-15.458.934c-.98.047-1.448-.093-1.962-.747l-3.129-4.06c-.56-.747-.793-1.306-.793-1.96V2.667c0-.839.374-1.54 1.447-1.632z",
    tagline: "Organise ton travail et rédige 3x plus vite",
  },
  "canva-ai": {
    gradient: "linear-gradient(135deg, #00C4CC, #7B2FF7)",
    textColor: "white",
    logoFile: "/logos/canva.svg",
    tagline: "Crée des visuels pro sans être graphiste",
  },
  "perplexity": {
    gradient: "linear-gradient(135deg, #20808D, #1B6B75)",
    textColor: "white",
    svgPath: "M22.3977 7.0896h-2.3106V.0676l-7.5094 6.3542V.1577h-1.1554v6.1966L4.4904 0v7.0896H1.6023v10.3976h2.8882V24l6.932-6.3591v6.2005h1.1554v-6.0469l6.9318 6.1807v-6.4879h2.8882V7.0896zm-3.4657-4.531v4.531h-5.355l5.355-4.531zm-13.2862.0676 4.8691 4.4634H5.6458V2.6262zM2.7576 16.332V8.245h7.8476l-6.1149 6.1147v1.9723H2.7576zm2.8882 5.0404v-3.8852h.0001v-2.6488l5.7763-5.7764v7.0111l-5.7764 5.2993zm12.7086.0248-5.7766-5.1509V9.0618l5.7766 5.7766v6.5588zm2.8882-5.0652h-1.733v-1.9723L13.3948 8.245h7.8478v8.087z",
    tagline: "La recherche Google augmentée par l'IA",
  },
  "cursor": {
    gradient: "linear-gradient(135deg, #000000, #1A1A2E)",
    textColor: "white",
    svgPath: "M11.503.131 1.891 5.678a.84.84 0 0 0-.42.726v11.188c0 .3.162.575.42.724l9.609 5.55a1 1 0 0 0 .998 0l9.61-5.55a.84.84 0 0 0 .42-.724V6.404a.84.84 0 0 0-.42-.726L12.497.131a1.01 1.01 0 0 0-.996 0M2.657 6.338h18.55c.263 0 .43.287.297.515L12.23 22.918c-.062.107-.229.064-.229-.06V12.335a.59.59 0 0 0-.295-.51l-9.11-5.257c-.109-.063-.064-.23.061-.23",
    tagline: "L'éditeur de code qui écrit à ta place",
  },
  "surfer-seo": {
    gradient: "linear-gradient(135deg, #FF6B35, #F7931E)",
    textColor: "white",
    logoFile: "/logos/surfer.svg",
    tagline: "Optimise ton contenu pour Google avec l'IA",
  },
  "hubspot": {
    gradient: "linear-gradient(135deg, #FF7A59, #FF5C35)",
    textColor: "white",
    svgPath: "M18.164 7.93V5.084a2.198 2.198 0 001.267-1.978v-.067A2.2 2.2 0 0017.238.845h-.067a2.2 2.2 0 00-2.193 2.193v.067a2.196 2.196 0 001.252 1.973l.013.006v2.852a6.22 6.22 0 00-2.969 1.31l.012-.01-7.828-6.095A2.497 2.497 0 104.3 4.656l-.012.006 7.697 5.991a6.176 6.176 0 00-1.038 3.446c0 1.343.425 2.588 1.147 3.607l-.013-.02-2.342 2.343a1.968 1.968 0 00-.58-.095h-.002a2.033 2.033 0 102.033 2.033 1.978 1.978 0 00-.1-.595l.005.014 2.317-2.317a6.247 6.247 0 104.782-11.134l-.036-.005zm-.964 9.378a3.206 3.206 0 113.215-3.207v.002a3.206 3.206 0 01-3.207 3.207z",
    tagline: "Le CRM gratuit augmenté par l'IA",
  },
  "otter-ai": {
    gradient: "linear-gradient(135deg, #2D5BFF, #1E3A8A)",
    textColor: "white",
    logoFile: "/logos/otter.svg",
    tagline: "Transforme tes réunions en comptes-rendus",
  },
  "jasper": {
    gradient: "linear-gradient(135deg, #E04E39, #C73E2D)",
    textColor: "white",
    logoFile: "/logos/jasper.svg",
    tagline: "L'IA spécialisée marketing et copywriting",
  },
  "gamma": {
    gradient: "linear-gradient(135deg, #8B5CF6, #6D28D9)",
    textColor: "white",
    logoFile: "/logos/gamma.svg",
    tagline: "Des présentations pro en 2 minutes",
  },
  "zapier": {
    gradient: "linear-gradient(135deg, #FF4F00, #E04500)",
    textColor: "white",
    logoFile: "/logos/zapier.svg",
    tagline: "L'automatisation simple pour tous",
  },
  "copilot": {
    gradient: "linear-gradient(135deg, #000000, #24292E)",
    textColor: "white",
    logoFile: "/logos/copilot.svg",
    tagline: "L'assistant de code qui te rend 2x plus rapide",
  },
  "adobe-firefly": {
    gradient: "linear-gradient(135deg, #FF0000, #CC0000)",
    textColor: "white",
    logoFile: "/logos/adobe-firefly.svg",
    tagline: "L'IA créative intégrée à Photoshop",
  },
  "descript": {
    gradient: "linear-gradient(135deg, #1E88E5, #1565C0)",
    textColor: "white",
    logoFile: "/logos/descript.svg",
    tagline: "Édite tes vidéos comme un document texte",
  },
  "elevenlabs": {
    gradient: "linear-gradient(135deg, #000000, #1A1A1A)",
    textColor: "white",
    logoFile: "/logos/elevenlabs.svg",
    tagline: "Clone ta voix et génère de l'audio IA",
  },
  "copy-ai": {
    gradient: "linear-gradient(135deg, #6366F1, #4F46E5)",
    textColor: "white",
    logoFile: "/logos/copyai.svg",
    tagline: "Rédaction marketing en 2 clics",
  },
  "writesonic": {
    gradient: "linear-gradient(135deg, #0066FF, #0052CC)",
    textColor: "white",
    logoFile: "/logos/writesonic.svg",
    tagline: "Rédaction IA au meilleur rapport qualité-prix",
  },
};
