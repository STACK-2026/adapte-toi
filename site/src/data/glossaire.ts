/**
 * Glossaire Adapte-toi : termes techniques vulgarisés pour novices 100%.
 * Chaque entrée : definition (vulgarisée) + example (concret) + internalLink (maillage obligatoire)
 * + externalSource (pour approfondir, source autorité vérifiée).
 *
 * Utilisé par : Glossaire.astro (inline), AutoGlossaire.astro (auto-wrap articles), /glossaire (pillar SEO).
 * Clé = terme en minuscules. L'affichage garde la casse fournie par l'auteur.
 */

export interface GlossaireEntry {
  definition: string;
  example: string;
  internalLink: { href: string; label: string };
  externalSource: { url: string; label: string };
  category: "ia" | "outils" | "emploi" | "juridique" | "dev" | "business";
  aliases?: string[]; // autres formulations qui doivent matcher le même terme
}

export const glossaire: Record<string, GlossaireEntry> = {
  // ==========================================================================
  // CATÉGORIE : IA (concepts fondamentaux)
  // ==========================================================================
  "intelligence artificielle": {
    definition: "Programme informatique capable d'apprendre et d'exécuter des tâches qui demandaient avant un humain : écrire, analyser, traduire, créer des images.",
    example: "Quand tu demandes à ChatGPT de rédiger un email, c'est de l'intelligence artificielle qui travaille derrière.",
    internalLink: { href: "/guides/ia-emploi-chiffres-cles", label: "IA et emploi : les chiffres clés" },
    externalSource: { url: "https://fr.wikipedia.org/wiki/Intelligence_artificielle", label: "Wikipedia" },
    category: "ia",
    aliases: ["ia"],
  },
  "ia générative": {
    definition: "Type d'IA qui crée du contenu nouveau (texte, image, code, son) à partir d'une simple instruction en français.",
    example: "Midjourney génère une image de chat samouraï parce que tu lui écris 'chat samouraï en pleine action' : c'est de l'IA générative.",
    internalLink: { href: "/outils", label: "Les outils d'IA générative" },
    externalSource: { url: "https://fr.wikipedia.org/wiki/Intelligence_artificielle_g%C3%A9n%C3%A9rative", label: "Wikipedia" },
    category: "ia",
  },
  "llm": {
    definition: "Large Language Model (grand modèle de langage) : le moteur derrière ChatGPT ou Claude. Il prédit mot après mot ce qui doit suivre dans une phrase, ce qui lui permet d'écrire des textes cohérents.",
    example: "Quand Claude te répond 300 mots bien tournés, un LLM a calculé chaque mot un par un à partir de milliards d'exemples.",
    internalLink: { href: "/outils/claude", label: "Claude, un LLM" },
    externalSource: { url: "https://fr.wikipedia.org/wiki/Grand_mod%C3%A8le_de_langage", label: "Wikipedia" },
    category: "ia",
    aliases: ["grand modèle de langage"],
  },
  "prompt": {
    definition: "L'instruction que tu écris à une IA. Plus ton prompt est précis, meilleur est le résultat, c'est comme briefer un assistant nouveau.",
    example: "'Résume ce PDF en 5 bullets, ton direct, pour un dirigeant pressé' est un bon prompt. 'Résume ça' est un mauvais prompt.",
    internalLink: { href: "/guides/prompt-engineering-debutant", label: "Guide prompt engineering débutant" },
    externalSource: { url: "https://www.anthropic.com/learn/prompt-engineering", label: "Anthropic" },
    category: "ia",
  },
  "prompt engineering": {
    definition: "L'art de formuler des prompts efficaces pour obtenir les meilleurs résultats d'une IA. Devenue une vraie compétence métier en 2026.",
    example: "Un prompt engineer réduit un temps de rédaction de 3 heures à 10 minutes en construisant le bon gabarit d'instruction pour son équipe.",
    internalLink: { href: "/guides/prompt-engineering-debutant", label: "S'initier au prompt engineering" },
    externalSource: { url: "https://platform.openai.com/docs/guides/prompt-engineering", label: "OpenAI Docs" },
    category: "ia",
  },
  "token": {
    definition: "Unité de base qu'un LLM lit et écrit, grosso modo un petit bout de mot. L'IA compte en tokens, pas en caractères.",
    example: "'Bonjour' pèse environ 2 tokens. Un prompt de 1 000 mots = environ 1 300 tokens. C'est ce qui détermine le prix de l'API.",
    internalLink: { href: "/outils/claude", label: "Claude et les tokens" },
    externalSource: { url: "https://platform.openai.com/tokenizer", label: "Tokenizer OpenAI" },
    category: "ia",
  },
  "hallucination": {
    definition: "Quand une IA invente une information qui sonne juste mais qui est fausse. Ça arrive à tous les LLM, d'où l'importance de toujours vérifier.",
    example: "Tu demandes à ChatGPT une référence juridique précise, il t'invente un article de loi qui n'existe pas : c'est une hallucination.",
    internalLink: { href: "/actu/anthropic-economic-index-mars-2026-impact", label: "Les limites actuelles des LLM" },
    externalSource: { url: "https://fr.wikipedia.org/wiki/Hallucination_(intelligence_artificielle)", label: "Wikipedia" },
    category: "ia",
  },
  "agent ia": {
    definition: "IA à qui tu confies une mission complète (pas juste une question), et qui exécute plusieurs étapes elle-même : chercher, raisonner, cliquer, appeler d'autres outils.",
    example: "Tu dis 'trouve-moi 5 prospects fintech à Paris, rédige un cold email à chacun, planifie l'envoi pour demain' : un agent IA peut enchaîner tout ça.",
    internalLink: { href: "/guides/automatiser-travail-ia", label: "Automatiser son travail avec l'IA" },
    externalSource: { url: "https://www.anthropic.com/news/claude-3-5-sonnet-agentic", label: "Anthropic agents" },
    category: "ia",
    aliases: ["agent autonome"],
  },
  "rag": {
    definition: "Retrieval-Augmented Generation : technique qui permet à une IA d'aller chercher une info dans ta base de documents avant de te répondre, pour coller à ta réalité.",
    example: "Un chatbot RH qui répond à tes questions en piochant dans les PDF de ton entreprise : c'est du RAG.",
    internalLink: { href: "/guides/automatiser-travail-ia", label: "Mettre l'IA au service de ses données" },
    externalSource: { url: "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", label: "Wikipedia EN" },
    category: "ia",
  },
  "fine-tuning": {
    definition: "Entraîner un modèle IA généraliste sur tes propres données pour le spécialiser sur ton métier ou ton style.",
    example: "Un cabinet d'avocats fait du fine-tuning pour que Claude réponde exactement dans le ton et le format de ses mémos internes.",
    internalLink: { href: "/metiers/developpeur-ia", label: "Dev IA et fine-tuning" },
    externalSource: { url: "https://platform.openai.com/docs/guides/fine-tuning", label: "OpenAI Docs" },
    category: "ia",
  },
  "rlhf": {
    definition: "Reinforcement Learning from Human Feedback : on entraîne l'IA en notant à la main ses réponses (bonnes / mauvaises) pour qu'elle apprenne à mieux répondre aux humains.",
    example: "Si ChatGPT est plus poli et utile qu'un modèle brut, c'est grâce au RLHF : des milliers d'humains ont noté des milliers de réponses.",
    internalLink: { href: "/outils/chatgpt", label: "ChatGPT, entraîné par RLHF" },
    externalSource: { url: "https://en.wikipedia.org/wiki/Reinforcement_learning_from_human_feedback", label: "Wikipedia EN" },
    category: "ia",
  },
  "transformer": {
    definition: "Architecture technique qui a tout changé en 2017 et qui fait tourner tous les LLM actuels (GPT, Claude, Gemini, Mistral).",
    example: "Le 'T' de ChatGPT, c'est Transformer. Sans cette invention, pas de GPT-4, pas de Claude, pas de vague IA 2022-2026.",
    internalLink: { href: "/guides/ia-emploi-chiffres-cles", label: "L'histoire moderne de l'IA" },
    externalSource: { url: "https://fr.wikipedia.org/wiki/Transformeur", label: "Wikipedia" },
    category: "ia",
  },
  "machine learning": {
    definition: "Apprentissage automatique : technique où un programme apprend à partir de données, sans qu'on lui code chaque cas à la main.",
    example: "Ton Netflix qui te propose une série parce que tu as regardé 10 séries similaires, c'est du machine learning.",
    internalLink: { href: "/metiers/data-analyst-ia", label: "Data analyst et machine learning" },
    externalSource: { url: "https://fr.wikipedia.org/wiki/Apprentissage_automatique", label: "Wikipedia" },
    category: "ia",
    aliases: ["apprentissage automatique", "ml"],
  },
  "deep learning": {
    definition: "Forme avancée de machine learning inspirée du cerveau humain (réseaux de neurones à plusieurs couches). C'est la techno derrière la reconnaissance d'images, la voix, les LLM.",
    example: "Quand Google Photos reconnaît ton chien sur 500 photos, c'est du deep learning qui a appris ce qu'est 'un chien'.",
    internalLink: { href: "/metiers/data-analyst-ia", label: "Les métiers data et deep learning" },
    externalSource: { url: "https://fr.wikipedia.org/wiki/Apprentissage_profond", label: "Wikipedia" },
    category: "ia",
    aliases: ["apprentissage profond"],
  },
  "benchmark": {
    definition: "Test standardisé pour comparer les IA entre elles (raisonnement, code, maths). Les éditeurs s'y affrontent comme au championnat.",
    example: "Claude 3.5 Sonnet a battu GPT-4 sur le benchmark HumanEval (code) en 2024 : c'est comme comparer deux voitures sur un même circuit.",
    internalLink: { href: "/outils", label: "Comparer les outils IA" },
    externalSource: { url: "https://huggingface.co/open-llm-leaderboard", label: "HuggingFace Leaderboard" },
    category: "ia",
  },
  "open source": {
    definition: "Code source public et réutilisable par tous, gratuitement. S'oppose aux logiciels propriétaires fermés.",
    example: "Mistral AI (FR) publie ses modèles en open source : n'importe qui peut les télécharger et les faire tourner chez soi.",
    internalLink: { href: "/guides/ia-europe-reglementation", label: "IA open source et Europe" },
    externalSource: { url: "https://fr.wikipedia.org/wiki/Open_source", label: "Wikipedia" },
    category: "ia",
  },

  // ==========================================================================
  // CATÉGORIE : OUTILS IA (éditeurs / produits)
  // ==========================================================================
  "chatgpt": {
    definition: "Assistant IA créé par OpenAI. Tu poses une question, il répond en texte. Plus de 900 millions d'utilisateurs hebdo en 2026.",
    example: "Tu lui donnes un long email client, il te rédige la réponse en 10 secondes, tu ajustes, tu envoies.",
    internalLink: { href: "/outils/chatgpt", label: "Fiche ChatGPT" },
    externalSource: { url: "https://chat.openai.com", label: "chat.openai.com" },
    category: "outils",
  },
  "claude": {
    definition: "Assistant IA créé par Anthropic. Concurrent direct de ChatGPT, réputé pour sa précision et sa capacité à traiter de très longs documents (200k tokens).",
    example: "Tu colles un rapport de 80 pages dans Claude et tu lui demandes de lister les 10 chiffres clés : il le fait en un prompt.",
    internalLink: { href: "/outils/claude", label: "Fiche Claude" },
    externalSource: { url: "https://claude.com", label: "claude.com" },
    category: "outils",
  },
  "midjourney": {
    definition: "IA de génération d'images à partir d'une description textuelle. Très utilisée par designers, marketeurs, créatifs.",
    example: "Tu écris 'un café parisien sous la pluie, ambiance film des années 60, photo argentique' et tu obtiens 4 visuels bluffants.",
    internalLink: { href: "/outils/midjourney", label: "Fiche Midjourney" },
    externalSource: { url: "https://www.midjourney.com", label: "midjourney.com" },
    category: "outils",
  },
  "copilot": {
    definition: "Assistant IA de GitHub (Microsoft) qui aide les développeurs en suggérant du code en temps réel pendant qu'ils tapent.",
    example: "Tu tapes 'fonction qui trie un tableau', Copilot te propose directement les 10 lignes de code. Tu acceptes avec Tab.",
    internalLink: { href: "/outils/copilot", label: "Fiche GitHub Copilot" },
    externalSource: { url: "https://github.com/features/copilot", label: "github.com/copilot" },
    category: "outils",
  },
  "cursor": {
    definition: "Éditeur de code avec IA intégrée. Le développeur décrit en français ce qu'il veut, l'IA écrit les fichiers.",
    example: "'Ajoute un bouton de partage LinkedIn sur ma page d'article' : Cursor édite le HTML + le CSS + le JS automatiquement.",
    internalLink: { href: "/outils/cursor", label: "Fiche Cursor" },
    externalSource: { url: "https://cursor.com", label: "cursor.com" },
    category: "outils",
  },
  "perplexity": {
    definition: "Moteur de recherche propulsé par IA qui répond à ta question avec des sources cliquables au lieu d'une liste de liens bleus.",
    example: "Tu demandes 'quelles sont les 3 études OCDE sur l'emploi IA 2024', Perplexity te donne la réponse avec les liens directs.",
    internalLink: { href: "/outils/perplexity", label: "Fiche Perplexity" },
    externalSource: { url: "https://www.perplexity.ai", label: "perplexity.ai" },
    category: "outils",
  },
  "notion": {
    definition: "Outil tout-en-un pour organiser ton travail : notes, bases de données, projets, wikis. Intègre maintenant une IA native.",
    example: "Une équipe de 10 personnes gère dans Notion : CRM, documentation, roadmap, CRaccount, board projet, tout au même endroit.",
    internalLink: { href: "/outils/notion-ai", label: "Fiche Notion AI" },
    externalSource: { url: "https://www.notion.so", label: "notion.so" },
    category: "outils",
  },
  "zapier": {
    definition: "Plateforme d'automatisation entre apps web : quand X se passe, fais Y automatiquement. Sans écrire une ligne de code.",
    example: "Quand un nouveau lead remplit le form de ton site, Zapier l'ajoute dans ton CRM et envoie un Slack à ton commercial.",
    internalLink: { href: "/outils/zapier", label: "Fiche Zapier" },
    externalSource: { url: "https://zapier.com", label: "zapier.com" },
    category: "outils",
  },
  "make": {
    definition: "Concurrent européen de Zapier (ex-Integromat). Plateforme d'automatisation no-code entre apps web, plus visuelle.",
    example: "Tu relies Gmail, Airtable et ChatGPT : chaque email reçu est résumé par l'IA et stocké dans ta base Airtable.",
    internalLink: { href: "/outils/make", label: "Fiche Make" },
    externalSource: { url: "https://www.make.com", label: "make.com" },
    category: "outils",
    aliases: ["make.com", "integromat"],
  },

  // ==========================================================================
  // CATÉGORIE : DEV (tech pour novices)
  // ==========================================================================
  "python": {
    definition: "Langage de programmation le plus utilisé pour l'IA, la data et l'automatisation. Réputé pour être lisible et accessible aux débutants.",
    example: "En 10 lignes de Python, tu peux lire un fichier Excel de 10 000 lignes, filtrer tes clients et les envoyer à l'API ChatGPT.",
    internalLink: { href: "/guides/se-former-ia-gratuitement", label: "Se former Python IA gratuitement" },
    externalSource: { url: "https://www.python.org", label: "python.org" },
    category: "dev",
  },
  "javascript": {
    definition: "Langage de programmation historique du web : c'est lui qui fait vivre 99 % des sites que tu consultes (interactions, animations).",
    example: "Le bouton 'Ajouter au panier' qui met à jour le total sans recharger la page, c'est du JavaScript.",
    internalLink: { href: "/metiers/developpeur-ia", label: "Dev JavaScript à l'ère de l'IA" },
    externalSource: { url: "https://developer.mozilla.org/fr/docs/Web/JavaScript", label: "MDN" },
    category: "dev",
    aliases: ["js"],
  },
  "algorithme": {
    definition: "Suite d'instructions précises que suit un programme pour accomplir une tâche. Comme une recette de cuisine pour un ordinateur.",
    example: "L'algorithme de TikTok qui décide quelle vidéo tu vois ensuite, c'est une recette complexe qui mélange tes likes, tes pauses, tes partages.",
    internalLink: { href: "/guides/ia-emploi-chiffres-cles", label: "Comment les algorithmes transforment le travail" },
    externalSource: { url: "https://fr.wikipedia.org/wiki/Algorithme", label: "Wikipedia" },
    category: "dev",
  },
  "api": {
    definition: "Application Programming Interface : tuyau qui permet à deux logiciels de se parler automatiquement. Ton site appelle l'API de ChatGPT, il reçoit la réponse, il l'affiche.",
    example: "Ton appli de météo affiche la température de Lyon parce qu'elle appelle l'API de Météo France toutes les heures.",
    internalLink: { href: "/guides/automatiser-travail-ia", label: "Automatiser avec les API" },
    externalSource: { url: "https://fr.wikipedia.org/wiki/Interface_de_programmation", label: "Wikipedia" },
    category: "dev",
  },
  "github": {
    definition: "Plateforme où les développeurs stockent, versionnent et partagent leur code. Propriété de Microsoft, utilisée par 100 M+ de devs dans le monde.",
    example: "Tu veux utiliser une librairie Python pour analyser tes CSV ? Tu la trouves sur GitHub, tu la télécharges, tu l'installes.",
    internalLink: { href: "/metiers/developpeur-ia", label: "Dev et GitHub au quotidien" },
    externalSource: { url: "https://github.com", label: "github.com" },
    category: "dev",
  },
  "cloud": {
    definition: "Serveurs informatiques hébergés à distance par des géants (AWS, Azure, Google Cloud) que tu loues au lieu d'acheter ta propre machine.",
    example: "Netflix ne possède pas ses serveurs, ils sont loués sur le cloud d'AWS. Tu règles à l'usage, tu scales à volonté.",
    internalLink: { href: "/guides/ia-emploi-chiffres-cles", label: "Le cloud et l'emploi tech" },
    externalSource: { url: "https://fr.wikipedia.org/wiki/Cloud_computing", label: "Wikipedia" },
    category: "dev",
  },
  "sql": {
    definition: "Langage universel pour parler aux bases de données : récupérer, filtrer, trier, agréger des données.",
    example: "'SELECT nom, email FROM clients WHERE ville = Paris' : en 1 ligne tu sors tous tes clients parisiens.",
    internalLink: { href: "/metiers/data-analyst-ia", label: "Data analyst et SQL" },
    externalSource: { url: "https://fr.wikipedia.org/wiki/Structured_Query_Language", label: "Wikipedia" },
    category: "dev",
  },
  "no-code": {
    definition: "Outils qui permettent de créer des apps, des sites et des automatisations sans écrire une ligne de code. Accessible à tous.",
    example: "Avec Bubble, tu construis un site e-commerce fonctionnel en 3 semaines, sans dev. Avec Make, tu automatises tes tâches sans coder.",
    internalLink: { href: "/guides/automatiser-travail-ia", label: "Automatiser en no-code" },
    externalSource: { url: "https://fr.wikipedia.org/wiki/No-code", label: "Wikipedia" },
    category: "dev",
    aliases: ["nocode", "no code"],
  },
  "low-code": {
    definition: "Entre no-code et code classique : tu assembles visuellement, mais tu peux ajouter du code pour les cas complexes.",
    example: "Retool ou Budibase : tu construis des dashboards internes en glisser-déposer, puis tu greffes du JavaScript si besoin.",
    internalLink: { href: "/guides/automatiser-travail-ia", label: "Low-code vs no-code" },
    externalSource: { url: "https://en.wikipedia.org/wiki/Low-code_development_platform", label: "Wikipedia EN" },
    category: "dev",
  },
  "open api": {
    definition: "Standard pour documenter une API de manière structurée (ex-Swagger). Permet aux autres devs de comprendre et d'utiliser ton API vite.",
    example: "L'API de Stripe (paiement) est documentée en OpenAPI : n'importe quel dev peut l'intégrer en 1 après-midi.",
    internalLink: { href: "/metiers/developpeur-ia", label: "Dev et intégrations API" },
    externalSource: { url: "https://www.openapis.org", label: "openapis.org" },
    category: "dev",
  },

  // ==========================================================================
  // CATÉGORIE : EMPLOI / RECONVERSION
  // ==========================================================================
  "reconversion professionnelle": {
    definition: "Changer de métier ou de secteur d'activité. En 2026, souvent motivé par l'impact de l'IA sur son métier actuel.",
    example: "Une comptable de 38 ans qui devient consultante IA pour PME après 9 mois de formation CPF + PTP : reconversion type 2026.",
    internalLink: { href: "/guides/reconversion-ia-guide-complet", label: "Guide reconversion IA complet" },
    externalSource: { url: "https://www.francetravail.fr", label: "France Travail" },
    category: "emploi",
  },
  "cpf": {
    definition: "Compte Personnel de Formation : budget formation que chaque salarié cumule chaque année (jusqu'à 500 EUR/an plafonné à 5 000 EUR) et utilise pour financer une formation certifiante.",
    example: "Tu as 3 200 EUR sur ton CPF, tu les utilises pour payer une formation prompt engineering certifiée Qualiopi. Zéro reste à charge.",
    internalLink: { href: "/guides/financer-formation-ia-cpf", label: "Financer sa formation IA avec le CPF" },
    externalSource: { url: "https://www.moncompteformation.gouv.fr", label: "moncompteformation.gouv.fr" },
    category: "emploi",
  },
  "ptp": {
    definition: "Projet de Transition Professionnelle : dispositif qui permet à un salarié de se former à un nouveau métier tout en conservant sa rémunération pendant la formation.",
    example: "Un comptable obtient un PTP de 12 mois pour devenir data analyst : il garde son salaire, l'État finance la formation, il revient sur un nouveau poste.",
    internalLink: { href: "/guides/financer-formation-ia-cpf", label: "PTP et financements formation" },
    externalSource: { url: "https://www.transitionspro.fr", label: "Transitions Pro" },
    category: "emploi",
  },
  "vae": {
    definition: "Validation des Acquis de l'Expérience : obtenir un diplôme en faisant reconnaître officiellement son expérience pro, sans repasser un examen classique.",
    example: "10 ans d'expérience RH sans diplôme ? Une VAE peut te décerner un master RH en 9-12 mois sur dossier + soutenance.",
    internalLink: { href: "/guides/reconversion-ia-guide-complet", label: "VAE dans un parcours de reconversion" },
    externalSource: { url: "https://vae.gouv.fr", label: "vae.gouv.fr" },
    category: "emploi",
  },
  "france travail": {
    definition: "Organisme public qui accompagne les demandeurs d'emploi et publie les grandes enquêtes sur le marché du travail (BMO notamment). Anciennement Pôle Emploi.",
    example: "France Travail publie chaque année le BMO, enquête qui recense les projets de recrutement par métier et par région.",
    internalLink: { href: "/actu/france-travail-bmo-2025-cognizant-metiers-tension", label: "Décryptage BMO 2025" },
    externalSource: { url: "https://www.francetravail.org", label: "francetravail.org" },
    category: "emploi",
    aliases: ["pôle emploi"],
  },
  "freelance": {
    definition: "Travailleur indépendant qui propose ses services à plusieurs clients, sans être salarié. Souvent en micro-entreprise ou EURL.",
    example: "Une ancienne salariée marketing devient freelance : 4 clients à 1 500 EUR/mois, 6 000 EUR de CA, plus de liberté, plus de risque.",
    internalLink: { href: "/guides/freelance-ia-guide", label: "Guide freelance IA" },
    externalSource: { url: "https://www.urssaf.fr/portail/home/independant.html", label: "URSSAF indépendants" },
    category: "emploi",
  },
  "soft skills": {
    definition: "Compétences humaines et relationnelles : communication, empathie, leadership, créativité, esprit critique. Ce que l'IA ne sait justement pas faire.",
    example: "Un manager qui désamorce un conflit d'équipe, c'est 100 % soft skill, 0 % technique : irremplaçable par une IA.",
    internalLink: { href: "/guides/reconversion-ia-guide-complet", label: "Valoriser ses soft skills" },
    externalSource: { url: "https://fr.wikipedia.org/wiki/Compétences_comportementales", label: "Wikipedia" },
    category: "emploi",
  },
  "hard skills": {
    definition: "Compétences techniques mesurables et certifiables : savoir coder en Python, parler anglais, maîtriser Excel, manipuler une base SQL.",
    example: "Un cadre commercial qui passe une certif Salesforce, c'est un hard skill ajouté à son CV, directement valorisable.",
    internalLink: { href: "/guides/se-former-ia-gratuitement", label: "Empiler des hard skills IA" },
    externalSource: { url: "https://en.wikipedia.org/wiki/Skill", label: "Wikipedia EN" },
    category: "emploi",
  },
  "upskilling": {
    definition: "Monter en compétences dans son métier actuel pour s'adapter aux évolutions technologiques. On reste dans sa voie, on l'enrichit.",
    example: "Une avocate qui suit une formation 'IA pour juristes' pour automatiser sa veille et ses mémos : upskilling.",
    internalLink: { href: "/guides/prompt-engineering-debutant", label: "Upskilling prompt engineering" },
    externalSource: { url: "https://www.oecd.org/en/topics/sub-issues/skills.html", label: "OCDE Skills" },
    category: "emploi",
  },
  "reskilling": {
    definition: "Se former à un métier complètement différent du sien. Plus radical que l'upskilling, c'est une vraie bifurcation.",
    example: "Un chargé de clientèle banque qui devient développeur full-stack après un bootcamp de 6 mois : reskilling total.",
    internalLink: { href: "/guides/reconversion-ia-guide-complet", label: "Réussir son reskilling" },
    externalSource: { url: "https://www.oecd.org/en/topics/sub-issues/skills.html", label: "OCDE Skills" },
    category: "emploi",
  },
  "bilan de compétences": {
    definition: "Démarche de 24 heures (étalées sur 2-3 mois) qui aide à faire le point sur ses compétences, ses motivations et son projet pro. Financée à 100 % par le CPF.",
    example: "Avant de te reconvertir, 24h de bilan financé par ton CPF évitent 80 % des mauvais choix de réorientation.",
    internalLink: { href: "/guides/reconversion-ia-guide-complet", label: "Étape 1 : bilan de compétences" },
    externalSource: { url: "https://www.service-public.fr/particuliers/vosdroits/F3087", label: "service-public.fr" },
    category: "emploi",
  },
  "bmo": {
    definition: "Besoins en Main-d'Œuvre : enquête annuelle de France Travail auprès de 2+ millions d'employeurs. Cartographie des intentions de recrutement par métier et territoire.",
    example: "Le BMO 2025 indique 2,77 M de projets de recrutement en France, 57 % jugés difficiles à pourvoir.",
    internalLink: { href: "/actu/france-travail-bmo-2025-cognizant-metiers-tension", label: "Décryptage BMO 2025" },
    externalSource: { url: "https://www.francetravail.org/statistiques-analyses/enquetes/bmo.html", label: "BMO France Travail" },
    category: "emploi",
  },

  // ==========================================================================
  // CATÉGORIE : ORGS / ÉTUDES
  // ==========================================================================
  "ocde": {
    definition: "Organisation de Coopération et de Développement Économiques : 38 pays membres, produit des études de référence sur l'économie, l'emploi, l'éducation.",
    example: "Le chiffre '27 % des emplois français exposés à l'automatisation d'ici 2030' vient de l'OCDE.",
    internalLink: { href: "/actu/ocde-27-pourcent-emplois-france-automatisation", label: "Décryptage OCDE 27 %" },
    externalSource: { url: "https://www.oecd.org/fr.html", label: "oecd.org" },
    category: "emploi",
  },
  "mckinsey": {
    definition: "Cabinet de conseil en stratégie mondial. Publie régulièrement des rapports influents sur l'avenir du travail et l'impact de l'IA.",
    example: "Le rapport McKinsey Global Institute sur l'IA génère tous les ans les statistiques que tu vois reprises partout en presse.",
    internalLink: { href: "/guides/ia-emploi-chiffres-cles", label: "Synthèse des études IA emploi" },
    externalSource: { url: "https://www.mckinsey.com/mgi", label: "McKinsey Global Institute" },
    category: "emploi",
  },
  "anthropic": {
    definition: "Entreprise américaine éditrice de Claude. Fondée en 2021 par d'anciens d'OpenAI. A publié en 2026 le premier Economic Index chiffrant l'impact IA sur l'emploi.",
    example: "Quand Claude te répond, Anthropic est la boîte qui fait tourner le modèle derrière.",
    internalLink: { href: "/actu/anthropic-economic-index-mars-2026-impact", label: "Décryptage Anthropic Economic Index" },
    externalSource: { url: "https://www.anthropic.com", label: "anthropic.com" },
    category: "outils",
  },
  "openai": {
    definition: "Entreprise américaine éditrice de ChatGPT, DALL-E, GPT-4o. Fondée en 2015, initialement non-profit. Valorisée plus de 150 Mds USD en 2025.",
    example: "Derrière ChatGPT, Microsoft Copilot, l'intégration IA d'Apple : c'est la techno d'OpenAI.",
    internalLink: { href: "/outils/chatgpt", label: "ChatGPT, produit OpenAI" },
    externalSource: { url: "https://openai.com", label: "openai.com" },
    category: "outils",
  },
  "fmi": {
    definition: "Fonds Monétaire International : institution qui analyse l'économie mondiale. Estime que 40 % des emplois mondiaux seront impactés par l'IA.",
    example: "Le rapport FMI de janvier 2024 sur l'IA est devenu la référence pour mesurer l'exposition par pays.",
    internalLink: { href: "/guides/ia-emploi-chiffres-cles", label: "Chiffres FMI sur l'IA" },
    externalSource: { url: "https://www.imf.org/fr/Home", label: "imf.org" },
    category: "emploi",
  },
  "cognizant": {
    definition: "Entreprise de conseil et services IT (350 000 salariés). Son rapport 'New Work, New World' (2026) estime que 93 % des métiers seront impactés par l'IA d'ici 2030.",
    example: "Cognizant projette 12 % des postes français significativement reconfigurés par l'IA d'ici 2030.",
    internalLink: { href: "/actu/france-travail-bmo-2025-cognizant-metiers-tension", label: "Décryptage BMO + Cognizant" },
    externalSource: { url: "https://www.cognizant.com", label: "cognizant.com" },
    category: "emploi",
  },
  "ipsos": {
    definition: "Institut de sondage français parmi les plus grands mondialement. Publie le baromètre de référence sur les intentions de reconversion des actifs.",
    example: "47 % des actifs français envisagent une reconversion dans les 2 ans : c'est un chiffre Ipsos 2025.",
    internalLink: { href: "/actu/ipsos-47-pourcent-actifs-reconversion-ia", label: "Décryptage Ipsos reconversion" },
    externalSource: { url: "https://www.ipsos.com/fr-fr", label: "ipsos.com" },
    category: "emploi",
  },
  "insee": {
    definition: "Institut National de la Statistique et des Études Économiques. La source publique française de référence pour toutes les stats emploi, démographie, économie.",
    example: "Le taux de chômage officiel français, c'est l'INSEE qui le calcule selon les normes du Bureau International du Travail.",
    internalLink: { href: "/guides/ia-emploi-chiffres-cles", label: "Stats INSEE sur l'emploi" },
    externalSource: { url: "https://www.insee.fr", label: "insee.fr" },
    category: "emploi",
  },

  // ==========================================================================
  // CATÉGORIE : JURIDIQUE / RÉGLEMENTATION
  // ==========================================================================
  "ai act": {
    definition: "Règlement européen sur l'IA adopté en 2024, applicable progressivement 2025-2027. Classe les usages IA en 4 niveaux de risque (inacceptable, haut, limité, minimal) avec obligations proportionnées.",
    example: "Un logiciel RH qui trie des CV est classé 'haut risque' par l'AI Act : l'entreprise doit documenter, auditer, informer les candidats.",
    internalLink: { href: "/guides/ia-europe-reglementation", label: "Guide AI Act complet" },
    externalSource: { url: "https://artificialintelligenceact.eu", label: "artificialintelligenceact.eu" },
    category: "juridique",
    aliases: ["ia act", "règlement ia"],
  },
  "rgpd": {
    definition: "Règlement Général sur la Protection des Données : loi européenne de 2018 qui protège les données personnelles. Amendes jusqu'à 4 % du CA mondial en cas de violation.",
    example: "Meta a écopé de 1,2 Md EUR d'amende RGPD en 2023 pour transfert illégal de données européennes vers les USA.",
    internalLink: { href: "/guides/ia-europe-reglementation", label: "RGPD et IA" },
    externalSource: { url: "https://www.cnil.fr/fr/rgpd-de-quoi-parle-t-on", label: "CNIL" },
    category: "juridique",
  },
  "cnil": {
    definition: "Commission Nationale de l'Informatique et des Libertés : autorité française qui veille à la protection des données personnelles et peut sanctionner.",
    example: "La CNIL a infligé 150 M EUR à Google pour cookies non conformes en 2022.",
    internalLink: { href: "/guides/ia-europe-reglementation", label: "CNIL et IA en France" },
    externalSource: { url: "https://www.cnil.fr", label: "cnil.fr" },
    category: "juridique",
  },
  "open source license": {
    definition: "Contrat qui dit ce que tu as le droit de faire avec un logiciel open source : l'utiliser, le modifier, le revendre, ou pas. MIT, Apache, GPL sont les plus connues.",
    example: "Tu veux utiliser un modèle Mistral dans ton produit commercial ? Vérifie sa licence : Apache 2.0 permet, certaines non-commerciales non.",
    internalLink: { href: "/guides/ia-europe-reglementation", label: "Licences et usage commercial IA" },
    externalSource: { url: "https://choosealicense.com", label: "choosealicense.com" },
    category: "juridique",
  },

  // ==========================================================================
  // CATÉGORIE : BUSINESS / STARTUP
  // ==========================================================================
  "saas": {
    definition: "Software as a Service : logiciel accessible en ligne via un abonnement mensuel ou annuel. Rien à installer. Mises à jour automatiques.",
    example: "Gmail, Notion, Slack, HubSpot, Shopify : tous des SaaS. Tu paies chaque mois, tu utilises, point.",
    internalLink: { href: "/outils", label: "Annuaire des SaaS IA" },
    externalSource: { url: "https://fr.wikipedia.org/wiki/Software_as_a_service", label: "Wikipedia" },
    category: "business",
  },
  "api rest": {
    definition: "Standard le plus courant pour construire une API web : communication en HTTP, données au format JSON, simple à intégrer.",
    example: "Pour appeler ChatGPT depuis ton site, tu fais un POST sur api.openai.com/v1/chat : c'est une API REST.",
    internalLink: { href: "/metiers/developpeur-ia", label: "Dev et API REST" },
    externalSource: { url: "https://fr.wikipedia.org/wiki/Representational_state_transfer", label: "Wikipedia" },
    category: "dev",
  },
  "crm": {
    definition: "Customer Relationship Management : logiciel pour suivre tes contacts prospects, clients, ventes, interactions. Colonne vertébrale du commerce.",
    example: "Un commercial utilise HubSpot ou Salesforce pour voir les 40 prospects à relancer cette semaine et leur historique.",
    internalLink: { href: "/outils/hubspot", label: "Fiche HubSpot CRM" },
    externalSource: { url: "https://fr.wikipedia.org/wiki/Gestion_de_la_relation_client", label: "Wikipedia" },
    category: "business",
  },
  "seo": {
    definition: "Search Engine Optimization (référencement naturel) : ensemble de techniques pour qu'un site apparaisse en haut des résultats Google, Bing, Perplexity, ChatGPT.",
    example: "Adapte-toi travaille son SEO : c'est pour ça que tu es arrivé ici en cherchant 'IA emploi reconversion'.",
    internalLink: { href: "/guides/ia-emploi-chiffres-cles", label: "SEO à l'ère de l'IA" },
    externalSource: { url: "https://developers.google.com/search/docs", label: "Google Search Docs" },
    category: "business",
  },
  "geo": {
    definition: "Generative Engine Optimization : optimiser ses contenus pour être cité par ChatGPT, Claude, Perplexity (pas seulement pour sortir dans Google).",
    example: "Avoir une page 'chiffres clés IA emploi' bien structurée avec sources, c'est faire du GEO : Perplexity te cite en source.",
    internalLink: { href: "/guides/ia-emploi-chiffres-cles", label: "Page référence citée par les IA" },
    externalSource: { url: "https://arxiv.org/abs/2311.09735", label: "Paper GEO arXiv" },
    category: "business",
  },
  "e-e-a-t": {
    definition: "Experience, Expertise, Authoritativeness, Trustworthiness : critères Google pour juger la qualité d'un site. L'auteur est-il compétent, l'info sourcée, l'expérience vécue ?",
    example: "Un article santé signé par un médecin, avec sources académiques, images originales : coche E-E-A-T haut.",
    internalLink: { href: "/guides/ia-emploi-chiffres-cles", label: "E-E-A-T et contenus IA" },
    externalSource: { url: "https://developers.google.com/search/docs/fundamentals/creating-helpful-content", label: "Google E-E-A-T" },
    category: "business",
  },
  "arr": {
    definition: "Annual Recurring Revenue : chiffre d'affaires récurrent annuel d'un SaaS. Métrique reine de la valorisation.",
    example: "Une startup SaaS à 2 M EUR d'ARR se valorise souvent 15 à 30 fois son ARR, soit 30-60 M EUR.",
    internalLink: { href: "/guides/freelance-ia-guide", label: "Business models IA" },
    externalSource: { url: "https://en.wikipedia.org/wiki/Annual_recurring_revenue", label: "Wikipedia EN" },
    category: "business",
  },
  "burn rate": {
    definition: "Vitesse à laquelle une startup consomme son cash chaque mois. Divise ta trésorerie par ton burn rate : tu as ton runway (combien de mois avant le mur).",
    example: "Startup avec 600 k EUR en caisse et un burn de 50 k EUR/mois : 12 mois de runway avant levée obligatoire.",
    internalLink: { href: "/guides/freelance-ia-guide", label: "Gérer sa trésorerie freelance/startup" },
    externalSource: { url: "https://en.wikipedia.org/wiki/Burn_rate", label: "Wikipedia EN" },
    category: "business",
    aliases: ["burn-rate"],
  },
  "cold email": {
    definition: "Email de prospection envoyé à un contact qui ne te connaît pas. Encadré par RGPD en B2B, interdit au grand public sans opt-in.",
    example: "Un cold email bien fait = personnalisé sur 1 fait récent du prospect, 1 offre claire, 1 CTA simple. Taux de réponse 5-15 %.",
    internalLink: { href: "/guides/freelance-ia-guide", label: "Prospection freelance à l'IA" },
    externalSource: { url: "https://www.cnil.fr/fr/la-prospection-commerciale-par-courrier-electronique", label: "CNIL prospection" },
    category: "business",
  },
  "ocr": {
    definition: "Reconnaissance Optique de Caractères : techno qui lit le texte dans des images ou PDF scannés pour le transformer en texte modifiable.",
    example: "Un comptable scanne 200 factures papier, un OCR les lit, extrait montants et fournisseurs, les envoie dans son logiciel.",
    internalLink: { href: "/guides/automatiser-travail-ia", label: "Automatiser ses docs avec l'OCR" },
    externalSource: { url: "https://fr.wikipedia.org/wiki/Reconnaissance_optique_de_caract%C3%A8res", label: "Wikipedia" },
    category: "business",
  },
};

