# Information Architecture — Connect by Dimagi Marketing Site

Updated 2026-04-29 for v10 generation (canopy v0.2.66). Adds:
- `/insights` index page (required, not optional)
- Homepage Trail Teasers table — every homepage→depth link is a verbatim
  scoped claim, not a generic CTA
- Open Questions Roster — every depth page lists 1–3 specific open questions,
  sourced from insight caveats and nugget caveats
- Pattern assignments for v10a (Foundation memo) / v10b (Field dispatch) /
  v10c (Knowledge graph)

Earlier (v7): insight-driven content model with learning presentation
patterns per variant.

**Key shift from v6 → v7:** Pages are no longer collections of stats and facts.
On sub-pages (LDVP, program details), each insight is treated as a case entry
of 250-600 words with structure that rewards both skimming and close reading.
The visitor has already committed by reaching this page — substance, not hooks.

The source of truth for what gets written on pages is now `./context/insights.md`
(ten extracted learnings in "what we thought / what we learned / what we changed"
form). The source of truth for how insights are presented is the pattern choice
per variant × page-template below.

## Sitemap

| Page | Path | Template | Content Source | Status |
|------|------|----------|---------------|--------|
| Homepage | `/index.html` | homepage | pages/homepage.md + stats from LDVP + programs/_index.md | Ready |
| Learn | `/learn.html` | ldvp-step | pages/learn.md | Ready (rich) |
| Deliver | `/deliver.html` | ldvp-step | pages/deliver.md | Ready (rich) |
| Verify | `/verify.html` | ldvp-step | pages/verify.md | Ready (rich) |
| Pay | `/pay.html` | ldvp-step | pages/pay.md | Ready (rich) |
| Programs | `/programs.html` | program-catalog | programs/_index.md | Ready |
| KMC | `/programs/kmc.html` | program-detail | programs/kmc/* | Ready (rich — blog narrative) |
| Readers | `/programs/readers.html` | program-detail | programs/readers/* | Ready (overview only) |
| ECD | `/programs/ecd.html` | program-detail | programs/ecd/* | Ready (rich — pilot data) |
| CHC | `/programs/chc.html` | program-detail | programs/chc/* | Ready (rich — microplanning, FP report) |
| Insights | `/insights.html` | insights-index | nuggets.md + insights.md | Ready (required — v10) |

**Programs in catalog only (no detail page):** MBW, Chlorine, WellMe, RUTF, Interviews, Rooftop Sampling — show as "Coming soon" cards.

## Homepage Trail Teasers (v10 — required)

For every homepage section linking to a depth page, the verbatim teaser text.
Every teaser must be a specific scoped claim ≥8 words containing a number,
mechanism, or named decision. Generic CTAs ("Learn more", "Explore",
"Discover", category-only labels) are forbidden — the website-builder lints
the generated HTML against this list.

| Section → target | Teaser (verbatim, used as link text) |
|------------------|--------------------------------------|
| Hero proof → /verify | "We paid FLWs bonuses to defeat our fraud detection — they couldn't. 97.5% scored cleaner than the lowest fabricator. →" |
| Programs card → /programs/chc | "In CHC, microplans tripled visits-per-child from 0.4 to 1.4 and pushed coverage from 84% to 94%. →" |
| Programs card → /programs/kmc | "KMC reduces neonatal mortality up to 40%, yet global coverage is below 5% — we close the post-discharge gap. →" |
| Programs card → /programs/ecd | "Caregivers' ECD attitudes were already correct — we moved knowledge +33% and observed teaching behavior +21%. →" |
| Programs card → /programs/readers | "RestoringVision's 15,000 reading-glasses pairs delivered through Connect's verified-payment model. →" |
| LDVP → /learn | "Knowledge tests didn't produce competent FLWs — we layered an AI coach. 88% score above 70% on first observed visits. →" |
| LDVP → /deliver | "We invented the Trial Run because pre-vetting LLOs didn't predict performance — 65% conversion through it. →" |
| LDVP → /verify | "Workers naturally cluster — microplans force them into harder areas, and fraud detection hits AUC 0.91. →" |
| LDVP → /pay | "In CHC, cost per verified visit fell 22% — Nigeria $1.30 with ORS, outside Nigeria $0.78 without. →" |
| Methodology → /insights | "Every claim, scoped to its evidence — the buffet view of what we've learned across programs. →" |

## Open Questions Roster (v10 — required)

For every depth page, 1–3 specific unresolved tensions, in-progress
validations, or honest limitations. Sourced from insight caveats and
nugget caveats. Pages without an Open Questions block fail the build.
**Do not invent open questions.**

| Page | Open Question 1 | Open Question 2 | Open Question 3 |
|------|----------------|----------------|----------------|
| /learn | Whether the AI coach or peer practice contributes more to the 77% supervised-observation pass rate — we have not yet published the decomposition. | Whether the 97.8% AI-coach handle rate from the Kenya CHC pilot holds in non-English-language deployments. | Encouragement-of-autonomy is the hardest ECD sub-domain (47% endline). Whether 8–10 visits will move it, or it needs a different design entirely. |
| /deliver | Whether the 65% Trial Run conversion holds outside CHC — KMC, ECD, and Readers are still on too small a contract base to publish their own. | "Fragile context requires in-country presence" is a coarse rule learned from CAR. We don't have a sharper predictive model yet. | We have not built a structured framework for capturing what individual LLOs invent locally — the real intervention often lives in their heads. |
| /verify | The 97.5% adversarial detection is from paid-bonus testing in CHC. Production false-positive rates against unmotivated fabrication aren't yet published. | Microplans failed in dispersed settlement patterns. We don't yet have a clean threshold for when settlement density makes microplanning counterproductive. | Photo verification quality degrades on low bandwidth. False-positive rate on the photo layer in low-bandwidth deployments isn't yet published. |
| /pay | The $1.70 weighted average masks bundle differences ($1.30 Nigeria with ORS, $0.78 outside). Whether the 22% year-over-year curve holds in non-CHC programs is open. | The N=24 displacement survey is in two Nigerian states. Whether "campaigns are routine" holds in CHV systems with different structures — re-survey first. | Setup-fee projection ($0.40 → ~$0.10/visit at scale) is forward-looking. We will publish the converged number when the next cohort closes. |
| /programs/chc | Whether the cost-per-verified-visit advantage holds outside Nigeria's commodity bundle — IPA RCT 2026 ($1.5M, PRO Impact) will test. | The 65% Trial Run conversion criteria are program-manager judgment calls today, not codified into a model an outside funder could replicate. | Microplan execution failed in CAR's dispersed settlement and on inaccessible land. We removed it from one campaign entirely. |
| /programs/kmc | Whether discharge-notification integration alone closes the 50% → 70% within-3-days enrollment gap, or the 3-day target itself needs to be redesigned. | Equipment availability across the 6 KMC LLO partners has been uneven. We don't yet have a published audit of equipment uptime. | Whether KMC FLWs will sustain ≥4 visits per case at the 5,000+ scale; current average is 3.4 against a 5-visit guardrail. |
| /programs/ecd | The 47% endline on encouragement-of-autonomy is the hardest sub-domain. Whether 8–10 visits will move it is open. | The Malawi pilot is N=50 caregivers. Whether the attitude-already-correct finding holds in Mozambique and Nigeria contexts is open. | Whether AI coach contribution to the 77% pass rate generalizes outside ECD — we have not run the controlled comparison. |
| /programs/readers | LLOs finalized (eHA, C3HD); contract signing pending. Field-performance data won't exist until the first cohort runs. | Whether the screening protocol holds quality consistency across novice FLWs trained only digitally — first cohort will tell. | Whether door-to-door distribution finds the right adults (35+, presbyopic) at sufficient rates without targeting infrastructure. |
| /insights | This page is only as honest as the insights and nuggets the team mines. Internal lore that didn't make it onto the public site is the rate-limiter, not the format. | Numbers without benchmarks are excluded by policy — but our benchmark library is uneven across programs. KMC and Readers have thinner comparators than CHC. | Whether the methodology-footer framing ("we have a methodology for what's on the website") survives a year of new programs without drift toward marketing copy. |

## Navigation

### Primary Nav
- Logo (left, links to `/`)
- **How It Works** → dropdown: Learn, Deliver, Verify, Pay
- **Programs** → `/programs.html`
- **Impact** → `/#impact` (homepage anchor)
- **Request a Demo** CTA (right, pill button, Mango background)

### Mobile Nav
Hamburger on right. Opens slide-in or full-screen overlay. All links stacked flat (no dropdown nesting on mobile).

### Breadcrumbs
- Program detail pages: `Programs > [Program Name]`
- LDVP pages: `How It Works > [Step Name]` (optional, depending on variant)

### Footer
Three-column layout:
- **Platform** — Learn, Deliver, Verify, Pay
- **Programs** — top 4 active programs with links
- **Connect** — Impact, About Dimagi, Request a Demo
- Logo + "by Dimagi" credit on left, copyright right

## Content Routing Table (critical for rich pages)

| Insight | Primary Source | Program Page | LDVP Page | Audience Angle |
|---------|---------------|-------------|-----------|----------------|
| 88% of FLWs scored >70% on first observed visits | ECD report | ECD | Learn | Proves digital training quality |
| 85% of FLWs progress from training to delivery | ECD report | ECD | Learn | — |
| AI coach handles 97.8% of queries without escalation | FP report / CLP | CHC | Learn AND Deliver | Shows ongoing support works |
| Digital resources rated 9-9.5/10 by new LLOs | CLP report | — | Learn AND Deliver | LLO self-service value |
| 94% population coverage with microplanning | FP report | CHC | Verify | Funders — equitable reach |
| 1.4 visits/child (microplan) vs 0.4 (no microplan) | FP report | CHC | Verify | Funders — thoroughness |
| AUC 0.91 fraud detection from 3 data elements | FP report | — | Verify | Funders — no fraud risk |
| 22% cost reduction per verified visit | FP report | CHC | Pay | Funders — ROI |
| $1.70 per verified visit (down from $2.20) | FP report | CHC | Pay | Funders |
| No displacement of routine health work | GiveWell survey | CHC | Pay | FLWs — income benefit |
| FLWs report substantial income increase | GiveWell survey | — | Pay | FLWs |
| KMC reduces neonatal mortality by 40% | KMC blog | KMC | — | Impact argument |
| KMC coverage remains <5% globally | KMC blog | KMC | — | Why program matters |
| 880K+ visits in 14 months | FP report | CHC | Deliver | Scale argument |
| 44 LLOs activated in 14 months | FP report | CHC | Deliver | LLO scalability |
| Trial Run model: 65% pass rate | FP report | CHC | Deliver | How scaling works |
| ECD +33% caregiver knowledge, +41% understanding | ECD report | ECD | — | Program impact |
| ECD +21% teaching behavior observed | ECD report | ECD | — | Behavior change evidence |
| ECD cost: $7-$18 per child | ECD report | ECD | Pay | Cost-effectiveness |
| 5 structured home visits per SVN (KMC) | KMC blog | KMC | Deliver | Service depth |
| KMC FLW equipment: scale, thermometer, pulse oximeter | KMC overview | KMC | Deliver | Tangible details |

## Design Directions (three variants to generate)

The generator MUST NOT lock in on one approach. Produce three distinctive sites that differ in **aesthetic direction AND content emphasis**.

### Variant A: "Editorial / Narrative-first"
- **Aesthetic:** Magazine-like. Large editorial typography. Full-bleed photography. Generous whitespace alternating with dense data blocks.
- **Content emphasis:** Lead with the human story. KMC page opens with "2.3 million newborns die in the first 28 days…" CHC opens with the coverage gap. Narrative arc drives each page.
- **Key moves:**
  - Hero: editorial headline, small tagline, single CTA
  - LDVP: each step gets a full-width section with a pull quote from the reports
  - Programs: each detail page structured like a feature article (lede, context, body, evidence, call to action)
  - Typography: Work Sans with heavy contrast (200 for display, 600 for emphasis)
- **Think:** New York Times Magazine piece on global development.

### Variant B: "Dashboard / Data-first"
- **Aesthetic:** Clean, information-dense. Stat cards, charts, tables. Thin borders, lots of numbers at large sizes.
- **Content emphasis:** Lead with evidence. Every page opens with a metric. Every claim backed by a number. Sources cited inline.
- **Key moves:**
  - Hero: single huge number ("880,000+") with surrounding context
  - LDVP: each step opens with a stats ribbon, then explains mechanism
  - Verify page gets a special treatment — showing the fraud detection AUC, microplanning coverage chart, etc.
  - Programs: each detail page leads with a key-metrics row (like a research paper)
- **Think:** The Gates Foundation annual report, or Our World in Data.

### Variant C: "Modular / Platform-first"
- **Aesthetic:** Bold, modern, product-focused. Gradients, geometric shapes, animated interactions. Feels like a B2B SaaS product page.
- **Content emphasis:** Lead with the mechanism. Connect is a platform that composes — show the LDVP cycle as a diagram. Programs are apps running on the platform.
- **Key moves:**
  - Hero: gradient background, animated LDVP diagram, "Powering the Frontline" headline
  - LDVP: each step has a visual component (icon, diagram, or mini-interaction) + a demo-style description
  - Programs: each detail page treats the program as a "case study" showing how the platform was applied
  - Deliver page gets special treatment — showing microplanning grid, LLO activation model as a funnel
- **Think:** Stripe, Linear, or Anthropic — technical products with aesthetic polish.

## Learning Presentation Patterns

**The substance rule:** On sub-pages, each insight from `./context/insights.md`
becomes a section of **250-600 words** with internal structure. No one-liner
pull quotes, no 20-word stat cards standing in for content. The visitor has
clicked in — reward the commitment.

### Pattern Assignments per Variant × Page-Template

| Variant | Homepage | LDVP sub-pages | Program detail pages |
|---------|----------|----------------|---------------------|
| **v7a Editorial** | Hero + teasers only (homepage stays light) | **Pattern B: Two-Column Long-Form** — body text left, supporting material (methodology notes, specific numbers, pull quotes drawn from body) right | **Pattern E: Question-Led** — each program frames 3-4 learnings as questions (e.g., "How do you scale KMC when global coverage is below 5%?") with 300-500 word answers |
| **v7b Dashboard** | Hero + teasers only | **Pattern A: Engineering Retrospective** — each learning as a structured entry: The question / What we tried / What we found / What changed / What's still open, with data in prose and sources at bottom | **Pattern C: Annotated Discovery** — clean narrative surface with inline source markers (superscripts or small underlines) revealing citation, methodology, or caveat on hover |
| **v7c Platform** | Hero + teasers only | **Pattern D: Progression of Thinking** — each learning as a timeline ("Q1 2025: we assumed X. By Q3, data suggested Y. By 2026, we'd redesigned to Z"), showing how the team's thinking evolved with data at each phase | **Pattern E: Question-Led** — each program as a case study of how the platform answered a specific delivery question |
| **v10a Foundation memo** | Hero + verbatim trail teasers, dense and serif, footnoted | **Pattern C: Annotated Discovery** — clean serif prose with superscript citations and inline source notes; reads like a Gates Foundation internal memo | **Pattern C: Annotated Discovery** — same Pattern C treatment for program detail, with inline footnotes |
| **v10b Field dispatch** | Hero + verbatim trail teasers, journal voice, large editorial typography | **Pattern D: Progression of Thinking** — timeline of how the team's thinking evolved on each LDVP step | **Pattern B: Two-Column Long-Form** — body on left, methodology/quotes on right; each program reads like a New Yorker dispatch |
| **v10c Knowledge graph** | Hero + verbatim trail teasers, dense interlinked layout, evidence tier badges visible from homepage | **Pattern A: Engineering Retrospective** — each learning has structured headings (question / what we tried / what we found / what changed / what's still open) and a visible evidence-tier badge | **Pattern E: Question-Led** — each program frames 3–4 questions, each with an evidence-tier badge, deep-link nuggets are first-class navigation |

### Which Insights Go Where (from insights.md)

**LDVP sub-pages get:**
- **Learn page** — Insight 8 (Knowledge tests ≠ competence) + Insight 7 (ECD: attitudes already correct, behavior is the gap, informing what Learn must do)
- **Deliver page** — Insight 1 (LLO Trial Run model) + Insight 6 (LLOs leverage community/religious leaders independently) + Insight 9 (CAR failure and in-country presence)
- **Verify page** — Insight 2 (Workers cluster; microplans push outward) + Insight 3 (Adversarial fraud testing) + Insight 10 (Guardrails vs hard stops — design philosophy)
- **Pay page** — Insight 4 (Connect inverts the scaling-cost pattern) + Insight 5 (No displacement of routine health work — questioned Western assumption)

**Program detail pages get:**
- **KMC** — Insight 10 (Guardrails philosophy applied to 4-visit minimum) + learnings specific to KMC enrollment gap (50% vs 70% target) + WHO alignment arc
- **CHC** — Insight 1 (Trial Run) + Insight 2 (Microplanning) + Insight 3 (Adversarial testing) + Insight 4 (Cost inversion) + Insight 6 (Religious leaders) — CHC is the richest source, supports 4-5 learnings
- **ECD** — Insight 7 (Attitudes vs knowledge) + Insight 8 (Knowledge ≠ competence, AI coach layered model)
- **Readers** — Less learning-rich; present as "platform applied to a new domain" with inline notes on what we'll learn as the campaign runs

Each learning section starts with its own subheading and weighs 250-600 words. A
program detail page with 4 learnings runs ~1,200-2,000 words of substance. A
LDVP page with 3 learnings runs ~900-1,500 words. This is not too long for a
committed reader — it's what they came for.

## Page Templates (shared across variants)

### Homepage
- Hero (tagline + pitch + CTAs)
- How It Works overview (links to 4 LDVP pages)
- Impact stats (4-6 headline numbers)
- Programs showcase (catalog grid)
- Audiences (Funders / LLOs / Workers)
- CTA / contact
- Footer

### LDVP Step Page
- Hero (step name, core message)
- Three features/pillars
- Evidence section (pulled from reports, per Content Routing table)
- Supporting sections specific to the step (microplanning on Verify, cost table on Pay, etc.)
- Next step CTA (sequential: Learn → Deliver → Verify → Pay → Programs)

### Program Catalog
- Hero (title, one-line description)
- Grid of all 10 programs
- Each card: name, sector, regions, scale, link (for the 4 with detail pages) or "Coming soon" badge

### LDVP Step Page (v7 — insight-heavy)
- Hero (step name, core message, 1-2 headline numbers)
- **3 learning sections** (250-600 words each, per variant's presentation pattern) — drawn from the insights routed to this page
- Each learning section has internal structure: subheading, specific data, caveats, "what's next" where applicable
- Source citations per learning (at bottom of section, small grey text)
- Next step CTA (sequential: Learn → Deliver → Verify → Pay → Programs)

Total length per LDVP page: ~900-1,500 words of substance.

### Program Detail (v7 — insight-heavy)
- Hero (program name, one-line tagline)
- Key metrics row (4-6 numbers specific to the program)
- The Challenge (why this program exists — problem statement, ~200 words)
- How It Works (implementation mechanics, 4-5 blocks)
- **3-5 learning sections** (250-600 words each, per variant's presentation pattern) — drawn from insights.md + program-specific learnings. For rich programs (CHC, KMC, ECD) aim for 4-5 learnings; for Readers aim for 2-3.
- Program Details (metadata: regions, funder, partners, standards)
- Resources (public links only — YouTube videos for KMC/CHC; others blank)
- Back to catalog CTA

Total length per program detail page: ~1,200-2,000 words of substance.

## Media Placement

Public video URLs — safe to embed or link:
- **KMC detail page:** Embed/link https://www.youtube.com/watch?v=o1nHOWhInbY (Ugandan National TV PIPNU interview)
- **CHC detail page:** Embed/link https://www.youtube.com/watch?v=VRbvUj9LTUg (Inside CHC Kenya)
- **Homepage hero / Deliver page:** Embed/link https://www.youtube.com/watch?v=oiUuT5v6ir0 (CommCare Connect Demo)

Internal links (NEVER as public href):
- Google Drive folders
- Google Docs (EOI responses, internal reports)
- Salesforce, Asana
- Any docs tagged [Internal], [WIP]

## Content Gaps & Handling

- **Readers detail page** — thin on evidence; no public resources. Handle by emphasizing the model and the Restoring Vision partnership rather than pilot results.
- **MBW, Chlorine, WellMe, RUTF, Interviews, Rooftop Sampling** — only basic metadata. Show as "Coming soon" or "Launching 2026" cards in the catalog; don't attempt detail pages.
- **Homepage impact stats** — draw from the Content Routing table. Don't invent numbers.

## Output Structure

Each variant generates:
```
v10X/
  index.html
  learn.html
  deliver.html
  verify.html
  pay.html
  programs.html
  insights.html         (NEW — required v10)
  programs/
    kmc.html
    readers.html
    ecd.html
    chc.html
  styles.css
```

Total: 11 HTML files + 1 CSS per variant × 3 variants = 33 pages, 3 CSS files.

## /insights Page Template (v10 — required)

Hero: "What we've learned" + one-sentence framing.

Index (the buffet): every Kept insight from `insights.md` and every
above-threshold nugget from `nuggets.md` listed as a one-sentence teaser
with Scope, source link, and an optional Open Question.

Grouped by Scope. Programs first (CHC, ECD, KMC, Readers), then Platform
mechanisms. Within each group, ordered by judge-anticipated score
descending.

Methodology footer: a paragraph explaining what makes the cut — claims
scoped to evidence, numbers carry benchmarks, in-validation findings
named with the evaluation underway.

Per Pattern assignments:
- **v10a:** Annotated Discovery — clean prose surface, inline source markers
- **v10b:** Field-dispatch journal voice — each entry as a stub of a longer story
- **v10c:** Evidence-tier badges visible on every entry, deep-link anchors
