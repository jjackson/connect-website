# Nugget Candidates

Mined from internal sources (insights.md, program overviews, FP report, ECD report, KMC blog narrative, brand messaging). Each entry is a candidate for inclusion on a depth page (program detail, LDVP step, /insights). The information-architecture step routes them to specific pages and the website-builder's depth-sharpness eval scores whether they actually landed.

Mining run: 2026-04-29 (v10 generation, canopy v0.2.66).

## N1: 97.5% of real workers scored *cleaner* than even the lowest-scoring paid fabricator we hired

**Source:** insights.md Insight 3; CHC overview "Fraud Detection (Adversarial Testing)"; FP Final Report (Feb 2026)
**Scope:** Platform (mechanism is the same Random Forest pipeline regardless of program; tested in CHC)
**Surprise:** 5/5 — most platforms claim fraud detection without naming the test. Naming an adversarial paid red-team is rare.
**Publishability:** 5/5 — already documented in the public Founders Pledge final report; no PII.
**Suggested home:** /verify (signature story); /programs/chc (where it ran); /insights (top-line).
**Verbatim phrasing candidate:** "We paid experienced FLWs to fake 100 visit records each across three rounds and offered bonuses to the top 25% most convincing fabricators. Out of 33 adversarial fakers, 97.5% of real workers scored *cleaner* than even the lowest-scoring fabricator — using just three data points (age, gender, MUAC). AUC 0.91 ± 0.09."
**Caveats / what's still unproven:** That 97.5% is on adversarial paid-bonus testing in CHC. The production false-positive rate against unmotivated fabrication has not been published; we will when we have a clean cohort comparison.

## N2: Microplanning produced a 3.5× increase in visits-per-child — 1.4 vs 0.4

**Source:** insights.md Insight 2; CHC overview "Coverage Results"; FP Final Report
**Scope:** CHC (the 0.4 → 1.4 numbers are CHC measurements; microplanning is portable)
**Surprise:** 4/5 — most "coverage" claims don't quantify the cluster behavior they're correcting.
**Publishability:** 5/5 — already in published FP report.
**Suggested home:** /verify (named example "In CHC…"); /programs/chc (the innovation); /insights.
**Verbatim phrasing candidate:** "Without microplans, FLWs in CHC averaged 0.4 visits per estimated eligible child — they cherry-picked accessible households. With microplans forcing them to close every Delivery Unit before unlocking the next Service Area, they hit 1.4 visits per child. A 3.5× thoroughness gain, and population coverage rose from 82–84% to 94%."
**Caveats / what's still unproven:** Microplans failed in dispersed settlement patterns and on inaccessible land (one campaign removed microplan execution entirely). We don't yet have a clean threshold for when settlement density makes microplanning counterproductive.

## N3: We measure verified-visit cost, not enrolled-FLW cost — and CHC fell 22% as it scaled

**Source:** insights.md Insight 4; CHC overview "Cost Reduction"
**Scope:** CHC (the 22%, $2.20→$1.70 numbers are CHC during the FP grant period)
**Surprise:** 4/5 — most NGOs report cost-per-enrolled-worker; cost-per-verified-outcome is harder.
**Publishability:** 5/5 — public in FP report.
**Suggested home:** /pay (named "In CHC…"); /programs/chc; /insights; /audiences/funders.
**Verbatim phrasing candidate:** "In the CHC program, cost per *verified* visit fell 22% — from $2.20 to $1.70 — as the program scaled. Connect's architecture (LLO economics + performance-based payment + integrated tooling) is designed to produce cost-reducing scale; CHC is the program where we've measured it. The cost-per-activity number, which most platforms publish, hides this asymmetry."
**Caveats / what's still unproven:** The $1.70 weighted average masks commodity bundle differences ($1.30 in Nigeria with ORS/Zinc co-packs; $0.78 outside Nigeria with VAS+deworming only). Whether the same year-over-year curve holds in non-CHC programs is an open question.

## N4: We invented the Trial Run because pre-vetting LLOs didn't predict performance

**Source:** insights.md Insight 1; CHC overview "LLO Activation Model"
**Scope:** Platform (Trial Run model has been reused across CHC, Readers, KMC, chlorine work)
**Surprise:** 4/5 — funders typically require deep pre-qualification; the explicit reframe is valuable.
**Publishability:** 5/5 — already public in FP report and EOI documents.
**Suggested home:** /deliver (the operational insight); /programs/chc; /audiences/funders; /insights.
**Verbatim phrasing candidate:** "Conventional procurement says vet partners thoroughly before contracting. We tried it. Past reputation, team size, organizational maturity — none of it reliably predicted whether an LLO would actually deliver. So we invented the Trial Run: $3,000 setup for 3,000 verified child visits. Of 37 contracted LLOs in CHC, 24 ran Trials, 10 underperformed and were not continued, 3 went straight to larger campaigns based on prior measured performance."
**Caveats / what's still unproven:** Trial Run requires baseline connectivity and LLO staffing capacity. In CAR, both contracted LLOs dropped out — we now flag fragile contexts as needing dedicated in-country presence before activation.

