/**
 * Glossaire des termes IA et reconversion
 * Utilisé par le composant Tooltip pour afficher des définitions inline
 * Chaque terme = définition vulgarisée pour un public non-tech
 */

export const glossaire: Record<string, string> = {
  // IA et technologie
  "intelligence artificielle":
    "Programme informatique capable d'apprendre et de réaliser des tâches qui demandaient avant un humain : écrire, analyser, traduire, créer des images.",
  "ia": "Intelligence artificielle : programme qui apprend et réalise des tâches complexes automatiquement.",
  "ia générative":
    "Type d'IA capable de créer du contenu nouveau (texte, image, code, musique) à partir d'instructions en langage courant.",
  "chatgpt":
    "Assistant IA créé par OpenAI. Tu lui poses une question ou tu lui donnes une instruction, il répond en texte. Utilisé par 900 millions de personnes par semaine en 2026.",
  "claude": "Assistant IA créé par Anthropic, concurrent de ChatGPT. Réputé pour sa précision et sa capacité à traiter de longs documents.",
  "llm": "Large Language Model (grand modèle de langage) : le moteur derrière ChatGPT, Claude et les autres. Il prédit le mot suivant dans une phrase, ce qui lui permet de générer du texte cohérent.",
  "prompt": "L'instruction que tu donnes à une IA. Plus ton prompt est précis, meilleur est le résultat. C'est comme donner un brief à un assistant.",
  "prompt engineering":
    "L'art de formuler des instructions efficaces pour obtenir les meilleurs résultats d'une IA. C'est une compétence recherchée en 2026.",
  "automatisation":
    "Le fait de confier des tâches répétitives à un logiciel ou une IA pour qu'elles se fassent toutes seules, sans intervention humaine.",
  "machine learning":
    "Technique qui permet à un programme d'apprendre à partir de données, sans être explicitement programmé pour chaque cas. C'est comme ça que l'IA s'améliore.",
  "deep learning": "Forme avancée de machine learning inspirée du cerveau humain. C'est la technologie derrière la reconnaissance d'images et la traduction automatique.",
  "no-code":
    "Outils qui permettent de créer des applications, des sites web ou des automatisations sans écrire de code. Accessible à tous.",
  "api": "Interface qui permet à deux logiciels de communiquer entre eux. Par exemple, ton site peut appeler l'API de ChatGPT pour générer du texte automatiquement.",
  "saas": "Software as a Service : logiciel accessible en ligne via un abonnement mensuel, sans rien installer. Exemples : Gmail, Notion, Slack.",
  "ocr": "Reconnaissance optique de caractères : technologie qui lit le texte dans les images et les documents scannés pour le transformer en texte modifiable.",

  // Outils spécifiques
  "midjourney": "Outil d'IA qui génère des images à partir de descriptions textuelles. Très utilisé par les designers et les marketeurs.",
  "dall-e": "Outil de génération d'images par IA créé par OpenAI (les créateurs de ChatGPT).",
  "make.com": "Plateforme d'automatisation no-code. Tu connectes tes outils (Gmail, Slack, CRM...) et tu crées des workflows automatiques sans coder.",
  "zapier": "Concurrent de Make.com. Permet d'automatiser des tâches entre applications web.",
  "notion": "Outil tout-en-un pour organiser son travail : notes, bases de données, projets, wikis. Intègre maintenant de l'IA.",
  "cursor": "Éditeur de code avec IA intégrée. Le développeur décrit ce qu'il veut, l'IA écrit le code.",
  "copilot": "Assistant IA de GitHub (Microsoft) qui aide les développeurs en suggérant du code en temps réel.",

  // Emploi et reconversion
  "reconversion professionnelle":
    "Changer de métier ou de secteur d'activité. En 2026, souvent motivé par l'impact de l'IA sur son métier actuel.",
  "cpf": "Compte Personnel de Formation : budget formation que chaque salarié cumule et peut utiliser pour financer une formation certifiante.",
  "ptp": "Projet de Transition Professionnelle : dispositif qui permet de se former à un nouveau métier tout en étant rémunéré.",
  "vae": "Validation des Acquis de l'Expérience : obtenir un diplôme en faisant reconnaître son expérience professionnelle, sans repasser d'examen.",
  "france travail": "L'organisme public qui accompagne les demandeurs d'emploi (anciennement Pôle Emploi).",
  "freelance": "Travailleur indépendant qui propose ses services à plusieurs clients, sans être salarié.",
  "soft skills":
    "Compétences humaines et relationnelles : communication, empathie, leadership, créativité, esprit critique. Ce que l'IA ne sait pas faire.",
  "upskilling": "Monter en compétences dans son métier actuel pour s'adapter aux évolutions technologiques.",
  "reskilling": "Se former à un métier complètement différent du sien. Plus radical que l'upskilling.",

  // Études et rapports
  "ocde": "Organisation de Coopération et de Développement Économiques : institution internationale qui publie des études sur l'économie et l'emploi.",
  "mckinsey": "Cabinet de conseil en stratégie mondial. Publie des rapports influents sur l'avenir du travail et l'impact de l'IA.",
  "anthropic": "Entreprise américaine créatrice de Claude (concurrent de ChatGPT). A publié une étude majeure en mars 2026 sur l'impact de l'IA sur l'emploi.",
  "fmi": "Fonds Monétaire International : institution qui analyse l'économie mondiale. Estime que 40% des emplois mondiaux seront impactés par l'IA.",
  "cognizant": "Entreprise de conseil technologique. Son rapport 'New Work, New World' (2026) estime que 93% des métiers seront impactés par l'IA.",

  // SEO / Marketing (pour les fiches outils)
  "seo": "Search Engine Optimization (référencement naturel) : techniques pour que ton site apparaisse en haut des résultats Google.",
  "crm": "Customer Relationship Management : logiciel pour gérer tes contacts clients, tes ventes et ton suivi commercial. Exemples : HubSpot, Salesforce.",
  "e-e-a-t": "Critères Google pour évaluer la qualité d'un site : Expérience, Expertise, Autorité, Fiabilité.",
};
