---
title: "France Travail balance un algorithme pour traquer les chômeurs : le contrôle social version IA"
description: "France Travail déploie un algorithme de profilage pour cibler 500 000 chômeurs en 2026. Derrière les promesses d'efficacité, un glissement dangereux vers un contrôle automatisé et opaque."
date: 2026-07-20
category: "politique"
impactLevel: 4
author: "Léa Moreau"
keyQuote:
  text: "On assiste à la transformation d'un problème politique, le choix des critères de sélection des personnes à contrôler, en un problème purement technique."
  author: "La Quadrature du Net"
  context: "Réaction à l'algorithme de profilage de France Travail, juillet 2026"
tldr:
  - "France Travail utilise un algorithme pour cibler 500 000 chômeurs en 2026, avec un taux de sanction ou redynamisation de 64% sur les dossiers sélectionnés."
  - "L'outil analyse 26 variables (refus d'offres, absences aux entretiens, métiers en tension...) pour profiler les demandeurs d'emploi, sans transparence sur la pondération des critères."
  - "La Quadrature du Net dénonce une dépolitisation du contrôle social : l'IA est présentée comme neutre, alors qu'elle reproduit des biais systémiques (ex : retrait du critère 'revenu' après détection d'un biais)."
  - "Aucun accès au code source malgré les demandes répétées, ce qui empêche tout audit indépendant sur les discriminations potentielles."
sources:
  - title: "France Travail : un algorithme pour accélérer le profilage des chômeurs et les contrôles"
    url: "https://next.ink/248042/france-travail-un-algorithme-pour-accelerer-le-profilage-des-chomeurs-et-les-controles/"
    outlet: "Next.ink"
    date: 2026-07-20
  - title: "Transparence, discriminations : les questions soulevées par l'algorithme de la CAF"
    url: "https://next.ink/182345/transparence-discriminations-questions-algorithme-caf/"
    outlet: "Next.ink"
    date: 2023-11-28
relatedMetiers:
  - "consultant-ia"
  - "charge-clientele-ia"
  - "data-analyst-ia"
  - "avocat-ia"
relatedGuides:
  - "ia-emploi-chiffres-cles"
  - "ia-europe-reglementation"
  - "reconversion-ia-guide-complet"
relatedOutils:
  - "claude"
  - "perplexity"
  - "notion-ai"
imageAlt: "Capture d'écran d'une diapositive PowerPoint de France Travail montrant un schéma d'algorithme de profilage des chômeurs"
keywords: "France Travail, algorithme, profilage, chômeurs, contrôle, IA, biais, Quadrature du Net, droits sociaux, automatisation, emploi, reconversion"
lastReviewed: 2026-07-20
reviewedBy: "Rédaction Adapte-toi"
draft: false
---