## N5: Knowledge ≠ competence — and we have ~400 FLWs of evidence

**Source:** insights.md Insight 8; ECD overview "Digital Upskilling for FLWs"
**Scope:** Platform (the layered Learn→test→AI coach→peer practice→supervised observation pipeline runs on every deployment)
**Surprise:** 3/5 — practitioners know this; foundation officers may not have seen it explicitly named.
**Publishability:** 5/5 — discussed in ECD report and CLP Stage 2 report.
**Suggested home:** /learn (the methodology); /programs/ecd (the example); /insights.
**Verbatim phrasing candidate:** "Workers who aced our digital knowledge test still struggled with the nuances of in-person counseling. So we layered the model: self-paced learning, in-app test, daily AI coach interaction (Open Chat Studio), peer practice, one supervised observation visit. 85% of FLWs progress to service delivery; 88% score above 70% on first observed visits. Validated across 400+ FLWs through iterative experiments."
**Caveats / what's still unproven:** The 77% supervised-observation pass rate is the binding constraint — we have not yet published a clean comparison of AI-coach vs. peer-practice contributions to that figure.

## N6: Caregivers' attitudes were already correct — we moved knowledge and behavior, not beliefs

**Source:** insights.md Insight 7; ECD overview "Pilot Results"
**Scope:** ECD (Malawi pilot, 50 caregiver surveys)
**Surprise:** 5/5 — almost every ECD pitch leads with "we shift attitudes." Naming the floor effect is rare.
**Publishability:** 5/5 — published in ECD report.
**Suggested home:** /programs/ecd (the pilot insight); /learn (named example); /insights.
**Verbatim phrasing candidate:** "Our Malawi ECD pilot (76 FLWs, 9,510+ visits, 50-caregiver baseline/endline) found nearly all caregivers *already* held positive ECD attitudes at baseline. The intervention didn't need to convince them — it needed to close the gap between belief and practice. Knowledge of rapid-development timing rose +33%; observed teaching behavior +21%; encouragement of autonomy +21% but still only 47% at endline. So we doubled the dosage from 3 visits to 8–10 across 12 months."
**Caveats / what's still unproven:** Encouragement of autonomy (47% endline) is the hardest sub-domain. We don't yet know whether 8–10 visits will move it, or whether it requires a different intervention design entirely.

## N7: LLOs invented vaccine-hesitancy outreach with religious leaders before we asked

**Source:** insights.md Insight 6; CLP Stage 2 report
**Scope:** CHC (CLP Stage 2 vaccine campaign, 7 LLOs)
**Surprise:** 4/5 — names the L in LLO doing real work, with a specific count.
**Publishability:** 4/5 — public in CLP Stage 2 report.
**Suggested home:** /deliver (why locally-led matters); /programs/chc; /insights.
**Verbatim phrasing candidate:** "Of 7 LLOs in our CLP Stage 2 vaccine campaign (CHC), 5–6 independently leveraged religious leaders, community leaders, or existing community relationships to navigate vaccine hesitancy. They did this before we asked. One FLW countered hesitancy with a personal example: 'We were immunized, we have children.' Another LLO sourced FLWs the community itself recommended. The platform's job is to enable this, not to centralize it."
**Caveats / what's still unproven:** We have not built a structured framework for capturing or sharing what individual LLOs invent locally — the "real intervention" is in their heads, not in our app.

## N8: Both LLOs in CAR dropped out — we now flag fragile contexts as needing in-country presence

**Source:** insights.md Insight 9; CHC overview (vaccine campaign work)
**Scope:** CHC (CAR vaccine-campaign cohort)
**Surprise:** 5/5 — explicitly publishing failure is rare.
**Publishability:** 4/5 — discussed in FP report; sensitive but reported.
**Suggested home:** /deliver (named example, "what's next" aside); /programs/chc; /insights.
**Verbatim phrasing candidate:** "In the Central African Republic, both contracted LLOs in our CHC vaccine work dropped out — staffing and connectivity issues. Remote coordination wasn't enough. We've now flagged fragile contexts as requiring dedicated in-country presence before activation; we don't repeat the same model in similarly difficult geographies."
**Caveats / what's still unproven:** "In-country presence" is a coarse rule. We don't yet have a sharper predictive model for which fragile-context features make remote coordination fail.

