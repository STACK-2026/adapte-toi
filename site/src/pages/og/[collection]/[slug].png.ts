import satori from "satori";
import { Resvg } from "@resvg/resvg-js";
import fs from "node:fs";
import path from "node:path";
import { getCollection } from "astro:content";
import type { APIRoute } from "astro";

const fontsDir = path.join(process.cwd(), "src", "assets", "fonts");
const INTER_600 = fs.readFileSync(path.join(fontsDir, "Inter-600.woff"));
const INTER_700 = fs.readFileSync(path.join(fontsDir, "Inter-700.woff"));
const INTER_800 = fs.readFileSync(path.join(fontsDir, "Inter-800.woff"));

type Palette = { from: string; to: string; accent: string; pillBg: string };

const BRAND_PRIMARY = "#e63946";
const BRAND_SECONDARY = "#1d3557";
const BRAND_ACCENT = "#f77f00";

const PALETTES: Record<string, Palette> = {
  actu: { from: "#1d3557", to: "#0d1b2a", accent: BRAND_ACCENT, pillBg: "rgba(247,127,0,0.18)" },
  guides: { from: "#1d3557", to: "#14213d", accent: "#a8dadc", pillBg: "rgba(168,218,220,0.15)" },
  metiers: { from: "#0d1b2a", to: "#1d3557", accent: BRAND_PRIMARY, pillBg: "rgba(230,57,70,0.18)" },
  outils: { from: "#14213d", to: "#1d3557", accent: BRAND_ACCENT, pillBg: "rgba(247,127,0,0.18)" },
  default: { from: "#1d3557", to: "#0d1b2a", accent: BRAND_ACCENT, pillBg: "rgba(247,127,0,0.18)" },
};

const COLLECTION_LABELS: Record<string, string> = {
  actu: "Actu",
  guides: "Guide",
  metiers: "Metier",
  outils: "Outil IA",
};

const ACTU_CAT_LABELS: Record<string, string> = {
  menace: "Menace",
  etude: "Etude",
  annonce: "Annonce",
  politique: "Politique",
  outil: "Outil",
  voix: "Voix",
  chiffre: "Chiffre",
};

const RISK_LABELS: Record<string, string> = {
  faible: "Risque faible",
  moyen: "Risque moyen",
  eleve: "Risque eleve",
  "tres-eleve": "Risque tres eleve",
};

export async function getStaticPaths() {
  const paths: Array<{
    params: { collection: string; slug: string };
    props: { title: string; collection: string; pills: string[] };
  }> = [];

  const actu = await getCollection("actu", ({ data }) => !data.draft);
  for (const post of actu) {
    const cat = post.data.category;
    const impact = post.data.impactLevel;
    paths.push({
      params: { collection: "actu", slug: post.id },
      props: {
        title: post.data.title,
        collection: "actu",
        pills: [COLLECTION_LABELS.actu, ACTU_CAT_LABELS[cat] ?? cat, `Impact ${impact}/5`],
      },
    });
  }

  const guides = await getCollection("guides", ({ data }) => !data.draft);
  for (const post of guides) {
    const cat = post.data.category ?? "Strategie";
    paths.push({
      params: { collection: "guides", slug: post.id },
      props: {
        title: post.data.title,
        collection: "guides",
        pills: [COLLECTION_LABELS.guides, cat],
      },
    });
  }

  const metiers = await getCollection("metiers", ({ data }) => !data.draft);
  for (const post of metiers) {
    paths.push({
      params: { collection: "metiers", slug: post.id },
      props: {
        title: post.data.title,
        collection: "metiers",
        pills: [
          COLLECTION_LABELS.metiers,
          post.data.sector,
          RISK_LABELS[post.data.riskLevel] ?? post.data.riskLevel,
        ],
      },
    });
  }

  const outils = await getCollection("outils", ({ data }) => !data.draft);
  for (const post of outils) {
    const rating = post.data.rating ? `${post.data.rating}/10` : null;
    const pills = [COLLECTION_LABELS.outils, post.data.category];
    if (rating) pills.push(rating);
    paths.push({
      params: { collection: "outils", slug: post.id },
      props: {
        title: post.data.title,
        collection: "outils",
        pills,
      },
    });
  }

  return paths;
}