// Index par aliases pour résolution rapide côté composant
export const glossaireAliases: Record<string, string> = (() => {
  const map: Record<string, string> = {};
  for (const [key, entry] of Object.entries(glossaire)) {
    map[key] = key;
    if (entry.aliases) {
      for (const alias of entry.aliases) map[alias.toLowerCase()] = key;
    }
  }
  return map;
})();

export function resolveGlossaireKey(input: string): string | null {
  const k = input.toLowerCase().trim();
  return glossaireAliases[k] ?? null;
}

export const glossaireCategories: Array<{ id: GlossaireEntry["category"]; label: string; description: string }> = [
  { id: "ia", label: "IA et concepts", description: "Les termes fondamentaux pour comprendre l'intelligence artificielle." },
  { id: "outils", label: "Outils IA", description: "Les produits et plateformes qui équipent les actifs en 2026." },
  { id: "dev", label: "Développement et tech", description: "Le vocabulaire tech utile même aux non-développeurs." },
  { id: "emploi", label: "Emploi et reconversion", description: "Dispositifs, acronymes et organismes du monde du travail." },
  { id: "juridique", label: "Juridique et réglementation", description: "AI Act, RGPD, CNIL et cadre européen." },
  { id: "business", label: "Business et marketing", description: "SaaS, CRM, SEO, métriques qu'on croise partout." },
];