## N9: We pay 65% of LLOs; the other 35% don't make it past Trial Run — and we don't keep contracting them

**Source:** insights.md Insight 1; CHC overview
**Scope:** CHC (37 contracted; 24 Trials; 14 completed campaigns; 65% conversion)
**Surprise:** 4/5 — a specific failure rate, published.
**Publishability:** 5/5 — public in FP report.
**Suggested home:** /deliver; /programs/chc; /audiences/funders.
**Verbatim phrasing candidate:** "107 EOI applications. 37 contracted under Trial Run terms. 24 advanced to full Trials. 14 passed and ran larger campaigns. The 35% that didn't pass aren't continued. We publish this conversion rate because diligence readers ask about it."
**Caveats / what's still unproven:** The selection criteria that drive the 65% are not yet codified into a model an outside funder could replicate; today they're judgment calls by program managers.

## N10: Guardrails are not hard stops — and KMC is currently failing one (50% vs 70% target)

**Source:** insights.md Insight 10; KMC overview "Early Performance"
**Scope:** Platform philosophy; KMC for the live numbers
**Surprise:** 4/5 — naming a current performance gap on a marketing site is rare.
**Publishability:** 4/5 — KMC numbers are in conceptual model; comfortable publishing.
**Suggested home:** /verify (the design philosophy); /programs/kmc (the live example); /insights.
**Verbatim phrasing candidate:** "KMC has 4 mandatory home visits per SVN as a payment criterion. Its 'first visit within 3 days of discharge' is a guardrail — audited, not enforced. Current performance: 50% against a 70% target. We don't punish FLWs for missing it because punishment trains workers to falsify dates. We coach, integrate discharge notifications, and track. Platforms that punish guardrails don't get honest data."
**Caveats / what's still unproven:** Whether 70% is achievable through coaching plus discharge-notification integration alone, or whether the 3-day window itself needs to be redesigned for the realities of post-discharge timing.

## N11: KMC reduces neonatal mortality up to 40% — and yet global coverage is below 5%

**Source:** KMC overview; KMC narrative blog
**Scope:** KMC (the 40% figure is from WHO/published evidence; <5% is global coverage gap)
**Surprise:** 3/5 — known to MNCH specialists, but stark.
**Publishability:** 5/5 — public in WHO 2022 KMC guidance and our blog.
**Suggested home:** /programs/kmc; /insights.
**Verbatim phrasing candidate:** "Kangaroo Mother Care reduces neonatal mortality by up to 40%. The WHO recommends it for all newborns ≤2000g. Yet global KMC coverage remains below 5% for eligible infants — hospitals discharge families within days; structured at-home follow-up rarely exists. Connect KMC closes the post-discharge gap with 4–5 home visits in the first 60 days."
**Caveats / what's still unproven:** Our enrollment-within-3-days-of-discharge rate is currently 50% against a 70% target — closing the post-discharge gap depends on closing the enrollment-timing gap first.

## N12: 880,000 verified visits in 14 months — roughly 4 years of traditional NGO output, in one country bundle

**Source:** Brand messaging "Core Stats"; CHC overview; FP final report
**Scope:** CHC during the Founders Pledge grant period
**Surprise:** 3/5 — the time-equivalent translation is the move; the raw number alone is generic.
**Publishability:** 5/5 — public in FP report.
**Suggested home:** /deliver; /programs/chc; /insights.
**Verbatim phrasing candidate:** "880,000+ verified CHC visits in 14 months across 8 countries — performance-payment delivery at a pace that conventional NGO-led VAS supplementation typically achieves over multi-year campaigns in the same geographies. 44 LLOs activated in that window."
**Caveats / what's still unproven:** The 4-year time-equivalent is illustrative — there isn't a single published comparator that holds the country mix and commodity bundle constant. We are working with PRO Impact (IPA evaluation, $1.5M, 2026) on a cleaner counterfactual.

## N13: We separate cost asymmetry by commodity bundle — Nigeria $1.30 with ORS/Zinc co-pack, outside $0.78 without