## Le fait
France Travail a déployé un algorithme de profilage pour cibler les chômeurs à contrôler. Un document interne de décembre 2025, révélé par la Quadrature du Net, décrit un système analysant **26 variables** (refus d'offres, absences aux entretiens, métiers en tension, etc.) pour identifier les demandeurs d'emploi nécessitant un **Contrôle de Recherche d'Emploi (CRE)**.

L'objectif : **500 000 contrôles ciblés en 2026**, soit 40% des vérifications. Sur un échantillon test de 60 000 dossiers, l'algorithme a abouti à une **redynamisation ou sanction dans 64% des cas**, contre 53% pour les contrôles aléatoires. Basé sur un arbre de décision, le modèle a été entraîné sur des données historiques de CRE pour repérer les profils à risque.

Parmi les cibles : sortants de formation, ruptures conventionnelles, métiers en tension. France Travail justifie l'outil par la complexité des variables à croiser, la suppression des "a priori" et un gain d'efficacité. Mais **le poids des critères reste opaque**, et le code source inaccessible malgré les demandes de la Quadrature du Net.

## Ce qu'on en dit vraiment

**1. L'algorithme n'est pas neutre : c'est un outil politique.**
Le document présente l'outil comme "objectif", remplaçant les "a priori" des conseillers. Pourtant, **les 26 variables et leur pondération relèvent de choix politiques**. Exemple : le critère "Salaire Journalier de Référence" (SJR) a été retiré après détection d'un biais envers les bas revenus, puis réintégré avec ajustements. La Quadrature du Net souligne cette dépolitisation : un débat sur qui contrôler est réduit à une équation.

**2. Le ciblage des "métiers en tension" pénalise les précaires.**
France Travail cible les secteurs avec des offres abondantes (BTP, restauration, santé), où les conditions de travail sont souvent précaires. **L'algorithme risque de sanctionner ceux qui refusent des offres indécentes**, pas les "profiteurs".

**3. Sans accès au code, les biais restent invisibles.**
France Travail affirme avoir "recherché les biais", mais **le code source est verrouillé**, comme pour la CAF ou l'Assurance Maladie. La Quadrature du Net rappelle que ces outils sont rarement accessibles sans bataille juridique. Comment vérifier si l'algorithme ne discrimine pas femmes, seniors ou habitants des quartiers prioritaires ?

**4. L'outil pourrait s'étendre à d'autres allocations.**
Le document évoque un élargissement à "d'autres publics". On craint une généralisation au RSA, à la prime d'activité, voire à d'autres administrations. **L'argument du "gain d'efficacité" sert de prétexte** pour étendre le contrôle social sous couvert de lutte contre la fraude.

## Les chiffres qui comptent
- **500 000** : contrôles ciblés prévus en 2026 (40% du total). *(Next.ink, 20/07/2026)*
- **64%** : taux de dossiers aboutissant à une sanction ou redynamisation après contrôle ciblé, contre 53% pour les contrôles aléatoires. *(Document interne France Travail, décembre 2025)*
- **26** : variables analysées (refus d'offres, absences, métiers en tension, etc.). *(Next.ink, 20/07/2026)*
- **79%** : dossiers ciblés donnant lieu à un examen complémentaire, contre 53% pour les requêtes aléatoires. *(Document interne France Travail, décembre 2025)*
- **7 000** : tests réalisés sur des demandeurs en rupture conventionnelle. *(Next.ink, 20/07/2026)*

## La citation qui résume tout
> "On assiste à la transformation d'un problème politique, le choix des critères de sélection des personnes à contrôler, en un problème purement technique."
> *La Quadrature du Net, juillet 2026*

Cette phrase résume l'enjeu : **l'IA masque des choix politiques derrière une apparence de neutralité**. En présentant l'algorithme comme "objectif", France Travail évite le débat démocratique. Les machines reproduisent les biais de leurs concepteurs.

## Pour toi concrètement

**Tu es demandeur d'emploi.**
- **30 jours** : Mets à jour ton **CV** sur France Travail et réponds aux **Offres Raisonnables d'Emploi (ORE)**. L'algorithme surveille ces critères. Consulte notre [guide pour optimiser ton profil](/guides/se-former-ia-gratuitement).
- **60 jours** : Si tu es contrôlé, **prépare tes preuves** (candidatures, attestations). L'algorithme peut se tromper. Utilise [Notion AI](/outils/notion-ai) pour organiser tes documents.
- **90 jours** : Dans un **métier en tension**, méfie-toi des offres précaires. Refuser une offre indécente ne devrait pas être sanctionné. Voir notre [fiche "chargé de clientèle IA"](/metiers/charge-clientele-ia).

**Tu es conseiller à France Travail.**
- **30 jours** : **Documente les biais** observés (ex : ciblage des femmes, seniors). Signale-les. Notre [guide sur les biais algorithmiques](/guides/ia-emploi-chiffres-cles) peut t'aider.
- **60 jours** : **Ne te fie pas uniquement à l'IA**. Elle peut ignorer des contextes humains (santé, discriminations). Utilise [Claude](/outils/claude) pour des questions plus nuancées.
- **90 jours** : **Forme-toi aux limites de l'IA**. Complète avec notre [guide sur la régulation européenne](/guides/ia-europe-reglementation).

**Tu es juriste, militant ou journaliste.**
- **30 jours** : **Demande le code source** via la CADA. La Quadrature du Net propose un [modèle de lettre](https://www.laquadrature.net/).
- **60 jours** : **Compare avec d'autres algorithmes** (CAF, Assurance Maladie). Voir notre [décryptage sur l'algorithme de la CAF](/actu/algorithme-caf-controles).
- **90 jours** : **Organise un atelier** pour expliquer l'algorithme. Utilise [Perplexity](/outils/perplexity) pour des études de cas similaires.

**Tu es développeur ou data analyst.**
- **30 jours** : **Étudie les arbres de décision**. Notre [fiche "data analyst IA"](/metiers/data-analyst-ia) explique comment les tester.
- **60 jours** : **Reproduis un modèle** avec des données ouvertes (ex : offres Pôle Emploi avant 2024). Utilise [Cursor](/outils/cursor).
- **90 jours** : **Publie une analyse critique**. Les médias comme [Next.ink](https://next.ink) ou [Mediapart](https://www.mediapart.fr) sont intéressés.

## Le verdict Adapte-toi
France Travail a franchi une ligne : **l'algorithme n'est pas un outil d'accompagnement, mais un instrument de contrôle de masse**. Derrière l'efficacité se cache une machine décidant qui sanctionner, sans transparence ni débat.

**Ce qui doit changer** :
1. **Un audit indépendant** du code source, avec publication des résultats.
2. **Un moratoire** sur l'extension de l'algorithme.
3. **Un droit de regard** pour les demandeurs d'emploi sur leurs données.

Pour aller plus loin, consulte notre [guide sur l'IA et l'emploi](/guides/ia-emploi-chiffres-cles) ou notre [fiche "avocat IA"](/metiers/avocat-ia). La bataille pour les droits sociaux à l'ère de l'IA commence.