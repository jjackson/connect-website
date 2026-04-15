# Connect Insights — Hard-Won Learnings from Implementation

The facts are in the overviews. The insights — the learnings that show *we actually know what we're doing* — are here. Every insight below has a **what we thought** / **what we learned** / **what we changed** structure because that's what makes it insightful rather than just factual.

Source: Founders Pledge Final Report (Feb 2026, CHC program), ECD Overview (Feb 2026), CLP Stage 2 Report (Feb 2026, CHC program), FLW Displacement Survey (Oct 2025, CHC program), KMC Conceptual Model (March 2026).

**Scoping rule (v0.2.36):** Every insight carries a `Scope:` field — either a program name or `Platform`. `Platform` is reserved for (a) cross-program evidence or (b) mechanisms that share the same code path across programs. Program-specific stats stay named to their program on every page. If you see a CHC-only number dressed as a Connect-wide claim, that's a bug — fix it before generating.

---

## Insight 1: LLO performance can't be pre-vetted. Only proven.

**Scope:** Platform (Trial Run model has been reused across CHC, Readers, KMC, and chlorine-dispenser work without modification; evidence spans programs.)

**What we thought:** Carefully vet LLOs before contracting — check their track record, assess their team, evaluate their capacity. Standard procurement practice.

**What we learned:** Pre-selection was a **poor predictor of field performance**. Past reputation, team size, organizational maturity — none of it reliably predicted whether an LLO would actually deliver.

**What we changed:** We invented the **Trial Run model**. New LLOs get a small initial contract — $3,000 setup fee for 3,000 verified child visits. Performance-based payment means we bear minimal financial risk if they fail. Of 37 LLOs contracted under this model, 24 entered Trial Runs, 10 underperformed and weren't continued, 3 went straight to larger campaigns based on prior track record.

**Why it matters:** The Trial Run model is sector-agnostic. It's now been reused for reading glasses distribution, KMC, and chlorine dispensers without modification. We can activate new partners in fragile contexts without betting the grant on them.

**Home:** Deliver page (as a core operational insight) + CHC detail (as the mechanism that scaled it to 44 LLOs).

---

## Insight 2: Workers naturally cluster. Microplans force them outward.

**Scope:** CHC (the 0.4 → 1.4 visits/child and 82-84% → 94% coverage numbers are all CHC measurements from the Founders Pledge evaluation. The microplanning mechanism is portable and in use on other campaigns, but reference the numbers as CHC-specific — e.g., "In the CHC program…".)

**What we thought:** Give FLWs a target area and a visit quota. They'll figure out the rest.

**What we learned:** Workers cherry-pick. In the CHC program, given a neighborhood, they'd average **0.4 visits per estimated eligible child** — visiting accessible households and skipping the harder ones. The populations missed were systematically those with lower baseline health coverage. **Convenience sampling at the exact moment equity was the goal.**

**What we changed:** Microplanning. Before a campaign, we overlay a grid onto the operational area using Google Open Buildings + OpenStreetMap + Microsoft data. Grid cells with at least one building become **Delivery Units**. DUs group into **Service Areas** sized for 1-2 weeks of work. A worker cannot move to the next Service Area until they close every DU in the current one — either completing visits or confirming no eligible children are present.

**The result (CHC):** 1.4 visits per estimated child in microplanned cells vs 0.4 without. **A 3.5× increase in coverage thoroughness.** Population coverage in CHC jumped from 82-84% to 94%.

**What didn't work:** Microplans failed in dispersed settlement patterns. Workers walked long distances to DUs with no actual buildings. Some DUs fell on inaccessible land (factory grounds, prison grounds). One campaign removed microplan execution entirely due to partner constraints.

**Home:** Verify page (as "how verification drives equitable coverage in CHC") + CHC detail (as the CHC innovation).

---

## Insight 3: We paid people to defeat our fraud detection. Then we watched them fail.

**Scope:** Platform (the fraud-detection pipeline is the same code path on every program. The adversarial test was designed and run once; the model applies to any deployment that collects the relevant data elements.)

**What we thought:** Our verification stack — biometrics, GPS, photos — handles fraud risk. Good enough.

**What we asked:** What if a motivated insider tried to fake data? Could statistical patterns alone — no GPS, no timestamps, no photos — tell us?

**What we did:** Paid experienced FLWs to submit 100 fake visit records each. Ran three rounds. After each round, we coached the fakers on what gave them away. We offered bonuses to the top 25% most convincing fabricators. The kind of adversarial testing most organizations only do when a regulator makes them.

**What we found:** Using three data elements (age, gender, MUAC measurements), a Random Forest model achieved an **AUC of 0.91 ± 0.09**. Only **2.5% of real workers** received fraud risk scores higher than even the lowest-scoring fabricator. **Out of 33 adversarial fakers, we detected them with near-perfect discrimination using data patterns alone** — before GPS and photo verification even kicked in.

**Why it matters:** Fraud detection isn't a promise. It's an empirically validated layer. And because verification has four independent layers (biometric, GPS, photo, algorithmic), a fabricated visit has to beat all four.