**Source:** CHC overview "Cost Reduction"; FP report
**Scope:** CHC (Nigeria vs non-Nigeria sub-bundles within CHC)
**Surprise:** 4/5 — most cost-per-visit numbers are weighted averages that hide exactly this asymmetry.
**Publishability:** 5/5 — public in FP report.
**Suggested home:** /pay (named example); /programs/chc; /insights.
**Verbatim phrasing candidate:** "Our $1.70 weighted average per verified visit hides the bundle. Nigeria CHC with ORS/Zinc co-packs averaged $1.30 across 14 LLO contracts. Outside Nigeria — VAS + deworming, no ORS — averaged $0.78 across 17 contracts. Setup fees are running $0.40/visit during the grant and projected to fall to ~$0.10/visit at scale. Fully-loaded: commodity + FLW + LLO + 20% Connect platform fee."
**Caveats / what's still unproven:** Setup-fee projection ($0.40 → $0.10 at scale) is forward-looking. We will publish the converged number when the next cohort closes.

## N14: An AI coach (built on Open Chat Studio) handled 500 of 511 FLW queries — 97.8% — without human escalation in the Kenya pilot

**Source:** CHC overview "AI-Powered Supervision"
**Scope:** CHC (Kenya pilot)
**Surprise:** 3/5 — high-handle-rate AI numbers are common; the structured eval (88.7% accuracy, 81.5% usefulness) elevates it.
**Publishability:** 5/5 — public in FP report.
**Suggested home:** /learn (training-quality angle); /programs/chc; /insights.
**Verbatim phrasing candidate:** "In our Kenya CHC pilot, an AI chatbot on Dimagi's Open Chat Studio (accessed via WhatsApp) handled 500 of 511 FLW queries — 97.8% — without human escalation, with a 5-second average response time. Independent evaluation: 88.7% accuracy, 81.5% usefulness."
**Caveats / what's still unproven:** 97.8% handle rate is one pilot. We haven't yet published the failure-mode analysis on the 11 escalations or whether the rate holds for non-English-language deployments.

## N15: Campaign work in Nigeria isn't a disruption of routine care — it *is* the routine care

**Source:** insights.md Insight 5; FLW Displacement Survey (Oct 2025)
**Scope:** CHC (24 interviews in Gombe and Sokoto, 2025)
**Surprise:** 5/5 — directly contradicts the "crowd-out" concern most funders raise.
**Publishability:** 5/5 — survey is public.
**Suggested home:** /pay; /programs/chc; /audiences/funders; /insights.
**Verbatim phrasing candidate:** "Funders routinely ask whether paid campaign work crowds out volunteer health work. We commissioned 24 in-depth interviews in Gombe and Sokoto (CHC, 2025). Campaigns are not a disruption of Nigeria's CHV system — they *are* the system. CHVs routinely run campaigns, and other volunteers cover routine work during them. In Gombe, FLWs maintained volunteer hours by shifting schedules within Connect's 7am–7pm window."
**Caveats / what's still unproven:** N=24 in two states. We expect this to hold in similar community-health settings; we'd re-survey before claiming it elsewhere. The Western "crowd-out" assumption may still apply in countries with different CHV structures.

## N16: 65% conversion through Trial Run — and we publish what we drop

**Source:** insights.md Insight 1; CHC overview
**Scope:** CHC
**Surprise:** 3/5 — overlaps with N9 but framed differently for the funder lens.
**Publishability:** 5/5 — public.
**Suggested home:** /audiences/funders; /insights.
**Verbatim phrasing candidate:** "65% of LLOs that enter our Trial Run pass it. We publish that number because the alternative — opaque vendor lists — is what funders are trying to escape. The 35% that don't pass aren't blamed; they aren't continued."
**Caveats / what's still unproven:** Whether the 65% conversion holds outside CHC is an open question — KMC, ECD, and Readers are running on too small a contract base to publish their own conversion yet.

## N17: 5,000+ FLWs trained, $90,000+ in direct FLW payments — verified before disbursement

**Source:** Brand messaging "Core Stats"
**Scope:** Platform (cumulative across programs)
**Surprise:** 2/5 — generic-feeling unless paired with a verification claim.
**Publishability:** 5/5 — public.
**Suggested home:** Possibly /pay; not strong enough alone for /insights.
**Verbatim phrasing candidate:** "5,000+ FLWs trained across 12 countries; $90,000+ paid directly to FLWs in mobile money against verified visits."
**Caveats / what's still unproven:** —
**(Dropped: Surprise=2 below threshold.)**

## N18: We chose verified-visit cost reporting because cost-per-FLW-trained hides the lever that matters

