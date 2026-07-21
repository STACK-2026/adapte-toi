# Adapte-toi editorial, SEO and LLM glow-up

Date: 2026-07-21  
Owner: Codex, requested by the site owner  
Environment: Astro static site on Cloudflare Pages

## Outcome

Raise trust, search click-through potential, mobile quality and machine readability without changing the site's core visual identity or deleting published URLs.

## Scope

- Align public bylines and structured-data authorship with the published collective-signature policy.
- Make composite testimonials explicit and prevent undisclosed testimonial publication.
- Correct the verified BCG quotation mismatch and add automated editorial guardrails.
- Replace stale homepage claims with current, directly sourced July 2026 data.
- Fix News sitemap canonical URLs, Supabase CSP errors, known image-alt failures, weekly archive discoverability and homepage LCP animation behavior.
- Add a maintained `llms-full.txt` endpoint while keeping standard HTML, sitemaps and editorial quality as the primary SEO/GEO surfaces.
- Improve search snippets without rewriting every visible headline in one unsafe bulk pass.

## Non-goals

- No deletion or redirect of existing editorial URLs.
- No fabricated author biographies, testimonials, measurements or proprietary data.
- No visual redesign, CMS migration or analytics datastore migration.
- No claim that `llms.txt` or structured data directly improves rankings.

## Acceptance criteria

1. All article-level bylines resolve to the collective newsroom identity unless a future, documented exception is explicitly supported.
2. Every testimonial-category article contains a visible composite/anonymisation disclosure; the content guard blocks new undisclosed testimonials.
3. The known BCG quotation matches the primary BCG wording and attribution.
4. Homepage evidence is dated July 2026 and links to primary BCG data; unsupported April proprietary claims are removed from the homepage.
5. News sitemap locations are canonical 200 URLs with trailing slashes.
6. The public CSP permits only the Supabase origins actually used by the public site and produces no Supabase CSP console error.
7. The eight baseline image-alt failures and meaningful weekly archive orphan failures are removed.
8. Homepage reveal text is visible in initial HTML/CSS and animation is enhancement-only, reducing LCP delay.
9. `/llms-full.txt` builds as a 200 text resource containing current hubs, policies and recent editorial entries.
10. Content guard, Astro build, standards audit and orphan audit pass with no new blocking defect. Remaining intentional warnings are reported.

## Risk and rollback

Risk class: high for SEO-wide and public editorial changes; technically reversible through the prior production commit `ca316e1`.

- Failure mode: collective byline replacement changes attribution unexpectedly. Prevention: only top-level frontmatter `author` fields are changed; quoted-source authors remain untouched.
- Failure mode: testimonial disclosure overstates provenance. Prevention: label these pages as editorial composites rather than claiming interviews occurred.
- Failure mode: snippet truncation harms meaning. Prevention: keep visible titles unchanged and use deterministic word-boundary SEO titles only in metadata.
- Failure mode: CSP becomes too broad. Prevention: allow exact Supabase origins, not a wildcard.
- Rollback trigger: build failure, schema mismatch, canonical regression, homepage factual mismatch or materially worse Lighthouse result.
- Rollback: redeploy `ca316e1` or revert the glow-up commit.

## Implementation plan

1. Add RED checks to the content guard for non-collective article bylines and undisclosed testimonial content, then normalize the affected frontmatter and disclosures.
2. Add metadata-title clamping with focused deterministic tests/checks while preserving visible H1 text.
3. Correct homepage evidence, BCG quotation and public editorial copy.
4. Fix News sitemap URLs, CSP, image alts, weekly archive linking and animation-first-paint behavior.
5. Generate `llms-full.txt` from published collections and verify its build output.
6. Run guard, build, standards/orphan audits, metadata/canonical checks and Lighthouse preview/live checks before publishing.