**Home:** Verify page (as the signature story) + CHC detail (where the test was run).

---

## Insight 4: Connect's scaling pattern inverts the usual cost curve — evidence from CHC.

**Scope:** CHC for the specific numbers (the 22% reduction and $2.20 → $1.70 figures are CHC cost-per-verified-visit during the Founders Pledge grant period). The *structural reasons* (LLO economics, performance-based payment, integrated digital tooling) are platform-level mechanisms and can be described as Connect architecture, but the number must always be attached to the program it was measured in.

**What we thought:** As campaigns grow, operational costs grow. That's how scaling works. Every other Dimagi program follows this pattern.

**What we learned:** **In the CHC program, Connect inverted it.** During the Founders Pledge grant period, CHC scaled to a rate capable of supporting millions of child visits per year **without substantial growth in Dimagi's team**. Cost per verified visit in CHC dropped from $2.20 to $1.70 — a **22% reduction** as the program grew.

**Why this works (three structural reasons — platform-level):**
1. LLOs have inherently low overhead because they're local and lean
2. Performance-based payment ensures costs track actual delivery, not organizational size
3. Digital technology is integrated into every step — worker guidance, verification, payment — creating ongoing efficiency gains that compound as the network grows

**The counterintuitive implication (CHC as evidence):** Most development organizations have a structural ceiling on cost-effectiveness — the more they scale, the more ops burden grows. CHC under the Connect architecture is one of the few measured examples where scale created cost *reduction* instead of cost creep. Whether the same curve holds for every new program is an empirical question; we measure it per program.

**How to reference on pages:** Always as "In the CHC program, cost per verified visit fell 22%…" — never as "Connect got 22% leaner." The 22% is CHC. The *mechanism* is platform, and deserves separate language ("Connect's architecture — LLO economics plus performance-based payment plus integrated tooling — is designed to produce cost-reducing scale, and CHC is the program where we've measured it.")

**Home:** Pay page (as the cost story, clearly named to CHC) + CHC detail + For Funders.

---

## Insight 5: Campaign work doesn't displace routine health services — evidence from CHC in Nigeria.

**Scope:** CHC (survey of 24 interviews in Gombe and Sokoto within the CHC program, 2025). The underlying fact about Nigerian CHV systems is cultural context that generalizes to CHC-style campaigns in similar settings; it does not automatically generalize to all Connect programs in all countries.

**What we thought:** If we pay FLWs to do campaign visits, they'll neglect their regular volunteer health work. This is the "crowd-out" concern funders raise.

**What we did:** Commissioned 24 in-depth interviews with 20 FLWs, 2 LLO staff, and 2 local health representatives across Gombe and Sokoto in Nigeria — all inside the CHC program.

**What we learned:** Campaign work is **normal and expected** in Nigeria's community health volunteer system. CHVs routinely do campaigns — it's their main income source. When our CHC FLWs reduced volunteer hours, **other volunteers at the facility covered the work**, as they typically do during any campaign. In Gombe, FLWs maintained volunteer hours by shifting schedules within Connect's flexible 7am-7pm window.

**The deeper point:** The "displacement" concern was built on Western assumptions about what CHVs do. In the Nigerian CHC context, campaigns are not a disruption of the system. They *are* the system. We expect this to hold in similar community-health settings; we'd re-survey before claiming it elsewhere.

**Home:** Pay page (named as the CHC FLW-benefit finding) + CHC detail + For Funders (addresses a specific concern).

---

## Insight 6: LLOs navigate vaccine hesitancy with religious leaders. We didn't teach them this.

**Scope:** CHC (specifically the CLP Stage 2 vaccine campaign — 7 LLOs). The observation that locally-led organizations bring locally-grounded outreach strategies is a platform-level point about LLO value, but the specific religious-leader finding is from the CHC vaccine campaign.

**What we thought:** Digital training covers vaccine myths. FLWs read the content, they're equipped.

**What we learned:** Of 7 LLOs in our CLP Stage 2 vaccine campaign (CHC program), 5-6 independently leveraged **religious leaders, community leaders, or existing community relationships** as part of their outreach strategy. They did this before we asked. One FLW countered vaccine hesitancy with a personal example: "We were immunized, we have children." Another LLO had FLWs who were **recommended by the community itself**, lending immediate credibility.

**Why it matters:** The real intervention isn't what's in the app. It's what locally-led organizations do with the platform when they operate in their own communities. This is why the L in LLO is load-bearing. Dimagi can't centralize this knowledge. The platform's job is to enable it, not replace it.

**Home:** Deliver page (as "why locally-led matters" — named to the CHC vaccine campaign) + CHC detail.

---

## Insight 7: We learned caregiver attitudes were already correct. The gap is knowledge and behavior.

**Scope:** ECD (Malawi pilot, 50 caregiver surveys).

**What we thought:** An ECD intervention should build positive attitudes about responsive caregiving, talk-and-play, and developmental support.

**What we learned (Malawi ECD pilot, 50 caregiver surveys):** Nearly all caregivers **already held positive ECD attitudes at baseline**. They agreed talk-and-play supports brain development. They endorsed responsive caregiving. Attitude surveys scored high before we started and high after we finished.