**Source:** Insights.md framing across Insights 4 and the Pay-page logic; FP report methodology
**Scope:** Platform
**Surprise:** 4/5 — explicitly naming the metric *choice* rather than just the metric.
**Publishability:** 5/5 — implicit in our public reporting.
**Suggested home:** /pay (the methodology framing); /insights (methodology footer).
**Verbatim phrasing candidate:** "Most platforms report cost-per-FLW-trained, cost-per-app-installed, or cost-per-enrolled-LLO. We report cost-per-verified-visit because the others hide the lever that matters — whether the work was done. The asymmetry between activity-cost and outcome-cost is where most development funding gets eaten."
**Caveats / what's still unproven:** Verified-visit cost can itself be gamed if the verification stack is shallow; we publish our four-layer stack (biometric, GPS, photo, algorithmic) so readers can audit it.

## N19: Connect KMC FLWs carry a portable scale, thermometer, pulse oximeter, and measuring tape — every visit

**Source:** KMC overview "FLW Equipment"
**Scope:** KMC
**Surprise:** 3/5 — concrete and tangible; rare to see in a marketing site.
**Publishability:** 5/5 — public.
**Suggested home:** /programs/kmc.
**Verbatim phrasing candidate:** "Every Connect KMC home visit, the FLW arrives with a weighing scale, thermometer, pulse oximeter, and measuring tape. The app captures the readings. Danger signs — poor weight gain, hypothermia, infection — auto-trigger referrals, and the app prompts follow-up at the next visit."
**Caveats / what's still unproven:** Equipment availability across all 6 KMC LLO partners has been uneven; we don't yet have a published audit of equipment uptime.

## N20: A KMC enrolled SVN is on average 12.8 days old at first contact — under our 28-day target, but we're still missing the 3-day window for half

**Source:** KMC overview "Early Performance"
**Scope:** KMC (4,005 cases as of March 2026)
**Surprise:** 4/5 — splitting "we hit target A but not target B" honestly is unusual.
**Publishability:** 5/5 — public in conceptual model.
**Suggested home:** /programs/kmc; /insights.
**Verbatim phrasing candidate:** "Across 4,005 KMC cases (March 2026), we hit our 28-day enrollment target — average age at enrollment 12.8 days. We are *missing* our 70%-within-3-days-of-discharge target — currently 50%. The gap isn't FLW effort; it's that hospital discharge notifications aren't yet integrated. We're working on it; we publish the gap."
**Caveats / what's still unproven:** Whether discharge-notification integration alone closes the gap, or whether 3 days from discharge is the wrong target for the realities of post-discharge logistics.

## N21: 27,000+ ECD visits, 250M children at risk — the ratio that defines the problem

**Source:** ECD overview "Program Basics"; "The Challenge"
**Scope:** ECD
**Surprise:** 2/5 — scale-of-need framing is generic.
**Publishability:** 5/5 — public.
**Suggested home:** /programs/ecd.
**Verbatim phrasing candidate:** "27,000+ visits delivered against a population of 250 million children at risk of not achieving developmental potential."
**Caveats / what's still unproven:** —
**(Dropped: Surprise=2 below threshold.)**

## N22: Connect verifies through four independent layers — biometric, GPS, photo, algorithmic — a fabricated visit must beat all four

**Source:** insights.md Insight 3; CHC overview
**Scope:** Platform
**Surprise:** 4/5 — naming the verification stack as a *layered defense* (rather than a feature list) is the move.
**Publishability:** 5/5 — public.
**Suggested home:** /verify; /insights.
**Verbatim phrasing candidate:** "A fabricated visit on Connect has to beat four independent verification layers: biometric (FLW identity), GPS (location), photo (visit context), and algorithmic (statistical pattern from age/gender/MUAC). Our adversarial test only stresses the algorithmic layer — and even there, fabricators couldn't beat real workers. The other three layers compound."
**Caveats / what's still unproven:** Photo verification quality varies by network conditions; we have not yet published a clean false-positive rate on the photo layer in low-bandwidth deployments.

---

## Mining summary

- **Candidates produced:** 22
- **Above threshold (≥3 on both axes):** 20
- **Dropped:** N17 (Surprise=2), N21 (Surprise=2)
- **Median surprise of kept:** 4
- **Median publishability of kept:** 5

**Top 3 by combined score and depth-page potential:**
1. **N1** — adversarial fraud test. Signature for /verify and /programs/chc.
2. **N6** — caregiver attitudes already correct, knowledge/behavior is the gap. Signature for /programs/ecd and /learn.
3. **N15** — campaign work *is* Nigeria's CHV system. Signature for /pay and /audiences/funders.

**Internal-only source attribution:** All sources cited in this file are public-safe (insights.md is the team's curated public-ready summary; FP report is published; ECD report and CLP Stage 2 are publishable). No redactions required.