export const GET: APIRoute = async ({ props }) => {
  const { title, collection, pills } = props as {
    title: string;
    collection: string;
    pills: string[];
  };
  const p = PALETTES[collection] ?? PALETTES.default;
  const safePills = pills.filter(Boolean).slice(0, 3);

  const svg = await satori(
    {
      type: "div",
      props: {
        style: {
          display: "flex",
          flexDirection: "column",
          width: "1200px",
          height: "630px",
          backgroundImage: `linear-gradient(135deg, ${p.from} 0%, ${p.to} 100%)`,
          padding: "64px",
          fontFamily: "Inter",
          color: "white",
          position: "relative",
        },
        children: [
          // Header : wordmark adapte-toi + accent dot
          {
            type: "div",
            props: {
              style: {
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                width: "100%",
              },
              children: [
                {
                  type: "div",
                  props: {
                    style: { display: "flex", alignItems: "center", gap: 16 },
                    children: [
                      // dot rouge brand
                      {
                        type: "div",
                        props: {
                          style: {
                            width: 18,
                            height: 18,
                            backgroundColor: BRAND_PRIMARY,
                            borderRadius: 999,
                          },
                        },
                      },
                      {
                        type: "div",
                        props: {
                          style: {
                            fontSize: 28,
                            fontWeight: 800,
                            letterSpacing: -0.5,
                            color: "white",
                          },
                          children: "adapte-toi",
                        },
                      },
                    ],
                  },
                },
                {
                  type: "div",
                  props: {
                    style: {
                      fontSize: 14,
                      fontWeight: 700,
                      letterSpacing: 4,
                      textTransform: "uppercase",
                      color: p.accent,
                    },
                    children: "L'IA et ton job en 2026",
                  },
                },
              ],
            },
          },
          { type: "div", props: { style: { flex: 1 } } },
          // Titre principal
          {
            type: "div",
            props: {
              style: {
                fontSize: title.length > 70 ? 52 : 60,
                fontWeight: 800,
                lineHeight: 1.08,
                letterSpacing: -1.5,
                maxWidth: "92%",
                color: "white",
              },
              children: title,
            },
          },
          // Pills meta
          {
            type: "div",
            props: {
              style: {
                display: "flex",
                gap: 12,
                marginTop: 36,
                flexWrap: "wrap",
              },
              children: safePills.map((label) => ({
                type: "div",
                props: {
                  style: {
                    padding: "10px 22px",
                    border: `1px solid ${p.accent}`,
                    backgroundColor: p.pillBg,
                    fontSize: 16,
                    fontWeight: 700,
                    letterSpacing: 1.5,
                    textTransform: "uppercase",
                    borderRadius: 999,
                    color: "white",
                  },
                  children: String(label),
                },
              })),
            },
          },
          // Stripe accent
          {
            type: "div",
            props: {
              style: {
                width: 140,
                height: 5,
                backgroundColor: p.accent,
                marginTop: 28,
              },
            },
          },
        ],
      },
    },
    {
      width: 1200,
      height: 630,
      fonts: [
        { name: "Inter", data: INTER_600, weight: 600, style: "normal" },
        { name: "Inter", data: INTER_700, weight: 700, style: "normal" },
        { name: "Inter", data: INTER_800, weight: 800, style: "normal" },
      ],
    }
  );

  const resvg = new Resvg(svg, { fitTo: { mode: "width", value: 1200 } });
  const png = resvg.render().asPng();

  return new Response(png, {
    headers: {
      "Content-Type": "image/png",
      "Cache-Control": "public, max-age=31536000, immutable",
    },
  });
};