**Where we actually moved the needle (ECD pilot):**
- **Knowledge: +33%** on timing of rapid child development
- **Knowledge: +41%** on ways to support mental development
- **Behavior (observed): +21%** in teaching
- **Behavior (observed): +21%** in encouragement of autonomy

**Why it matters:** We reallocated the intervention. The 3-visit pilot is expanding to 8-10 visits across 12 months — not because we need more time to convince caregivers ECD matters (they know), but because behavior change takes sustained practice. The program is now evidence-guided, not just evidence-based.

**What we didn't move:** Encouragement of autonomy is still at 47% at endline (up from baseline). It's the hardest subdomain. We're still working on it.

**Home:** ECD detail (as the pilot insight) + Learn page (as how digital training adapts based on ECD evidence, named to ECD).

---

## Insight 8: Knowledge tests alone don't produce competent FLWs. We tried. They didn't.

**Scope:** Platform (the layered Learn→test→AI coach→peer practice→supervised observation methodology has been validated with ~400 FLWs across iterative experiments spanning multiple programs. Same code path — the Learn app and the AI coach — running on every deployment.)

**What we thought:** If FLWs pass a digital knowledge test, they're ready to deliver.

**What we learned:** Knowledge ≠ competence. Workers who aced the test still struggled with the nuances of in-person counseling — how to handle a skeptical caregiver, how to recognize subtle danger signs, how to practice motivational interviewing.

**What we changed:** Layered the model. Now FLWs complete:
1. Self-paced digital learning in the Learn app
2. An in-app knowledge test (must pass to progress)
3. Daily interaction with an AI coach bot (built on Dimagi's Open Chat Studio)
4. Practice with peers
5. One supervised observation visit rated by an LLO supervisor

**What the AI coach adds that the test doesn't:** Scenario-based practice. Motivational interviewing drills. Daily reflection on real visit experiences. Identifying knowledge gaps through conversation rather than multiple choice.

**Results (across programs):** 85% of FLWs progress from training to service delivery. 88% score above 70% on their first observed visits. 77% pass the supervised observation. **Validated with ~400 FLWs across iterative experiments.**

**Home:** Learn page (as the methodology insight) + ECD detail (as the specific program design example).

---

## Insight 9: We documented our failure in CAR. Publishing it is part of the practice.

**Scope:** CHC (the CAR LLO contracting happened inside the CHC vaccine-campaign work. The *lesson* — fragile contexts likely need in-country presence — is platform-portable guidance for future deployments, but the specific failure is CHC.)

**What we thought:** Connect's rapid partner activation model is portable to any context.

**What we learned:** In the Central African Republic (CHC vaccine work), **both contracted LLOs dropped out** due to staffing and connectivity issues. Remote coordination alone wasn't enough. Activating partners in fragile contexts likely requires dedicated in-country presence.

**Why this insight is in a marketing site:** Real platforms publish what didn't work. The CAR experience is now shaping how we approach fragile contexts — we're not repeating the same approach in similarly difficult geographies without in-country presence.

**Home:** Deliver page (in a "what's next / limitations" aside — named to CHC/CAR) + CHC detail.

---

## Insight 10: Guardrails are not hard stops. This is a design philosophy.

**Scope:** Platform (the guardrails-vs-payment-criteria distinction is a Connect configuration framework that every program inherits. The live example given — KMC's 3-day guardrail at 50% vs 70% target — is KMC-specific and must be named as such.)

**What we thought:** When a FLW misses a target — first visit within 3 days of discharge, say — we should reject the visit or withhold payment.

**What we changed:** We distinguished **payment criteria** (hard — must be met to be paid) from **guardrails** (soft — trigger audits and performance conversations, but don't block payment). This distinction is a platform configuration, inherited by every program.

**An example (KMC):** The KMC program has 4 mandatory home visits per SVN as a payment criterion. But the KMC guardrail "first visit within 3 days of discharge" is audited, not enforced. Current KMC performance on that guardrail is 50% against a 70% target. We're working on it — through LLO coaching, scheduling support, and discharge notification integration — not through punishment.

**Why it matters:** Platforms that punish missed guardrails don't get honest data. FLWs would learn to game the system (falsify visit dates to hit the 3-day window, for example). A platform that separates audits from payment gets **the real data it needs to improve the program**.

**Home:** Verify page (as the platform design philosophy) + KMC detail (as the live example).

---

## How to use these on pages

Each insight is structured to be dramatizable on a page:
- **Signature moment:** The insight is the moment. Don't bury it in a stat ribbon.
- **Set-up and pay-off:** Tell the tension. "We thought X. We learned Y. We changed Z."
- **Voice:** Direct, specific, willing to name what didn't work. This is expert-to-expert communication, not marketing copy.
- **Data earns the claim:** Numbers support the insight, they don't replace it.
- **Scope discipline:** A program-scoped stat stays attached to its program in prose. Never strip the program name to make the claim sound broader.

The tone should feel like reading a really good engineering retrospective — from a team that knows its stuff and doesn't need to oversell.
