#!/usr/bin/env python3
"""
Generate articles.json - Genere 100 sujets d'articles SEO via Claude API.

Usage:
  python generate_articles_json.py

Prerequis:
  - ANTHROPIC_API_KEY dans .env
"""

import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ARTICLES_FILE = Path(__file__).parent / "articles.json"

SITE_CONTEXT = """
Nom du projet : Adapte-toi
Secteur : reconversion professionnelle, emploi, intelligence artificielle
Description : Media francophone de reference sur la reconversion professionnelle a l'ere de l'IA. Pas un organisme de formation, un media editorial independant qui informe et outille.
Mots-cles principaux : reconversion professionnelle IA, metiers menaces intelligence artificielle, formation IA, emploi IA 2026, outils IA par metier
Categories de blog : reconversion, metiers-ia, formation, outils-ia, actu-emploi, temoignages, freelance-ia, etudes-rapports
Cible : salaries inquiets (35-55 ans), etudiants perdus (18-28 ans), freelances opportunistes (25-45 ans), cadres/managers en veille (40-55 ans), demandeurs d'emploi (tout age)
Langue : francais
Marche : France, Belgique francophone, Suisse romande, Afrique francophone

Sujets a couvrir :
- Impact de l'IA sur les metiers intellectuels (comptable, avocat, RH, marketing, journaliste, traducteur, graphiste, developpeur, etc.)
- Reconversion professionnelle a l'ere de l'IA (guides, etapes, financement CPF)
- Formation IA (gratuite, payante, CPF, en ligne)
- Outils IA par metier (ChatGPT, Claude, Make, Notion IA, Midjourney, etc.)
- Etudes et rapports (Anthropic, OCDE, McKinsey, FMI, Cognizant, PwC, LinkedIn)
- Freelance et IA (devenir consultant IA, facturer plus cher)
- Etudes et diplomes (obsolescence, livre Laurent Alexandre)
- Marche de l'emploi IA en France (chiffres, tendances, recrutement)
- Temoignages et histoires de reconversion
"""


def generate_topics():
    """Call Claude to generate 100 article topics."""
    if not ANTHROPIC_API_KEY:
        print("Erreur: ANTHROPIC_API_KEY manquant dans .env")
        sys.exit(1)

    prompt = f"""Tu es un expert SEO francais. Genere exactement 100 sujets d'articles de blog SEO pour le projet suivant :

{SITE_CONTEXT}

Pour chaque article, donne :
- title : titre SEO accrocheur (< 70 caracteres)
- keywords : 3-5 mots-cles separes par des virgules
- category : une des categories listees
- blog : "principal"

Regles :
- Varie les intentions de recherche : informationnelle, transactionnelle, comparatif, guide, liste
- Inclus des articles sur les metiers specifiques (au moins 20 fiches metier)
- Inclus des articles "guide complet", "top N", "comparatif", "etude", "temoignage"
- Couvre les 8 categories de maniere equilibree
- JAMAIS de doublon de sujet
- Titres en francais avec accents corrects
- JAMAIS de tiret cadratin dans les titres

Reponds UNIQUEMENT avec un JSON array valide, sans commentaire :
[
  {{"title": "...", "keywords": "...", "category": "...", "blog": "principal"}},
  ...
]
"""

    print("Generation de 100 sujets via Claude API...")
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 16000,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=300,
    )
    response.raise_for_status()

    text = response.json()["content"][0]["text"]

    start = text.find("[")
    end = text.rfind("]") + 1
    if start == -1 or end == 0:
        print("Erreur: pas de JSON valide dans la reponse")
        print(text[:500])
        sys.exit(1)

    articles = json.loads(text[start:end])

    # Assign rotating authors
    authors = [
        "Camille Renard",
        "Theo Marchand",
        "Sarah Bellamy",
    ]

    for i, article in enumerate(articles):
        article["index"] = i + 1
        article["published"] = False
        article["published_at"] = None
        article["slug"] = None
        article["scheduled_date"] = None
        article["scheduled_time"] = None
        article["scheduled_datetime"] = None
        article["title_tag"] = None
        article["meta_description"] = None
        article["featured_image_url"] = None
        article["author"] = authors[i % len(authors)]

    with open(ARTICLES_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

    print(f"OK - {len(articles)} articles generes dans {ARTICLES_FILE}")
    print(f"\nProchaine etape : python scheduler.py")


if __name__ == "__main__":
    generate_topics()
