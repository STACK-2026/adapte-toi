#!/usr/bin/env python3
from pathlib import Path
import tempfile
import unittest

import content_guard


class EditorialGuardTests(unittest.TestCase):
    def analyze(self, frontmatter: str, body: str):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "article.md"
            path.write_text(f"---\n{frontmatter}\n---\n\n{body}\n", encoding="utf-8")
            issues, _, _ = content_guard.analyze(path, fix=False, check_links=False)
            return {code for code, _ in issues}

    def test_blocks_individual_article_byline(self):
        issues = self.analyze(
            'title: "Titre fiable"\ndescription: "Description fiable"\nauthor: "Prénom Persona"',
            "Un contenu éditorial suffisamment court pour ce test.",
        )
        self.assertIn("AUTHOR_POLICY", issues)

    def test_accepts_collective_article_byline(self):
        issues = self.analyze(
            'title: "Titre fiable"\ndescription: "Description fiable"\nauthor: "La Rédaction Adapte-toi"',
            "Un contenu éditorial suffisamment court pour ce test.",
        )
        self.assertNotIn("AUTHOR_POLICY", issues)

    def test_blocks_undisclosed_composite_testimonial(self):
        issues = self.analyze(
            'title: "Parcours de reconversion"\ndescription: "Description fiable"\ncategory: "temoignages"\nauthor: "La Rédaction Adapte-toi"',
            "Camille raconte son parcours, son salaire et ses résultats.",
        )
        self.assertIn("TESTIMONIAL_DISCLOSURE", issues)

    def test_accepts_disclosed_composite_testimonial(self):
        issues = self.analyze(
            'title: "Parcours de reconversion"\ndescription: "Description fiable"\ncategory: "temoignages"\nauthor: "La Rédaction Adapte-toi"',
            "Note de transparence : ce témoignage composite est une reconstitution éditoriale fondée sur plusieurs parcours documentés.",
        )
        self.assertNotIn("TESTIMONIAL_DISCLOSURE", issues)

    def test_fix_inserts_composite_disclosure(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "article.md"
            path.write_text(
                '---\ntitle: "Parcours"\ndescription: "Description"\n'
                'category: "temoignages"\nauthor: "La Rédaction Adapte-toi"\n---\n\n'
                "Camille raconte son parcours.\n",
                encoding="utf-8",
            )
            _, fixes, new_text = content_guard.analyze(path, fix=True, check_links=False)
            self.assertIn("added composite-testimonial disclosure", fixes)
            self.assertIn("Note de transparence", new_text)


if __name__ == "__main__":
    unittest.main()
