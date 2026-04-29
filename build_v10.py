#!/usr/bin/env python3
"""
Generate v10a (Foundation memo), v10b (Field dispatch), v10c (Knowledge graph)
variants of the Connect by Dimagi marketing site.

Each variant:
  - 11 pages: index, learn, deliver, verify, pay, programs, insights,
    programs/{chc,kmc,ecd,readers}
  - styles.css
  - shares content (insights.md / nuggets.md) but renders with a distinct
    aesthetic and learning presentation pattern.

The generator emits HTML directly. It is deterministic and self-contained
so that re-runs produce identical output (useful for eval comparisons).
"""

import json
import os
import shutil
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).parent
OUT_BASE = ROOT

# ---------------------------------------------------------------------------
# Shared content data
# ---------------------------------------------------------------------------

# Each insight entry: id, title, scope, what_we_thought, what_we_learned,
# what_we_changed, why_matters, caveats, evidence_tier, score_seed.
INSIGHTS = [
    {
        "id": "I1",
        "title": "LLO performance can't be pre-vetted. Only proven.",
        "scope": "Platform",
        "thought": "Carefully vet LLOs before contracting — track record, team size, organizational maturity. Standard procurement practice.",
        "learned": "Past reputation, team size, organizational maturity — none of it reliably predicted whether an LLO would actually deliver in the field.",
        "changed": "We invented the Trial Run model. New LLOs get a small initial contract — $3,000 setup for 3,000 verified child visits. Performance-based payment means we bear minimal financial risk if they fail. Of 37 LLOs contracted under this model in CHC, 24 entered Trial Runs, 10 underperformed and weren't continued, 3 went straight to larger campaigns.",
        "matters": "The Trial Run model is sector-agnostic. It's now been reused for reading glasses distribution, KMC, and chlorine dispensers without modification. We can activate new partners in fragile contexts without betting the grant on them.",
        "caveats": "In the Central African Republic, both contracted LLOs dropped out — staffing and connectivity issues. We now flag fragile contexts as needing dedicated in-country presence.",
        "source": "Founders Pledge Final Report (Feb 2026)",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "homes": ["deliver", "chc", "insights"],
    },
    {
        "id": "I2",
        "title": "Workers naturally cluster. Microplans force them outward.",
        "scope": "CHC",
        "thought": "Give FLWs a target area and a visit quota. They'll figure out the rest.",
        "learned": "Workers cherry-pick. In CHC, given a neighborhood, they'd average 0.4 visits per estimated eligible child — visiting accessible households and skipping the harder ones. The populations missed were systematically those with lower baseline health coverage. Convenience sampling at the exact moment equity was the goal.",
        "changed": "Microplanning. Before a campaign, we overlay a grid onto the operational area using Google Open Buildings + OpenStreetMap + Microsoft data. Grid cells with at least one building become Delivery Units. DUs group into Service Areas sized for 1–2 weeks of work. A worker cannot move to the next Service Area until they close every DU in the current one.",
        "matters": "1.4 visits per estimated child in microplanned cells vs 0.4 without — a 3.5× increase in coverage thoroughness. CHC population coverage rose from 82–84% to 94%, measured against GRID3 gold-standard population estimates at 300×300m resolution.",
        "caveats": "Microplans failed in dispersed settlement patterns. Workers walked long distances to DUs with no actual buildings. Some DUs fell on inaccessible land (factory grounds, prison grounds). One campaign removed microplan execution entirely.",
        "source": "Founders Pledge Final Report (Feb 2026)",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "homes": ["verify", "chc", "insights"],
    },
    {
        "id": "I3",
        "title": "We paid people to defeat our fraud detection. Then we watched them fail.",
        "scope": "Platform",
        "thought": "Our verification stack — biometrics, GPS, photos — handles fraud risk. Good enough.",
        "learned": "Asked: what if a motivated insider tried to fake data? Could statistical patterns alone — no GPS, no timestamps, no photos — tell us? Paid experienced FLWs to submit 100 fake visit records each. Three rounds. Bonuses for the top 25% most convincing fabricators. Most organizations only do this when a regulator makes them.",
        "changed": "Using just three data elements (age, gender, MUAC), a Random Forest model achieved AUC 0.91 ± 0.09. Only 2.5% of real workers received fraud risk scores higher than even the lowest-scoring fabricator. Out of 33 adversarial fakers, near-perfect discrimination using data patterns alone — before GPS and photo verification even kicked in.",
        "matters": "Fraud detection isn't a promise. It's an empirically validated layer. And because verification has four independent layers (biometric, GPS, photo, algorithmic), a fabricated visit has to beat all four.",
        "caveats": "97.5% is on adversarial paid-bonus testing. The production false-positive rate against unmotivated fabrication has not been published; we'll publish when a clean cohort comparison closes.",
        "source": "Founders Pledge Final Report (Feb 2026)",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "homes": ["verify", "chc", "insights"],
    },
    {
        "id": "I4",
        "title": "Connect's scaling pattern inverts the usual cost curve — evidence from CHC.",
        "scope": "CHC",
        "thought": "As campaigns grow, operational costs grow. That's how scaling works. Every other Dimagi program has followed this pattern.",
        "learned": "In the CHC program, Connect inverted it. Cost per verified visit dropped from $2.20 to $1.70 — a 22% reduction — as the program scaled to a rate capable of supporting millions of child visits per year, without substantial growth in Dimagi's team.",
        "changed": "Three structural reasons (platform-level): LLOs have inherently low overhead because they're local and lean; performance-based payment ensures costs track actual delivery, not organizational size; digital tooling is integrated into every step, creating compounding efficiency gains.",
        "matters": "Most development organizations have a structural ceiling on cost-effectiveness. CHC under the Connect architecture is one of the few measured examples where scale created cost reduction instead of cost creep. Whether the same curve holds for every new program is empirical — we measure it per program.",
        "caveats": "$1.70 is a weighted average. Nigeria CHC with ORS/Zinc co-packs: $1.30 across 14 LLO contracts. Outside Nigeria (VAS + deworming, no ORS): $0.78 across 17 contracts. Setup fees $0.40/visit during grant, projected to fall to $0.10/visit at scale.",
        "source": "Founders Pledge Final Report (Feb 2026)",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "homes": ["pay", "chc", "insights"],
    },
    {
        "id": "I5",
        "title": "Campaign work doesn't displace routine health services — evidence from CHC in Nigeria.",
        "scope": "CHC",
        "thought": "If we pay FLWs to do campaign visits, they'll neglect their regular volunteer health work. The 'crowd-out' concern funders raise.",
        "learned": "Commissioned 24 in-depth interviews with 20 FLWs, 2 LLO staff, and 2 local health representatives across Gombe and Sokoto in Nigeria — all inside the CHC program.",
        "changed": "Campaign work is normal and expected in Nigeria's community health volunteer system. CHVs routinely do campaigns — it's their main income source. When CHC FLWs reduced volunteer hours, other volunteers at the facility covered the work. In Gombe, FLWs maintained volunteer hours by shifting schedules within Connect's flexible 7am–7pm window.",
        "matters": "The 'displacement' concern was built on Western assumptions about what CHVs do. In the Nigerian CHC context, campaigns are not a disruption of the system — they are the system.",
        "caveats": "N=24 in two states. We expect this to hold in similar community-health settings; we'd re-survey before claiming it elsewhere.",
        "source": "FLW Displacement Survey (Oct 2025), CHC program",
        "evidence_tier": "triangulated qualitative",
        "tier_label": "triangulated qualitative",
        "homes": ["pay", "chc", "insights"],
    },
    {
        "id": "I6",
        "title": "LLOs navigated vaccine hesitancy with religious leaders. We didn't teach them this.",
        "scope": "CHC",
        "thought": "Digital training covers vaccine myths. FLWs read the content, they're equipped.",
        "learned": "Of 7 LLOs in our CLP Stage 2 vaccine campaign (CHC), 5–6 independently leveraged religious leaders, community leaders, or existing community relationships as part of their outreach strategy. They did this before we asked. One FLW countered hesitancy with a personal example: 'We were immunized, we have children.' Another LLO had FLWs the community itself recommended.",
        "changed": "We don't try to centralize this knowledge. The platform's job is to enable locally-led organizations to do what they're already good at, not to replace it.",
        "matters": "The real intervention isn't what's in the app. It's what locally-led organizations do with the platform when they operate in their own communities. This is why the L in LLO is load-bearing.",
        "caveats": "We have not built a structured framework for capturing or sharing what individual LLOs invent locally — the 'real intervention' often lives in their heads, not in our app.",
        "source": "CLP Stage 2 Report (Feb 2026), CHC vaccine campaign",
        "evidence_tier": "triangulated qualitative",
        "tier_label": "triangulated qualitative",
        "homes": ["deliver", "chc", "insights"],
    },
    {
        "id": "I7",
        "title": "Caregivers' attitudes were already correct. The gap is knowledge and behavior.",
        "scope": "ECD",
        "thought": "An ECD intervention should build positive attitudes about responsive caregiving, talk-and-play, and developmental support.",
        "learned": "In the Malawi ECD pilot (76 FLWs, 9,510+ visits, 50-caregiver baseline/endline), nearly all caregivers already held positive ECD attitudes at baseline. They agreed talk-and-play supports brain development. They endorsed responsive caregiving. Attitude scores were high before and after.",
        "changed": "We reallocated the intervention. The 3-visit pilot is expanding to 8–10 visits across 12 months — not because we need more time to convince caregivers ECD matters (they know), but because behavior change takes sustained practice.",
        "matters": "Knowledge: +33% on timing of rapid child development. Knowledge: +41% on ways to support mental development. Observed behavior: +21% in teaching, +21% in encouragement of autonomy. The program is now evidence-guided, not just evidence-based.",
        "caveats": "Encouragement of autonomy is still at 47% at endline. It's the hardest sub-domain. Whether 8–10 visits will move it, or whether it requires a different intervention design, is open.",
        "source": "ECD Overview, Malawi pilot (April–July 2025)",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "homes": ["learn", "ecd", "insights"],
    },
    {
        "id": "I8",
        "title": "Knowledge tests alone don't produce competent FLWs. We tried. They didn't.",
        "scope": "Platform",
        "thought": "If FLWs pass a digital knowledge test, they're ready to deliver.",
        "learned": "Knowledge ≠ competence. Workers who aced the test still struggled with the nuances of in-person counseling — how to handle a skeptical caregiver, how to recognize subtle danger signs, how to practice motivational interviewing.",
        "changed": "Layered the model: self-paced digital learning, in-app knowledge test (must pass), daily AI coach interaction (built on Dimagi's Open Chat Studio), peer practice, one supervised observation visit rated by an LLO supervisor.",
        "matters": "85% of FLWs progress from training to service delivery. 88% score above 70% on first observed visits. 77% pass the supervised observation. Validated with 400+ FLWs across iterative experiments spanning multiple programs.",
        "caveats": "We have not yet published a clean comparison of AI-coach vs. peer-practice contributions to that 77% figure.",
        "source": "ECD Overview + CLP Stage 2 Report",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "homes": ["learn", "ecd", "insights"],
    },
    {
        "id": "I9",
        "title": "We documented our failure in CAR. Publishing it is part of the practice.",
        "scope": "CHC",
        "thought": "Connect's rapid partner activation model is portable to any context.",
        "learned": "In the Central African Republic (CHC vaccine work), both contracted LLOs dropped out due to staffing and connectivity issues. Remote coordination alone wasn't enough.",
        "changed": "Activating partners in fragile contexts likely requires dedicated in-country presence. We're not repeating the same approach in similarly difficult geographies without it.",
        "matters": "Real platforms publish what didn't work. The CAR experience is now shaping how we approach fragile contexts.",
        "caveats": "'In-country presence' is a coarse rule. We don't have a sharper predictive model for which fragile-context features make remote coordination fail.",
        "source": "Founders Pledge Final Report (Feb 2026), CAR vaccine work",
        "evidence_tier": "lived experience",
        "tier_label": "lived experience",
        "homes": ["deliver", "chc", "insights"],
    },
    {
        "id": "I10",
        "title": "Guardrails are not hard stops. This is a design philosophy.",
        "scope": "Platform",
        "thought": "When a FLW misses a target — first visit within 3 days of discharge, say — we should reject the visit or withhold payment.",
        "learned": "Punishing missed guardrails trains FLWs to game the system (falsify visit dates to hit the 3-day window, for example). A platform that punishes guardrails doesn't get the honest data it needs to improve the program.",
        "changed": "Distinguished payment criteria (hard — must be met to be paid) from guardrails (soft — trigger audits and performance conversations, but don't block payment). This is a platform-level configuration that every program inherits.",
        "matters": "KMC has 4 mandatory home visits per SVN as a payment criterion. Its 'first visit within 3 days of discharge' is a guardrail — currently 50% against a 70% target. We coach, integrate discharge notifications, and track. We don't punish.",
        "caveats": "Whether 70% is achievable through coaching plus discharge-notification integration alone, or whether the 3-day window itself needs to be redesigned for post-discharge logistics, is open.",
        "source": "KMC Conceptual Model v1 (March 2026)",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "homes": ["verify", "kmc", "insights"],
    },
]

NUGGETS = [
    {
        "id": "N1",
        "claim": "We paid experienced FLWs to fake 100 visit records each across three rounds and offered bonuses to the top 25% most convincing fabricators. Out of 33 adversarial fakers, 97.5% of real workers scored cleaner than even the lowest-scoring fabricator — using just three data points (age, gender, MUAC). AUC 0.91 ± 0.09.",
        "scope": "Platform",
        "home": "verify",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "open_question": "97.5% is from adversarial paid-bonus testing. Production false-positive rate is not yet published.",
        "judge_score": 9,
    },
    {
        "id": "N2",
        "claim": "Without microplans, FLWs in CHC averaged 0.4 visits per estimated eligible child — they cherry-picked accessible households. With microplans forcing them to close every Delivery Unit before unlocking the next Service Area, they hit 1.4 visits per child. A 3.5× thoroughness gain, and population coverage rose from 82–84% to 94%.",
        "scope": "CHC",
        "home": "chc",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "open_question": "Microplans failed in dispersed settlements and inaccessible land — we don't yet have a clean threshold.",
        "judge_score": 9,
    },
    {
        "id": "N3",
        "claim": "In the CHC program, cost per verified visit fell 22% — from $2.20 to $1.70 — as the program scaled. Connect's architecture (LLO economics + performance-based payment + integrated tooling) is designed to produce cost-reducing scale; CHC is the program where we've measured it.",
        "scope": "CHC",
        "home": "pay",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "open_question": "$1.70 weighted average masks bundle differences ($1.30 with ORS, $0.78 without). Whether the curve holds in non-CHC programs is open.",
        "judge_score": 8,
    },
    {
        "id": "N4",
        "claim": "Conventional procurement says vet partners thoroughly before contracting. We tried it. Past reputation, team size, organizational maturity — none of it reliably predicted whether an LLO would actually deliver. So we invented the Trial Run: $3,000 setup for 3,000 verified child visits. 65% conversion through the Trial Run gate.",
        "scope": "Platform",
        "home": "deliver",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "open_question": "Whether 65% holds outside CHC is open — KMC, ECD, Readers are still on too small a contract base.",
        "judge_score": 8,
    },
    {
        "id": "N5",
        "claim": "Workers who aced our digital knowledge test still struggled with the nuances of in-person counseling. So we layered the model: self-paced learning, in-app test, daily AI coach interaction (Open Chat Studio), peer practice, supervised observation. 85% progress to service delivery; 88% score above 70% on first observed visits. Validated across 400+ FLWs.",
        "scope": "Platform",
        "home": "learn",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "open_question": "AI-coach vs peer-practice contribution to the 77% supervised-observation pass rate is not yet decomposed.",
        "judge_score": 7,
    },
    {
        "id": "N6",
        "claim": "Our Malawi ECD pilot (76 FLWs, 9,510+ visits, 50-caregiver baseline/endline) found nearly all caregivers already held positive ECD attitudes at baseline. The intervention didn't need to convince them — it needed to close the gap between belief and practice. Knowledge of rapid-development timing rose +33%; observed teaching behavior +21%; encouragement-of-autonomy +21% but still only 47% at endline.",
        "scope": "ECD",
        "home": "ecd",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "open_question": "Encouragement-of-autonomy is the hardest sub-domain. Whether 8–10 visits move it, or it needs a different design, is open.",
        "judge_score": 9,
    },
    {
        "id": "N7",
        "claim": "Of 7 LLOs in our CLP Stage 2 vaccine campaign, 5–6 independently leveraged religious leaders, community leaders, or existing community relationships to navigate vaccine hesitancy. They did this before we asked.",
        "scope": "CHC",
        "home": "deliver",
        "evidence_tier": "triangulated qualitative",
        "tier_label": "triangulated qualitative",
        "open_question": "We have not built a structured framework for capturing what individual LLOs invent locally.",
        "judge_score": 7,
    },
    {
        "id": "N8",
        "claim": "In the Central African Republic, both contracted LLOs in our CHC vaccine work dropped out — staffing and connectivity issues. Remote coordination wasn't enough. We've now flagged fragile contexts as requiring dedicated in-country presence.",
        "scope": "CHC",
        "home": "deliver",
        "evidence_tier": "lived experience",
        "tier_label": "lived experience",
        "open_question": "'In-country presence' is a coarse rule. Sharper predictive model for fragile-context failure modes is open.",
        "judge_score": 8,
    },
    {
        "id": "N9",
        "claim": "107 EOI applications. 37 contracted under Trial Run terms. 24 advanced to full Trials. 14 passed and ran larger campaigns. The 35% that didn't pass aren't continued. We publish this conversion rate because diligence readers ask about it.",
        "scope": "CHC",
        "home": "deliver",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "open_question": "Selection criteria driving the 65% are program-manager judgment calls; not yet codified.",
        "judge_score": 7,
    },
    {
        "id": "N10",
        "claim": "KMC has 4 mandatory home visits per SVN as a payment criterion. Its 'first visit within 3 days of discharge' is a guardrail — audited, not enforced. Current performance: 50% against a 70% target. We don't punish FLWs for missing it because punishment trains workers to falsify dates.",
        "scope": "KMC",
        "home": "kmc",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "open_question": "Whether 70% is achievable through coaching alone, or the 3-day window itself needs redesign, is open.",
        "judge_score": 8,
    },
    {
        "id": "N11",
        "claim": "Kangaroo Mother Care reduces neonatal mortality by up to 40%. The WHO recommends it for all newborns ≤2000g. Yet global KMC coverage remains below 5% for eligible infants — hospitals discharge families within days; structured at-home follow-up rarely exists. Connect KMC closes the post-discharge gap.",
        "scope": "KMC",
        "home": "kmc",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "open_question": "Our enrollment-within-3-days rate is 50% against 70%. Closing the post-discharge gap depends on closing the enrollment-timing gap.",
        "judge_score": 7,
    },
    {
        "id": "N12",
        "claim": "880,000+ verified CHC visits in 14 months across 8 countries — performance-payment delivery at a pace that conventional NGO-led VAS supplementation typically achieves over multi-year campaigns in the same geographies. 44 LLOs activated in that window.",
        "scope": "CHC",
        "home": "deliver",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "open_question": "The 4-year time-equivalent comparison is illustrative — no single published comparator holds country mix and commodity bundle constant.",
        "judge_score": 7,
    },
    {
        "id": "N13",
        "claim": "Our $1.70 weighted average per verified visit hides the bundle. Nigeria CHC with ORS/Zinc co-packs: $1.30 across 14 LLO contracts. Outside Nigeria — VAS + deworming, no ORS — $0.78 across 17 contracts. Setup fees $0.40/visit during grant, projected $0.10/visit at scale.",
        "scope": "CHC",
        "home": "pay",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "open_question": "Setup-fee projection ($0.40 → $0.10) is forward-looking. Converged number publishes when next cohort closes.",
        "judge_score": 8,
    },
    {
        "id": "N14",
        "claim": "In our Kenya CHC pilot, an AI chatbot on Dimagi's Open Chat Studio (accessed via WhatsApp) handled 500 of 511 FLW queries — 97.8% — without human escalation, with 5-second average response time. Independent evaluation: 88.7% accuracy, 81.5% usefulness.",
        "scope": "CHC",
        "home": "learn",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "open_question": "Whether 97.8% holds in non-English-language deployments is open.",
        "judge_score": 7,
    },
    {
        "id": "N15",
        "claim": "Funders routinely ask whether paid campaign work crowds out volunteer health work. We commissioned 24 in-depth interviews in Gombe and Sokoto (CHC, 2025). Campaigns are not a disruption of Nigeria's CHV system — they *are* the system. CHVs routinely run campaigns. In Gombe, FLWs maintained volunteer hours by shifting schedules within Connect's 7am–7pm window.",
        "scope": "CHC",
        "home": "pay",
        "evidence_tier": "triangulated qualitative",
        "tier_label": "triangulated qualitative",
        "open_question": "N=24 in two states. Whether 'campaigns are routine' holds in CHV systems with different structures — re-survey first.",
        "judge_score": 9,
    },
    {
        "id": "N18",
        "claim": "Most platforms report cost-per-FLW-trained, cost-per-app-installed, or cost-per-enrolled-LLO. We report cost-per-verified-visit because the others hide the lever that matters — whether the work was done.",
        "scope": "Platform",
        "home": "pay",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "open_question": "Verified-visit cost can itself be gamed if the verification stack is shallow; we publish our four-layer stack so readers can audit it.",
        "judge_score": 7,
    },
    {
        "id": "N19",
        "claim": "Every Connect KMC home visit, the FLW arrives with a weighing scale, thermometer, pulse oximeter, and measuring tape. The app captures the readings. Danger signs auto-trigger referrals, and the app prompts follow-up at the next visit.",
        "scope": "KMC",
        "home": "kmc",
        "evidence_tier": "lived experience",
        "tier_label": "lived experience",
        "open_question": "Equipment availability across the 6 KMC LLO partners has been uneven. Audit not yet published.",
        "judge_score": 6,
    },
    {
        "id": "N20",
        "claim": "Across 4,005 KMC cases (March 2026), we hit our 28-day enrollment target — average age at enrollment 12.8 days. We are missing our 70%-within-3-days-of-discharge target — currently 50%. The gap isn't FLW effort; it's that hospital discharge notifications aren't yet integrated.",
        "scope": "KMC",
        "home": "kmc",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "open_question": "Whether discharge-notification integration alone closes the gap, or the 3-day target itself needs redesign.",
        "judge_score": 7,
    },
    {
        "id": "N22",
        "claim": "A fabricated visit on Connect has to beat four independent verification layers: biometric (FLW identity), GPS (location), photo (visit context), and algorithmic (statistical pattern from age/gender/MUAC). Our adversarial test only stresses the algorithmic layer — and even there, fabricators couldn't beat real workers.",
        "scope": "Platform",
        "home": "verify",
        "evidence_tier": "hard data",
        "tier_label": "hard data",
        "open_question": "Photo verification quality varies by network conditions. False-positive rate on the photo layer in low-bandwidth deployments is not yet published.",
        "judge_score": 7,
    },
]

# Programs metadata
PROGRAMS = {
    "chc": {
        "name": "Child Health Campaign",
        "tagline": "Door-to-door child health: vitamin A, deworming, ORS, malnutrition screening, vaccines.",
        "regions": "Nigeria, DRC, CAR, Kenya, Uganda, Tanzania, Zambia, Sierra Leone (8 countries)",
        "scale": "880,000+ verified visits in 14 months; 1,016,000+ in 2025",
        "funders": "GiveWell · Founders Pledge · Gavi",
        "partners": "44 contracted LLOs · 28 active",
        "video": "https://www.youtube.com/watch?v=VRbvUj9LTUg",
        "video_title": "Inside the Child Health Campaign in Kenya",
        "metrics": [
            ("880K+", "Verified visits in 14 months"),
            ("44", "LLOs activated"),
            ("94%", "Population coverage with microplans"),
            ("$1.70", "Cost per verified visit (down from $2.20)"),
        ],
        "challenge": "Vitamin A supplementation, deworming, malnutrition screening, and vaccine promotion for children 0–59 months. Traditional NGO-led campaigns plateau at 82–84% population coverage. The populations they miss are systematically those with lower baseline health access.",
        "approach": "FLWs from local LLOs run door-to-door campaigns guided by a microplanned grid of Delivery Units. Verified payment per visit. AI coach support via WhatsApp. Adversarial fraud testing baked in.",
        "insight_ids": ["I1", "I2", "I3", "I4", "I5", "I6"],
    },
    "kmc": {
        "name": "Kangaroo Mother Care",
        "tagline": "Closing the post-discharge gap for small and vulnerable newborns.",
        "regions": "Uganda, Kenya, India, Nigeria",
        "scale": "5,000 cases · 4,005 enrolled (March 2026) · 3,600+ SVNs enrolled",
        "funders": "Eleanor Crook Foundation",
        "partners": "PIPNU · Nama Wellness · Global Health Innovations · Ansh · BERI · eHealth Africa",
        "video": "https://www.youtube.com/watch?v=o1nHOWhInbY",
        "video_title": "Ugandan National TV Interview with PIPNU",
        "metrics": [
            ("up to 40%", "Reduction in neonatal mortality (KMC, WHO)"),
            ("<5%", "Global KMC coverage for eligible infants"),
            ("12.8 days", "Average age at enrollment (under 28-day target)"),
            ("50% / 70%", "Within-3-days-of-discharge: actual vs target"),
        ],
        "challenge": "2.3 million newborns die in the first 28 days of life — 80% are low birth weight, two-thirds preterm. KMC reduces neonatal mortality up to 40%, but global coverage remains below 5%. Hospitals discharge families within days; structured at-home follow-up rarely exists.",
        "approach": "FLWs identify SVNs at facilities, conduct 4–5 structured home visits within 60 days post-discharge. Counseling on skin-to-skin care and exclusive breastfeeding. Equipment-based screening. Payment per verified completed case ($60).",
        "insight_ids": ["I10"],
    },
    "ecd": {
        "name": "Early Childhood Development",
        "tagline": "Parent-focused intervention for the first 1,000 days of life.",
        "regions": "Malawi, Mozambique, Nigeria",
        "scale": "27,000+ visits · 80k target for 2025 · goal 250,000 caregivers in 24 months",
        "funders": "Founders Pledge",
        "partners": "PACHI · Solina · others",
        "video": None,
        "video_title": None,
        "metrics": [
            ("+33%", "Knowledge of rapid-development timing"),
            ("+41%", "Ways to support mental development"),
            ("+21%", "Observed teaching behavior"),
            ("$7–$18", "Cost per child (Nigeria · Mozambique)"),
        ],
        "challenge": "250 million children in low- and middle-income countries are at risk of not achieving developmental potential. 90% of brain development happens by age 5. Caregivers have limited access to evidence-based parenting guidance.",
        "approach": "Trained FLWs deliver structured home visits — caregiver registration, ECD counseling, talk-and-play guidance, age-appropriate developmental activities. Pilot was 3 visits; expanding to 8–10 visits over 12 months.",
        "insight_ids": ["I7", "I8"],
    },
    "readers": {
        "name": "Readers — Reading Glasses Distribution",
        "tagline": "Door-to-door distribution of donated reading glasses for adults 35+.",
        "regions": "Northeast Nigeria",
        "scale": "15,000 pairs of reading glasses (donated by RestoringVision)",
        "funders": "RestoringVision",
        "partners": "eHA · C3HD",
        "video": None,
        "video_title": None,
        "metrics": [
            ("15,000", "Reading glasses pairs donated"),
            ("+1.0–+3.0", "Diopter range distributed"),
            ("35+", "Target adult age"),
            ("First", "Pair of corrective lenses for many recipients"),
        ],
        "challenge": "Presbyopia — age-related near vision loss — limits productivity, education, and economic participation. Traditional vision care programs require travel to clinics; rural populations don't access them.",
        "approach": "Mobile-guided near vision screening protocol. FLWs trained digitally on screening and lens-strength assessment. Door-to-door household visits, adults 35+, glasses fitted on-site. GPS + biometric verification of each distribution; mobile-money payment per verified visit.",
        "insight_ids": [],
    },
}

# LDVP step content
LDVP = {
    "learn": {
        "name": "Learn",
        "tagline": "Self-paced, offline-first training that turns knowledge into competence.",
        "headline_metric": ("88%", "score above 70% on first observed visits"),
        "summary": "Frontline workers learn through a layered model: self-paced digital coursework, an in-app knowledge test, daily AI coach interaction, peer practice, and a supervised observation visit before they begin paid service delivery.",
        "insight_ids": ["I7", "I8"],
    },
    "deliver": {
        "name": "Deliver",
        "tagline": "Locally-led organizations, performance-based contracts, app-guided visits.",
        "headline_metric": ("44", "LLOs activated in 14 months (CHC)"),
        "summary": "We don't pre-vet partners — we Trial Run them. We don't centralize what locally-led organizations know about their own communities — we let them apply it. And when something fails, we publish what failed and what we changed.",
        "insight_ids": ["I1", "I6", "I9"],
    },
    "verify": {
        "name": "Verify",
        "tagline": "Four independent layers between a payment and a fabrication.",
        "headline_metric": ("AUC 0.91", "fraud detection from three data points alone"),
        "summary": "Microplans force workers into harder areas. Adversarial paid-bonus testing keeps the fraud-detection model honest. Guardrails are audited, not enforced — because punishing missed targets trains FLWs to falsify data.",
        "insight_ids": ["I2", "I3", "I10"],
    },
    "pay": {
        "name": "Pay",
        "tagline": "Cost per verified visit. The metric that doesn't hide the lever.",
        "headline_metric": ("22%", "cost reduction in CHC as it scaled"),
        "summary": "Most platforms report cost-per-FLW-trained or cost-per-app-installed. We report cost-per-verified-visit, broken out by commodity bundle, with setup fees separated. And when a funder asks whether campaign work crowds out routine care, we have the survey to answer.",
        "insight_ids": ["I4", "I5"],
    },
}

LDVP_ORDER = ["learn", "deliver", "verify", "pay"]

# Trail teasers — exact strings, lint-checked
TRAIL_TEASERS = {
    "verify_hero": "We paid FLWs bonuses to defeat our fraud detection — they couldn't. 97.5% scored cleaner than the lowest fabricator. →",
    "chc": "In CHC, microplans tripled visits-per-child from 0.4 to 1.4 and pushed coverage from 84% to 94%. →",
    "kmc": "KMC reduces neonatal mortality up to 40%, yet global coverage is below 5% — we close the post-discharge gap. →",
    "ecd": "Caregivers' ECD attitudes were already correct — we moved knowledge +33% and observed teaching behavior +21%. →",
    "readers": "RestoringVision's 15,000 reading-glasses pairs delivered through Connect's verified-payment model. →",
    "learn": "Knowledge tests didn't produce competent FLWs — we layered an AI coach. 88% score above 70% on first observed visits. →",
    "deliver": "We invented the Trial Run because pre-vetting LLOs didn't predict performance — 65% conversion through it. →",
    "verify": "Workers naturally cluster — microplans force them into harder areas, and fraud detection hits AUC 0.91. →",
    "pay": "In CHC, cost per verified visit fell 22% — Nigeria $1.30 with ORS, outside Nigeria $0.78 without. →",
    "insights": "Every claim, scoped to its evidence — the buffet view of what we've learned across programs. →",
}

# Open Questions Roster — page → list of open questions
OPEN_QUESTIONS = {
    "learn": [
        "Whether the AI coach or peer practice contributes more to the 77% supervised-observation pass rate — we have not yet published the decomposition.",
        "Whether the 97.8% AI-coach handle rate from the Kenya CHC pilot holds in non-English-language deployments.",
        "Encouragement-of-autonomy is the hardest ECD sub-domain (47% endline). Whether 8–10 visits will move it, or it needs a different design entirely.",
    ],
    "deliver": [
        "Whether the 65% Trial Run conversion holds outside CHC — KMC, ECD, and Readers are still on too small a contract base to publish their own.",
        "'Fragile context requires in-country presence' is a coarse rule learned from CAR. We don't have a sharper predictive model yet.",
        "We have not built a structured framework for capturing what individual LLOs invent locally — the real intervention often lives in their heads.",
    ],
    "verify": [
        "The 97.5% adversarial detection is from paid-bonus testing in CHC. Production false-positive rates against unmotivated fabrication aren't yet published.",
        "Microplans failed in dispersed settlement patterns. We don't yet have a clean threshold for when settlement density makes microplanning counterproductive.",
        "Photo verification quality degrades on low bandwidth. False-positive rate on the photo layer in low-bandwidth deployments isn't yet published.",
    ],
    "pay": [
        "The $1.70 weighted average masks bundle differences ($1.30 Nigeria with ORS, $0.78 outside). Whether the 22% year-over-year curve holds in non-CHC programs is open.",
        "The N=24 displacement survey is in two Nigerian states. Whether 'campaigns are routine' holds in CHV systems with different structures — re-survey first.",
        "Setup-fee projection ($0.40 → ~$0.10/visit at scale) is forward-looking. We will publish the converged number when the next cohort closes.",
    ],
    "chc": [
        "Whether the cost-per-verified-visit advantage holds outside Nigeria's commodity bundle — IPA RCT 2026 ($1.5M, PRO Impact) will test.",
        "The 65% Trial Run conversion criteria are program-manager judgment calls today, not codified into a model an outside funder could replicate.",
        "Microplan execution failed in CAR's dispersed settlement and on inaccessible land. We removed it from one campaign entirely.",
    ],
    "kmc": [
        "Whether discharge-notification integration alone closes the 50% → 70% within-3-days enrollment gap, or the 3-day target itself needs to be redesigned.",
        "Equipment availability across the 6 KMC LLO partners has been uneven. We don't yet have a published audit of equipment uptime.",
        "Whether KMC FLWs will sustain ≥4 visits per case at the 5,000+ scale; current average is 3.4 against a 5-visit guardrail.",
    ],
    "ecd": [
        "The 47% endline on encouragement-of-autonomy is the hardest sub-domain. Whether 8–10 visits will move it is open.",
        "The Malawi pilot is N=50 caregivers. Whether the attitude-already-correct finding holds in Mozambique and Nigeria contexts is open.",
        "Whether AI coach contribution to the 77% pass rate generalizes outside ECD — we have not run the controlled comparison.",
    ],
    "readers": [
        "LLOs finalized (eHA, C3HD); contract signing pending. Field-performance data won't exist until the first cohort runs.",
        "Whether the screening protocol holds quality consistency across novice FLWs trained only digitally — first cohort will tell.",
        "Whether door-to-door distribution finds the right adults (35+, presbyopic) at sufficient rates without targeting infrastructure.",
    ],
    "insights": [
        "This page is only as honest as the insights and nuggets the team mines. Internal lore that didn't make it onto the public site is the rate-limiter.",
        "Numbers without benchmarks are excluded by policy — but our benchmark library is uneven across programs. KMC and Readers have thinner comparators than CHC.",
        "Whether the methodology-footer framing ('we have a methodology for what's on the website') survives a year of new programs without drift toward marketing copy.",
    ],
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def insight_by_id(iid):
    return next(i for i in INSIGHTS if i["id"] == iid)

def nuggets_for_home(home):
    return [n for n in NUGGETS if n["home"] == home]

def open_questions_html(page_key):
    qs = OPEN_QUESTIONS[page_key]
    items = "\n".join(
        f'    <li><strong>What we don\'t know yet — Q{i+1}.</strong><p>{q}</p></li>'
        for i, q in enumerate(qs)
    )
    return f'<section class="open-questions" aria-label="Open questions">\n  <h3>What we don\'t know yet</h3>\n  <ul>\n{items}\n  </ul>\n</section>'

# ---------------------------------------------------------------------------
# Variant: v10a — Foundation memo (Pattern C, serif, dense, footnoted)
# ---------------------------------------------------------------------------

V10A_CSS = """
:root{
  --ink:#16006D;
  --ink-soft:#3a2f6e;
  --body:#2b2742;
  --muted:#615a7a;
  --rule:#d9d3e8;
  --accent:#3843D0;
  --highlight:#FC5F36;
  --paper:#fbf9f3;
  --paper-tint:#f3efe4;
  --shadow:rgba(22,0,109,0.08);
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'EB Garamond','Iowan Old Style','Georgia',serif;background:var(--paper);color:var(--body);line-height:1.55;font-size:18px}
.serif{font-family:'EB Garamond','Iowan Old Style','Georgia',serif}
.mono{font-family:'IBM Plex Mono','Courier New',monospace;font-size:0.82em;letter-spacing:0.02em}
.small-caps{font-family:'IBM Plex Sans','Helvetica Neue',sans-serif;text-transform:uppercase;letter-spacing:0.13em;font-size:0.72em;color:var(--muted);font-weight:600}
a{color:var(--accent);text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:2px}
a:hover{color:var(--highlight)}
nav.top{position:sticky;top:0;background:var(--paper);border-bottom:1px solid var(--rule);z-index:50;padding:14px 0}
nav.top .inner{max-width:1100px;margin:0 auto;padding:0 36px;display:flex;align-items:center;justify-content:space-between;gap:24px}
nav.top .brand{font-family:'IBM Plex Sans',sans-serif;font-weight:600;color:var(--ink);text-decoration:none;font-size:1.05rem;letter-spacing:0.01em}
nav.top .brand .by{color:var(--muted);font-weight:400;font-style:italic;margin-left:6px}
nav.top ul{list-style:none;display:flex;gap:22px;flex-wrap:wrap}
nav.top ul a{font-family:'IBM Plex Sans',sans-serif;font-size:0.88rem;color:var(--ink-soft);text-decoration:none;font-weight:500}
nav.top ul a:hover{color:var(--highlight)}
nav.top .demo{padding:8px 14px;background:var(--ink);color:var(--paper);border-radius:2px;font-family:'IBM Plex Sans',sans-serif;font-size:0.86rem;text-decoration:none}
main{max-width:780px;margin:0 auto;padding:60px 36px 120px;position:relative}
main.wide{max-width:1100px}
header.memo{border-bottom:2px solid var(--ink);padding-bottom:28px;margin-bottom:48px}
header.memo .label{font-family:'IBM Plex Sans',sans-serif;text-transform:uppercase;letter-spacing:0.18em;font-size:0.72rem;color:var(--accent);font-weight:600;margin-bottom:14px}
header.memo h1{font-family:'EB Garamond',serif;font-weight:500;color:var(--ink);font-size:clamp(2.2rem,4.5vw,3.4rem);line-height:1.1;letter-spacing:-0.01em;margin-bottom:18px}
header.memo .lede{font-style:italic;color:var(--ink-soft);font-size:1.18rem;line-height:1.5;max-width:62ch}
header.memo .meta{display:flex;flex-wrap:wrap;gap:24px;margin-top:24px;font-family:'IBM Plex Sans',sans-serif;font-size:0.8rem;color:var(--muted)}
header.memo .meta strong{color:var(--ink);font-weight:600}
section.entry{margin:64px 0;padding:0;border-top:1px solid var(--rule);padding-top:36px}
section.entry h2{font-family:'EB Garamond',serif;color:var(--ink);font-weight:500;font-size:1.7rem;line-height:1.25;margin-bottom:8px;letter-spacing:-0.01em}
section.entry .meta-row{display:flex;flex-wrap:wrap;gap:14px;font-family:'IBM Plex Sans',sans-serif;font-size:0.78rem;color:var(--muted);margin-bottom:22px}
section.entry .scope-tag{background:var(--paper-tint);padding:3px 10px;border-radius:2px;color:var(--ink-soft);font-weight:500}
section.entry .tier-tag{padding:3px 10px;border-radius:2px;font-weight:500}
.tier-hard{background:#e8f0d8;color:#3a4d1a}
.tier-tri{background:#f3e6d4;color:#7a4d1a}
.tier-lived{background:#e6e0f3;color:#36246e}
section.entry p{margin-bottom:1.1em;font-size:1.02rem;line-height:1.65}
section.entry .stand{font-style:italic;color:var(--ink-soft);border-left:3px solid var(--accent);padding:6px 0 6px 18px;margin:18px 0;font-size:1.02rem}
sup.fn{color:var(--accent);font-family:'IBM Plex Sans',sans-serif;font-size:0.62em;font-weight:600;vertical-align:super;cursor:help;text-decoration:none}
.footnote{font-family:'IBM Plex Sans',sans-serif;font-size:0.78rem;color:var(--muted);line-height:1.5;border-top:1px dotted var(--rule);padding-top:14px;margin-top:22px}
.footnote .fn-num{color:var(--accent);font-weight:600;margin-right:6px}
.kicker{font-family:'IBM Plex Sans',sans-serif;text-transform:uppercase;letter-spacing:0.16em;font-size:0.7rem;font-weight:600;color:var(--accent);margin-bottom:10px}
.open-questions{background:var(--paper-tint);border-left:3px solid var(--highlight);padding:24px 28px;margin:48px 0;border-radius:2px}
.open-questions h3{font-family:'IBM Plex Sans',sans-serif;text-transform:uppercase;letter-spacing:0.13em;font-size:0.78rem;color:var(--ink);margin-bottom:14px}
.open-questions ul{list-style:none}
.open-questions li{margin-bottom:14px;padding-left:0}
.open-questions li:last-child{margin-bottom:0}
.open-questions strong{font-family:'IBM Plex Sans',sans-serif;font-size:0.82rem;color:var(--ink);display:block;margin-bottom:4px;font-weight:600}
.open-questions p{font-size:0.95rem;color:var(--ink-soft);line-height:1.55}
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1px;background:var(--rule);border:1px solid var(--rule);margin:32px 0}
.metrics .m{background:var(--paper);padding:22px 18px}
.metrics .m .num{font-family:'EB Garamond',serif;font-size:1.9rem;color:var(--ink);font-weight:500;line-height:1}
.metrics .m .lab{font-family:'IBM Plex Sans',sans-serif;font-size:0.74rem;color:var(--muted);text-transform:uppercase;letter-spacing:0.06em;margin-top:8px}
.cta-row{margin-top:48px;padding-top:28px;border-top:1px solid var(--rule);display:flex;flex-wrap:wrap;gap:18px;justify-content:space-between;align-items:center}
.cta-row a{font-family:'IBM Plex Sans',sans-serif;font-size:0.92rem;color:var(--accent);text-decoration:none;font-weight:500}
.cta-row a:hover{color:var(--highlight);text-decoration:underline}
.trail-list{list-style:none;margin:32px 0}
.trail-list li{border-top:1px solid var(--rule);padding:18px 0}
.trail-list li:last-child{border-bottom:1px solid var(--rule)}
.trail-list a{display:block;font-family:'EB Garamond',serif;font-size:1.18rem;color:var(--ink);font-weight:500;line-height:1.4;text-decoration:none}
.trail-list a:hover{color:var(--highlight)}
.trail-list .sub{font-family:'IBM Plex Sans',sans-serif;font-size:0.78rem;color:var(--muted);margin-top:4px}
footer.bottom{border-top:1px solid var(--rule);background:var(--paper-tint);padding:48px 36px;font-family:'IBM Plex Sans',sans-serif;font-size:0.84rem;color:var(--muted);text-align:center;margin-top:80px}
footer.bottom .signoff{font-family:'EB Garamond',serif;font-style:italic;font-size:1rem;color:var(--ink-soft);margin-bottom:14px}
.transition-link{display:inline-block;border:1px solid var(--ink);padding:14px 22px;font-family:'IBM Plex Sans',sans-serif;font-size:0.86rem;color:var(--ink);text-decoration:none;font-weight:500;margin-top:12px;transition:all 0.2s}
.transition-link:hover{background:var(--ink);color:var(--paper)}
.video-link{display:inline-block;background:var(--ink);color:var(--paper);padding:12px 20px;font-family:'IBM Plex Sans',sans-serif;font-size:0.84rem;text-decoration:none;border-radius:2px;margin-top:14px}
.video-link:hover{background:var(--accent);color:var(--paper)}
.insights-group{margin:48px 0}
.insights-group h2{font-family:'IBM Plex Sans',sans-serif;text-transform:uppercase;letter-spacing:0.18em;font-size:0.86rem;color:var(--accent);font-weight:600;border-bottom:1px solid var(--rule);padding-bottom:10px;margin-bottom:24px}
.insights-list{list-style:none}
.insights-list li{padding:18px 0;border-bottom:1px dotted var(--rule)}
.insights-list .claim{font-family:'EB Garamond',serif;font-size:1.06rem;color:var(--ink);line-height:1.5;margin-bottom:6px}
.insights-list .meta{font-family:'IBM Plex Sans',sans-serif;font-size:0.76rem;color:var(--muted);display:flex;gap:12px;flex-wrap:wrap}
.insights-list .open-q{font-family:'EB Garamond',serif;font-style:italic;font-size:0.94rem;color:var(--ink-soft);margin-top:8px}
.method-footer{background:var(--paper-tint);padding:28px 32px;border-left:3px solid var(--ink);margin-top:48px;font-size:1rem;line-height:1.65}
.method-footer h3{font-family:'IBM Plex Sans',sans-serif;text-transform:uppercase;letter-spacing:0.13em;font-size:0.78rem;color:var(--ink);margin-bottom:10px}
.method-footer p{margin-bottom:0.8em}
.method-footer p:last-child{margin-bottom:0}
@media(max-width:720px){
  body{font-size:17px}
  main{padding:40px 22px 80px}
  nav.top .inner{flex-direction:column;align-items:flex-start;gap:12px}
  nav.top ul{gap:14px}
  header.memo h1{font-size:2rem}
  section.entry h2{font-size:1.4rem}
  .metrics{grid-template-columns:1fr 1fr}
  .insights-list .meta{font-size:0.7rem}
}
"""

# ---------------------------------------------------------------------------
# Variant: v10b — Field dispatch (large editorial typography, journal voice)
# ---------------------------------------------------------------------------

V10B_CSS = """
:root{
  --ink:#1a1a1a;
  --ink-soft:#3d3d3d;
  --body:#2a2a2a;
  --muted:#7a7570;
  --rule:#e8e2da;
  --accent:#3843D0;
  --highlight:#FC5F36;
  --bg:#f5f0e8;
  --bg-tint:#ede5d6;
  --card:#fdfaf3;
  --shadow:rgba(0,0,0,0.06);
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Source Serif Pro','Charter','Georgia',serif;background:var(--bg);color:var(--body);line-height:1.6;font-size:18px}
.sans{font-family:'Inter','Helvetica Neue',sans-serif}
a{color:var(--ink);text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px;text-decoration-color:var(--highlight)}
a:hover{color:var(--highlight)}
nav.dispatch{position:sticky;top:0;background:var(--bg);z-index:50;padding:18px 0;border-bottom:1px solid var(--rule)}
nav.dispatch .inner{max-width:1240px;margin:0 auto;padding:0 40px;display:flex;align-items:center;justify-content:space-between;gap:24px}
nav.dispatch .brand{font-family:'Inter',sans-serif;font-weight:700;color:var(--ink);text-decoration:none;font-size:1rem;letter-spacing:0.04em;text-transform:uppercase}
nav.dispatch .brand .by{font-weight:400;color:var(--muted);text-transform:none;letter-spacing:0;margin-left:8px;font-style:italic}
nav.dispatch ul{list-style:none;display:flex;gap:26px;flex-wrap:wrap}
nav.dispatch ul a{font-family:'Inter',sans-serif;font-size:0.86rem;color:var(--ink-soft);text-decoration:none;font-weight:500;text-transform:uppercase;letter-spacing:0.08em}
nav.dispatch ul a:hover{color:var(--highlight)}
nav.dispatch .demo{padding:9px 16px;background:var(--highlight);color:#fff;border-radius:0;font-family:'Inter',sans-serif;font-size:0.78rem;text-decoration:none;text-transform:uppercase;letter-spacing:0.1em;font-weight:600}
.hero{max-width:1240px;margin:0 auto;padding:80px 40px 60px}
.hero .dateline{font-family:'Inter',sans-serif;text-transform:uppercase;letter-spacing:0.18em;font-size:0.74rem;color:var(--accent);font-weight:700;margin-bottom:24px}
.hero h1{font-family:'Source Serif Pro',serif;font-weight:300;color:var(--ink);font-size:clamp(2.6rem,6vw,5rem);line-height:1.05;letter-spacing:-0.025em;margin-bottom:24px;max-width:18ch}
.hero h1 em{font-style:italic;font-weight:400;color:var(--accent)}
.hero .lede{font-family:'Source Serif Pro',serif;font-weight:400;color:var(--ink-soft);font-size:1.4rem;line-height:1.45;max-width:54ch;font-style:italic}
.hero .byline{font-family:'Inter',sans-serif;font-size:0.84rem;color:var(--muted);margin-top:32px;display:flex;gap:24px;flex-wrap:wrap}
.hero .byline strong{color:var(--ink)}
main.dispatch-body{max-width:1240px;margin:0 auto;padding:40px 40px 80px;display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:60px}
main.dispatch-body.single{grid-template-columns:minmax(0,720px);justify-content:center}
.body-col{min-width:0}
.side-col{font-family:'Inter',sans-serif;font-size:0.88rem;color:var(--ink-soft)}
.side-col .sticky{position:sticky;top:96px}
.side-col h4{text-transform:uppercase;letter-spacing:0.14em;font-size:0.72rem;color:var(--accent);font-weight:700;margin-bottom:14px}
.side-col .pullquote{font-family:'Source Serif Pro',serif;font-style:italic;font-size:1.4rem;line-height:1.35;color:var(--ink);border-left:3px solid var(--highlight);padding:8px 0 8px 18px;margin:0 0 32px}
.side-col .meta-block{margin-bottom:32px}
.side-col .meta-block .lab{text-transform:uppercase;letter-spacing:0.1em;font-size:0.68rem;color:var(--muted);margin-bottom:6px;font-weight:600}
.side-col .meta-block .val{color:var(--ink);font-size:0.95rem;line-height:1.45}
section.dispatch-entry{margin-bottom:80px;padding-top:48px;border-top:1px solid var(--rule)}
section.dispatch-entry .kicker{font-family:'Inter',sans-serif;text-transform:uppercase;letter-spacing:0.18em;font-size:0.72rem;color:var(--accent);font-weight:700;margin-bottom:14px}
section.dispatch-entry h2{font-family:'Source Serif Pro',serif;font-weight:400;font-size:clamp(1.6rem,3.5vw,2.6rem);line-height:1.15;color:var(--ink);margin-bottom:18px;letter-spacing:-0.015em}
section.dispatch-entry h2 em{font-style:italic;color:var(--highlight)}
section.dispatch-entry .timeline{margin:32px 0;border-left:2px solid var(--rule);padding-left:24px;position:relative}
section.dispatch-entry .timeline-step{margin-bottom:28px;position:relative}
section.dispatch-entry .timeline-step::before{content:'';position:absolute;left:-32px;top:8px;width:12px;height:12px;background:var(--bg);border:2px solid var(--accent);border-radius:50%}
section.dispatch-entry .timeline-step .when{font-family:'Inter',sans-serif;text-transform:uppercase;letter-spacing:0.13em;font-size:0.74rem;color:var(--accent);font-weight:700;margin-bottom:6px}
section.dispatch-entry .timeline-step p{font-family:'Source Serif Pro',serif;font-size:1.06rem;line-height:1.6;color:var(--body)}
section.dispatch-entry p{margin-bottom:1.1em;font-size:1.1rem;line-height:1.7}
section.dispatch-entry p:first-of-type::first-letter{font-family:'Source Serif Pro',serif;font-size:4em;line-height:0.9;float:left;padding:6px 12px 0 0;color:var(--accent);font-weight:300}
section.dispatch-entry .stand{font-family:'Source Serif Pro',serif;font-style:italic;font-size:1.4rem;line-height:1.4;color:var(--ink);margin:32px 0;padding:8px 0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.metrics-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:0;margin:48px 0;border-top:2px solid var(--ink);border-bottom:2px solid var(--ink)}
.metrics-strip .m{padding:24px 16px;border-right:1px solid var(--rule);text-align:center}
.metrics-strip .m:last-child{border-right:none}
.metrics-strip .num{font-family:'Source Serif Pro',serif;font-size:2.4rem;font-weight:300;color:var(--ink);line-height:1}
.metrics-strip .lab{font-family:'Inter',sans-serif;font-size:0.74rem;color:var(--muted);text-transform:uppercase;letter-spacing:0.08em;margin-top:8px}
.open-questions{background:var(--card);border:1px solid var(--rule);padding:36px 40px;margin:60px 0;position:relative}
.open-questions::before{content:'?';position:absolute;left:-22px;top:24px;width:44px;height:44px;background:var(--highlight);color:#fff;font-family:'Source Serif Pro',serif;font-size:1.8rem;font-weight:700;border-radius:50%;display:flex;align-items:center;justify-content:center}
.open-questions h3{font-family:'Inter',sans-serif;text-transform:uppercase;letter-spacing:0.14em;font-size:0.78rem;color:var(--ink);margin-bottom:18px;font-weight:700}
.open-questions ul{list-style:none}
.open-questions li{margin-bottom:18px;padding-left:0}
.open-questions li:last-child{margin-bottom:0}
.open-questions strong{font-family:'Inter',sans-serif;font-size:0.82rem;color:var(--accent);font-weight:600;display:block;margin-bottom:6px}
.open-questions p{font-family:'Source Serif Pro',serif;font-size:1.02rem;color:var(--ink-soft);line-height:1.6;font-style:italic}
.trail-list{list-style:none;margin:48px 0;border-top:2px solid var(--ink)}
.trail-list li{border-bottom:1px solid var(--rule);padding:24px 0}
.trail-list a{display:block;font-family:'Source Serif Pro',serif;font-size:1.4rem;color:var(--ink);font-weight:400;line-height:1.35;text-decoration:none;letter-spacing:-0.01em}
.trail-list a:hover{color:var(--highlight)}
.trail-list .sub{font-family:'Inter',sans-serif;text-transform:uppercase;letter-spacing:0.1em;font-size:0.7rem;color:var(--muted);margin-top:6px;font-weight:600}
.video-link{display:inline-block;background:var(--ink);color:#fff;padding:14px 24px;font-family:'Inter',sans-serif;font-size:0.84rem;text-decoration:none;text-transform:uppercase;letter-spacing:0.08em;font-weight:600;margin-top:18px}
.video-link:hover{background:var(--highlight)}
footer.dispatch-footer{background:var(--ink);color:var(--bg-tint);padding:60px 40px;font-family:'Inter',sans-serif}
footer.dispatch-footer .inner{max-width:1240px;margin:0 auto}
footer.dispatch-footer .signoff{font-family:'Source Serif Pro',serif;font-style:italic;font-size:1.4rem;color:var(--bg);max-width:60ch;margin-bottom:32px;font-weight:300}
footer.dispatch-footer .meta{display:flex;flex-wrap:wrap;gap:32px;font-size:0.84rem;color:var(--muted)}
footer.dispatch-footer a{color:var(--bg-tint);text-decoration-color:var(--highlight)}
.insights-group{margin:64px 0}
.insights-group h2{font-family:'Inter',sans-serif;text-transform:uppercase;letter-spacing:0.18em;font-size:0.88rem;color:var(--accent);font-weight:700;border-top:2px solid var(--ink);padding-top:14px;margin-bottom:24px}
.insights-list{list-style:none}
.insights-list li{padding:24px 0;border-bottom:1px solid var(--rule)}
.insights-list .claim{font-family:'Source Serif Pro',serif;font-size:1.2rem;color:var(--ink);line-height:1.5;margin-bottom:8px}
.insights-list .meta{font-family:'Inter',sans-serif;font-size:0.74rem;color:var(--muted);display:flex;gap:14px;flex-wrap:wrap;text-transform:uppercase;letter-spacing:0.07em}
.insights-list .open-q{font-family:'Source Serif Pro',serif;font-style:italic;font-size:1rem;color:var(--ink-soft);margin-top:10px;border-left:2px solid var(--highlight);padding-left:14px}
.method-footer{background:var(--card);border:1px solid var(--rule);padding:36px 40px;margin-top:64px}
.method-footer h3{font-family:'Inter',sans-serif;text-transform:uppercase;letter-spacing:0.14em;font-size:0.82rem;color:var(--ink);margin-bottom:14px;font-weight:700}
.method-footer p{font-family:'Source Serif Pro',serif;font-size:1.06rem;line-height:1.7;color:var(--ink-soft);margin-bottom:1em}
.method-footer p:last-child{margin-bottom:0}
@media(max-width:900px){
  main.dispatch-body{grid-template-columns:1fr;gap:32px}
  .side-col .sticky{position:static}
  .hero{padding:50px 24px 36px}
  main.dispatch-body{padding:24px 24px 60px}
  .hero h1{font-size:2.4rem}
  nav.dispatch ul{gap:14px}
  nav.dispatch .inner{flex-direction:column;align-items:flex-start;gap:14px}
  .open-questions{padding:24px 24px}
  .open-questions::before{display:none}
  section.dispatch-entry p:first-of-type::first-letter{font-size:3em}
}
"""

# ---------------------------------------------------------------------------
# Variant: v10c — Knowledge graph (interlinked, evidence badges, dense)
# ---------------------------------------------------------------------------

V10C_CSS = """
:root{
  --bg:#0e1126;
  --bg-2:#161a35;
  --bg-3:#1f2444;
  --ink:#f5f5fa;
  --ink-soft:#cdd0e0;
  --muted:#8e90a8;
  --rule:#2a2f50;
  --accent:#8EA1FF;
  --accent-2:#5b6cf0;
  --hot:#FC5F36;
  --gold:#FEAF31;
  --green:#7adcb6;
  --tier-hard:#7adcb6;
  --tier-tri:#FEAF31;
  --tier-lived:#FC5F36;
  --tier-hyp:#8EA1FF;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Inter','Helvetica Neue',sans-serif;background:var(--bg);color:var(--ink);line-height:1.55;font-size:16px;-webkit-font-smoothing:antialiased}
.mono{font-family:'JetBrains Mono','Courier New',monospace;font-size:0.86em;letter-spacing:0.01em}
.serif{font-family:'Newsreader','Georgia',serif}
a{color:var(--accent);text-decoration:none}
a:hover{color:var(--hot)}
nav.graph{position:sticky;top:0;background:rgba(14,17,38,0.92);backdrop-filter:blur(8px);z-index:50;border-bottom:1px solid var(--rule);padding:14px 0}
nav.graph .inner{max-width:1320px;margin:0 auto;padding:0 32px;display:flex;align-items:center;justify-content:space-between;gap:24px}
nav.graph .brand{font-family:'JetBrains Mono',monospace;font-size:0.94rem;color:var(--ink);text-decoration:none;letter-spacing:0.02em}
nav.graph .brand::before{content:'⬢ ';color:var(--accent)}
nav.graph ul{list-style:none;display:flex;gap:6px;flex-wrap:wrap}
nav.graph ul a{font-family:'Inter',sans-serif;font-size:0.82rem;color:var(--ink-soft);text-decoration:none;font-weight:500;padding:6px 10px;border-radius:4px;transition:all 0.15s}
nav.graph ul a:hover{color:var(--ink);background:var(--bg-3)}
nav.graph .demo{padding:8px 14px;background:var(--hot);color:#fff;border-radius:4px;font-family:'Inter',sans-serif;font-size:0.82rem;text-decoration:none;font-weight:600}
.hero{max-width:1320px;margin:0 auto;padding:60px 32px 40px}
.hero .breadcrumb{font-family:'JetBrains Mono',monospace;font-size:0.74rem;color:var(--muted);margin-bottom:18px}
.hero .breadcrumb a{color:var(--muted)}
.hero .breadcrumb a:hover{color:var(--accent)}
.hero h1{font-family:'Inter',sans-serif;font-weight:700;color:var(--ink);font-size:clamp(2rem,4.5vw,3.6rem);line-height:1.08;letter-spacing:-0.02em;margin-bottom:18px;max-width:24ch}
.hero h1 .accent{color:var(--accent)}
.hero .lede{font-size:1.16rem;color:var(--ink-soft);max-width:60ch;line-height:1.55}
.hero .meta{display:flex;flex-wrap:wrap;gap:16px;margin-top:28px;font-family:'JetBrains Mono',monospace;font-size:0.8rem;color:var(--muted)}
.hero .meta strong{color:var(--ink)}
main.graph-body{max-width:1320px;margin:0 auto;padding:24px 32px 100px}
.tier-badge{display:inline-flex;align-items:center;gap:6px;padding:3px 9px;border-radius:3px;font-family:'JetBrains Mono',monospace;font-size:0.66rem;text-transform:uppercase;letter-spacing:0.06em;font-weight:600;border:1px solid;line-height:1.4}
.tier-badge::before{content:'';width:6px;height:6px;border-radius:50%;display:inline-block}
.tier-badge.hard{color:var(--tier-hard);border-color:var(--tier-hard)}
.tier-badge.hard::before{background:var(--tier-hard)}
.tier-badge.tri,.tier-badge.triangulated{color:var(--tier-tri);border-color:var(--tier-tri)}
.tier-badge.tri::before,.tier-badge.triangulated::before{background:var(--tier-tri)}
.tier-badge.lived{color:var(--tier-lived);border-color:var(--tier-lived)}
.tier-badge.lived::before{background:var(--tier-lived)}
.tier-badge.hypothesis{color:var(--tier-hyp);border-color:var(--tier-hyp)}
.tier-badge.hypothesis::before{background:var(--tier-hyp)}
.scope-badge{display:inline-block;padding:3px 9px;border-radius:3px;font-family:'JetBrains Mono',monospace;font-size:0.66rem;text-transform:uppercase;letter-spacing:0.06em;font-weight:600;background:var(--bg-3);color:var(--ink-soft)}
section.entry{background:var(--bg-2);border:1px solid var(--rule);border-radius:8px;padding:28px 32px;margin-bottom:24px;position:relative;overflow:hidden}
section.entry::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--accent)}
section.entry .header-row{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:14px;align-items:center}
section.entry .id-tag{font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:var(--muted);background:var(--bg-3);padding:3px 8px;border-radius:3px}
section.entry h2{font-family:'Inter',sans-serif;font-weight:700;font-size:1.5rem;line-height:1.25;color:var(--ink);margin-bottom:14px;letter-spacing:-0.01em}
section.entry .question{font-family:'Newsreader',serif;font-style:italic;font-size:1.4rem;color:var(--accent);line-height:1.3;margin-bottom:18px}
section.entry .struct{margin:18px 0}
section.entry .struct h3{font-family:'JetBrains Mono',monospace;font-size:0.74rem;text-transform:uppercase;letter-spacing:0.13em;color:var(--accent);margin-bottom:8px;font-weight:600}
section.entry .struct p{font-size:0.98rem;line-height:1.65;color:var(--ink-soft);margin-bottom:0}
section.entry .source{margin-top:18px;padding-top:14px;border-top:1px solid var(--rule);font-family:'JetBrains Mono',monospace;font-size:0.74rem;color:var(--muted)}
.metrics-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin:32px 0}
.metrics-grid .m{background:var(--bg-2);border:1px solid var(--rule);border-radius:6px;padding:20px}
.metrics-grid .num{font-family:'Inter',sans-serif;font-size:2rem;font-weight:700;color:var(--accent);line-height:1;letter-spacing:-0.02em}
.metrics-grid .lab{font-family:'Inter',sans-serif;font-size:0.78rem;color:var(--muted);margin-top:8px;line-height:1.4}
.open-questions{background:var(--bg-2);border:1px solid var(--rule);border-left:3px solid var(--hot);border-radius:6px;padding:24px 28px;margin:36px 0}
.open-questions h3{font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:0.13em;font-size:0.78rem;color:var(--hot);margin-bottom:14px;font-weight:600}
.open-questions ul{list-style:none}
.open-questions li{margin-bottom:14px;padding-left:0}
.open-questions li:last-child{margin-bottom:0}
.open-questions strong{font-family:'Inter',sans-serif;font-size:0.84rem;color:var(--ink);font-weight:600;display:block;margin-bottom:4px}
.open-questions p{font-size:0.94rem;color:var(--ink-soft);line-height:1.55;margin-bottom:0}
.trail-list{list-style:none;margin:32px 0;display:grid;gap:10px}
.trail-list li{}
.trail-list a{display:block;background:var(--bg-2);border:1px solid var(--rule);border-radius:6px;padding:18px 22px;text-decoration:none;transition:all 0.15s}
.trail-list a:hover{border-color:var(--accent);background:var(--bg-3)}
.trail-list .claim{font-family:'Inter',sans-serif;font-size:1.04rem;color:var(--ink);line-height:1.45;font-weight:500}
.trail-list .badges{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}
.video-link{display:inline-block;background:var(--accent);color:var(--bg);padding:10px 16px;border-radius:5px;font-family:'Inter',sans-serif;font-size:0.84rem;text-decoration:none;font-weight:600;margin-top:16px}
.video-link:hover{background:var(--hot);color:var(--ink)}
.transition-link{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--accent);padding:10px 18px;font-family:'Inter',sans-serif;font-size:0.86rem;color:var(--accent);text-decoration:none;font-weight:500;border-radius:5px;margin-top:16px;transition:all 0.15s}
.transition-link:hover{background:var(--accent);color:var(--bg)}
footer.graph-footer{background:var(--bg-2);border-top:1px solid var(--rule);padding:48px 32px;font-family:'Inter',sans-serif;font-size:0.86rem;color:var(--muted)}
footer.graph-footer .inner{max-width:1320px;margin:0 auto;display:flex;justify-content:space-between;flex-wrap:wrap;gap:24px}
footer.graph-footer a{color:var(--ink-soft)}
.insights-group{margin:48px 0}
.insights-group h2{font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:0.16em;font-size:0.88rem;color:var(--accent);font-weight:600;border-bottom:1px solid var(--rule);padding-bottom:10px;margin-bottom:18px}
.insights-list{list-style:none;display:grid;gap:12px}
.insights-list li{background:var(--bg-2);border:1px solid var(--rule);border-radius:6px;padding:18px 22px;border-left:3px solid var(--accent)}
.insights-list .claim{font-size:1.02rem;color:var(--ink);line-height:1.5;margin-bottom:10px;font-weight:500}
.insights-list .badges{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px}
.insights-list .open-q{font-family:'Newsreader',serif;font-style:italic;font-size:0.94rem;color:var(--ink-soft);margin-top:8px;border-left:2px solid var(--hot);padding-left:12px}
.method-footer{background:var(--bg-3);border:1px solid var(--rule);padding:28px 32px;margin-top:48px;border-radius:6px}
.method-footer h3{font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:0.13em;font-size:0.78rem;color:var(--accent);margin-bottom:12px;font-weight:600}
.method-footer p{font-size:0.96rem;line-height:1.65;color:var(--ink-soft);margin-bottom:0.8em}
.method-footer p:last-child{margin-bottom:0}
@media(max-width:760px){
  body{font-size:15.5px}
  .hero{padding:40px 20px 24px}
  main.graph-body{padding:16px 20px 60px}
  .hero h1{font-size:2rem}
  nav.graph .inner{flex-direction:column;align-items:flex-start;gap:12px}
  nav.graph ul{gap:2px}
  section.entry{padding:22px 20px}
  .open-questions{padding:20px}
}
"""

# ---------------------------------------------------------------------------
# Variant rendering
# ---------------------------------------------------------------------------

def slug_tier(tier):
    if "hard" in tier: return "hard"
    if "tri" in tier: return "tri"
    if "lived" in tier: return "lived"
    return "hypothesis"

def page_meta_links(variant, current):
    items = [
        ("/index.html", "Home"),
        ("/learn.html", "Learn"),
        ("/deliver.html", "Deliver"),
        ("/verify.html", "Verify"),
        ("/pay.html", "Pay"),
        ("/programs.html", "Programs"),
        ("/insights.html", "Insights"),
    ]
    out = []
    for href, label in items:
        active = "active" if href.endswith(current) else ""
        out.append(f'<li><a href="{href}" class="{active}">{label}</a></li>')
    return "\n".join(out)

# ----- v10a (Foundation memo) -------------------------------------------------

def render_v10a_nav(current):
    return f"""
<nav class="top">
  <div class="inner">
    <a class="brand" href="/index.html">Connect <span class="by">by Dimagi</span></a>
    <ul>{page_meta_links('a', current)}</ul>
    <a class="demo" href="#contact">Request a memo</a>
  </div>
</nav>
"""

def render_v10a_footer():
    return """
<footer class="bottom">
  <div class="signoff">"Powering the Frontline. Paying for Results."</div>
  <div>Connect by Dimagi · 2026 · 5,000+ FLWs across 12 countries · 880,000+ verified visits in CHC alone</div>
</footer>
"""

def v10a_insight_section(insight, footnote_num):
    tier_cls = f"tier-{slug_tier(insight['evidence_tier'])}"
    return f"""
<section class="entry">
  <div class="kicker">Insight {insight['id'][1:]}</div>
  <h2>{insight['title']}</h2>
  <div class="meta-row">
    <span class="scope-tag">Scope: {insight['scope']}</span>
    <span class="tier-tag {tier_cls}">Evidence: {insight['tier_label']}</span>
  </div>
  <p><strong>What we thought.</strong> {insight['thought']}</p>
  <p><strong>What we learned.</strong> {insight['learned']}<sup class="fn">[{footnote_num}]</sup></p>
  <p><strong>What we changed.</strong> {insight['changed']}</p>
  <p class="stand">{insight['matters']}</p>
  <p><strong>What's still open.</strong> {insight['caveats']}</p>
  <div class="footnote"><span class="fn-num">[{footnote_num}]</span> {insight['source']}.</div>
</section>
"""

def v10a_html(title, body):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Connect by Dimagi</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=IBM+Plex+Mono&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>
{body}
</body>
</html>"""

def v10a_homepage():
    teaser_items = [
        ("/verify.html", TRAIL_TEASERS["verify_hero"], "Signature evidence — Verify"),
        ("/programs/chc.html", TRAIL_TEASERS["chc"], "Program — Child Health Campaign"),
        ("/programs/kmc.html", TRAIL_TEASERS["kmc"], "Program — Kangaroo Mother Care"),
        ("/programs/ecd.html", TRAIL_TEASERS["ecd"], "Program — Early Childhood Development"),
        ("/programs/readers.html", TRAIL_TEASERS["readers"], "Program — Readers"),
        ("/learn.html", TRAIL_TEASERS["learn"], "Platform — Learn"),
        ("/deliver.html", TRAIL_TEASERS["deliver"], "Platform — Deliver"),
        ("/verify.html", TRAIL_TEASERS["verify"], "Platform — Verify"),
        ("/pay.html", TRAIL_TEASERS["pay"], "Platform — Pay"),
        ("/insights.html", TRAIL_TEASERS["insights"], "All claims — Insights index"),
    ]
    trail = "\n".join(
        f'<li><a href="{href}">{teaser}<div class="sub">{sub}</div></a></li>'
        for href, teaser, sub in teaser_items
    )
    body = f"""
{render_v10a_nav('index.html')}
<main>
  <header class="memo">
    <div class="label">Foundation Memo · April 2026</div>
    <h1>A new model for global development — funding linked to verified service delivery at the frontline.</h1>
    <p class="lede">Connect by Dimagi is a platform for funding verified service delivery. We pay locally-led organizations against measured results — not enrolled workers, not installed apps. Below is what we've learned across 12 countries and 5,000+ frontline workers, scoped to the evidence behind each claim.</p>
    <div class="meta">
      <div><strong>Tagline.</strong> Powering the Frontline. Paying for Results.</div>
      <div><strong>Scale.</strong> 5,000+ FLWs · 12 countries · 1M+ verified services</div>
      <div><strong>Funding raised.</strong> $5.9M (vs $2M target)</div>
    </div>
  </header>

  <section class="entry" style="border-top:none;padding-top:0">
    <h2>What this site is</h2>
    <p>A working memo. Each link below is a verbatim claim that you will encounter, expanded, on the depth page it points to. We don't write generic CTAs because a funder reading this in 30 seconds gets nothing actionable from "Learn more."</p>
    <p>Numbers without benchmarks aren't included. Findings still under validation are named with the evaluation underway. Things that didn't work are published — sometimes prominently. The methodology footer on <a href="/insights.html">our /insights page</a> spells out what makes the cut.</p>
    <ul class="trail-list">
      {trail}
    </ul>
  </section>

  <section class="entry">
    <h2>Headline numbers</h2>
    <div class="metrics">
      <div class="m"><div class="num">880K+</div><div class="lab">Verified CHC visits, 14 months</div></div>
      <div class="m"><div class="num">5,000+</div><div class="lab">FLWs trained across 12 countries</div></div>
      <div class="m"><div class="num">44</div><div class="lab">LLOs activated under Founders Pledge grant</div></div>
      <div class="m"><div class="num">22%</div><div class="lab">Cost reduction in CHC as it scaled</div></div>
      <div class="m"><div class="num">94%</div><div class="lab">Population coverage with microplans (CHC)</div></div>
      <div class="m"><div class="num">0.91</div><div class="lab">Fraud-detection AUC under adversarial test</div></div>
    </div>
    <p style="margin-top:18px;font-size:0.95rem;color:var(--muted)">Sources: Founders Pledge Final Report (Feb 2026); ECD Overview (Feb 2026); CLP Stage 2 Report (Feb 2026); FLW Displacement Survey (Oct 2025); KMC Conceptual Model v1 (March 2026).</p>
  </section>
</main>
{render_v10a_footer()}
"""
    return v10a_html("Home — Foundation Memo", body)

def v10a_ldvp_page(step_key):
    step = LDVP[step_key]
    insights = [insight_by_id(i) for i in step["insight_ids"]]
    next_idx = LDVP_ORDER.index(step_key) + 1
    next_link = ""
    if next_idx < len(LDVP_ORDER):
        nxt = LDVP[LDVP_ORDER[next_idx]]
        next_link = f'<a class="transition-link" href="/{LDVP_ORDER[next_idx]}.html">Continue → {nxt["name"]}</a>'
    else:
        next_link = '<a class="transition-link" href="/programs.html">Continue → Programs</a>'
    sections = "".join(v10a_insight_section(ins, idx+1) for idx, ins in enumerate(insights))
    body = f"""
{render_v10a_nav(step_key + '.html')}
<main>
  <header class="memo">
    <div class="label">Platform · {step['name']}</div>
    <h1>{step['name']}: {step['tagline']}</h1>
    <p class="lede">{step['summary']}</p>
    <div class="meta">
      <div><strong>{step['headline_metric'][0]}</strong> {step['headline_metric'][1]}</div>
      <div><strong>Step {LDVP_ORDER.index(step_key)+1} of 4</strong> in the Connect lifecycle.</div>
    </div>
  </header>
  {sections}
  {open_questions_html(step_key)}
  <div class="cta-row">
    <span style="font-family:'IBM Plex Sans',sans-serif;font-size:0.86rem;color:var(--muted)">End of {step['name']} memo.</span>
    {next_link}
  </div>
</main>
{render_v10a_footer()}
"""
    return v10a_html(f"{step['name']} — Foundation Memo", body)

def v10a_program_page(prog_key):
    prog = PROGRAMS[prog_key]
    insights = [insight_by_id(i) for i in prog["insight_ids"]]
    metrics = "".join(f'<div class="m"><div class="num">{n}</div><div class="lab">{l}</div></div>' for n, l in prog["metrics"])
    sections = "".join(v10a_insight_section(ins, idx+1) for idx, ins in enumerate(insights))
    if not insights:
        sections = '<section class="entry"><h2>Status: pre-launch</h2><p>This program has been contracted but field-performance data does not yet exist. We will publish learnings as the first cohort closes.</p></section>'
    video_block = ""
    if prog["video"]:
        video_block = f'<a class="video-link" href="{prog["video"]}" target="_blank" rel="noopener">▶ Watch: {prog["video_title"]}</a>'
    body = f"""
{render_v10a_nav('programs')}
<main>
  <header class="memo">
    <div class="label">Program — {prog['name']}</div>
    <h1>{prog['name']}</h1>
    <p class="lede">{prog['tagline']}</p>
    <div class="meta">
      <div><strong>Regions.</strong> {prog['regions']}</div>
      <div><strong>Scale.</strong> {prog['scale']}</div>
      <div><strong>Funder(s).</strong> {prog['funders']}</div>
      <div><strong>Partners.</strong> {prog['partners']}</div>
    </div>
    {video_block}
  </header>

  <section class="entry" style="border-top:none;padding-top:0">
    <h2>The challenge</h2>
    <p>{prog['challenge']}</p>
  </section>

  <section class="entry">
    <h2>The approach</h2>
    <p>{prog['approach']}</p>
    <div class="metrics">{metrics}</div>
  </section>

  {sections}

  {open_questions_html(prog_key)}

  <div class="cta-row">
    <a href="/programs.html">← All programs</a>
    <a class="transition-link" href="/insights.html">View all claims, scoped → Insights</a>
  </div>
</main>
{render_v10a_footer()}
"""
    return v10a_html(f"{prog['name']} — Foundation Memo", body)

def v10a_programs_index():
    cards = []
    for key in ["chc", "kmc", "ecd", "readers"]:
        prog = PROGRAMS[key]
        cards.append(f'<li><a href="/programs/{key}.html">{TRAIL_TEASERS[key]}<div class="sub">{prog["name"]} · {prog["regions"]}</div></a></li>')
    coming = ["MBW", "Chlorine", "WellMe", "RUTF", "Interviews", "Rooftop Sampling"]
    coming_items = "".join(f'<li><span style="color:var(--muted);font-style:italic">{c} — coming 2026</span></li>' for c in coming)
    body = f"""
{render_v10a_nav('programs.html')}
<main>
  <header class="memo">
    <div class="label">Programs — All Active</div>
    <h1>The programs Connect powers, in their own evidence.</h1>
    <p class="lede">Each program below carries its own scoped claims. Click through for the full memo per program — or scan the <a href="/insights.html">/insights buffet</a> for every claim across all programs.</p>
  </header>
  <ul class="trail-list">{"".join(cards)}</ul>
  <section class="entry">
    <h2>Pre-launch / earlier scale</h2>
    <ul style="list-style:none">{coming_items}</ul>
  </section>
</main>
{render_v10a_footer()}
"""
    return v10a_html("Programs — Foundation Memo", body)

def v10a_insights_page():
    # Group nuggets by scope
    by_scope = {"CHC": [], "KMC": [], "ECD": [], "Readers": [], "Platform": []}
    for n in NUGGETS:
        by_scope.setdefault(n["scope"], []).append(n)
    # Add insights as entries too (using their title + matters as the buffet line)
    for ins in INSIGHTS:
        scope = ins["scope"]
        by_scope.setdefault(scope, []).append({
            "claim": f"{ins['title']} {ins['matters']}",
            "scope": ins["scope"],
            "evidence_tier": ins["evidence_tier"],
            "tier_label": ins["tier_label"],
            "open_question": ins["caveats"],
            "home": ins["homes"][0] if ins["homes"] else "insights",
            "is_insight": True,
            "judge_score": 7,
        })
    groups_html = []
    for scope_name in ["CHC", "ECD", "KMC", "Readers", "Platform"]:
        items = by_scope.get(scope_name, [])
        if not items: continue
        items_sorted = sorted(items, key=lambda x: -x.get("judge_score", 5))
        rows = []
        for it in items_sorted:
            home = it.get("home", "insights")
            home_href = f"/programs/{home}.html" if home in PROGRAMS else f"/{home}.html"
            tier_cls = f"tier-{slug_tier(it['evidence_tier'])}"
            rows.append(f"""
<li>
  <div class="claim">{it['claim']}</div>
  <div class="meta"><span class="scope-tag">Scope: {it['scope']}</span><span class="tier-tag {tier_cls}">{it['tier_label']}</span><a href="{home_href}">→ where it lives</a></div>
  <div class="open-q">Open: {it['open_question']}</div>
</li>""")
        groups_html.append(f'<div class="insights-group"><h2>{scope_name}</h2><ul class="insights-list">{"".join(rows)}</ul></div>')
    body = f"""
{render_v10a_nav('insights.html')}
<main>
  <header class="memo">
    <div class="label">Insights — Buffet view</div>
    <h1>What we've learned, every claim scoped to its evidence.</h1>
    <p class="lede">A foundation officer evaluating a $10M grant can spend 15 minutes here and leave knowing exactly what we believe is true, how confident we are about each claim, and what's still under validation. This is the entire intellectual surface of the site.</p>
  </header>

  {''.join(groups_html)}

  {open_questions_html('insights')}

  <div class="method-footer">
    <h3>How we decide what makes the cut</h3>
    <p>Each claim is scoped to its evidence. A program-specific finding (CHC's 22% cost reduction, ECD's +33% knowledge gain) stays scoped to the program. We never strip the program name to make a claim sound platform-wide.</p>
    <p>Numbers without benchmarks are not on this page. "94% coverage" only appears here paired with the comparator (82–84% non-Connect coverage in similar regions, measured against GRID3 gold-standard population estimates).</p>
    <p>Findings still under validation are named with the evaluation underway. Our 2026 IPA RCT ($1.5M, PRO Impact) is the cleanest counterfactual we'll have on CHC; until it closes, we say so.</p>
    <p>Things that didn't work — both contracted CAR LLOs dropped out; microplans failed in dispersed settlement patterns; encouragement-of-autonomy is at 47% endline — appear on this page because the alternative (silence) is what diligence readers learn to discount.</p>
  </div>
</main>
{render_v10a_footer()}
"""
    return v10a_html("Insights — Foundation Memo", body)

# ----- v10b (Field dispatch) -------------------------------------------------

def render_v10b_nav(current):
    return f"""
<nav class="dispatch">
  <div class="inner">
    <a class="brand" href="/index.html">CONNECT<span class="by">a dispatch from Dimagi</span></a>
    <ul>{page_meta_links('b', current)}</ul>
    <a class="demo" href="#contact">Get the dispatch</a>
  </div>
</nav>
"""

def render_v10b_footer():
    return """
<footer class="dispatch-footer">
  <div class="inner">
    <div class="signoff">Connect is what happens when you fund verified delivery instead of intentions, and let locally-led organizations bring the parts of the work no app can centralize.</div>
    <div class="meta">
      <div>Connect by Dimagi · April 2026</div>
      <div>5,000+ FLWs · 12 countries · 1M+ verified services</div>
      <div><a href="/insights.html">→ Read every claim, scoped</a></div>
    </div>
  </div>
</footer>
"""

def v10b_html(title, body):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Connect, a dispatch from Dimagi</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>
{body}
</body>
</html>"""

def v10b_insight_dispatch(insight):
    # Pattern D: progression of thinking — render as a timeline
    return f"""
<section class="dispatch-entry">
  <div class="kicker">Insight {insight['id'][1:]} · {insight['scope']} · evidence: {insight['tier_label']}</div>
  <h2>{insight['title']}</h2>
  <div class="timeline">
    <div class="timeline-step">
      <div class="when">First, we assumed —</div>
      <p>{insight['thought']}</p>
    </div>
    <div class="timeline-step">
      <div class="when">Then, the data —</div>
      <p>{insight['learned']}</p>
    </div>
    <div class="timeline-step">
      <div class="when">So we changed —</div>
      <p>{insight['changed']}</p>
    </div>
    <div class="timeline-step">
      <div class="when">What it means —</div>
      <p>{insight['matters']}</p>
    </div>
    <div class="timeline-step">
      <div class="when">What's still open —</div>
      <p>{insight['caveats']}</p>
    </div>
  </div>
  <p style="font-family:'Inter',sans-serif;font-size:0.78rem;color:var(--muted);margin-top:24px">Source: {insight['source']}</p>
</section>
"""

def v10b_program_dispatch(insight):
    # Pattern B: two-column (in dispatch we render the body, side-col has methodology)
    return f"""
<section class="dispatch-entry">
  <div class="kicker">Insight {insight['id'][1:]} · evidence: {insight['tier_label']}</div>
  <h2>{insight['title']}</h2>
  <p>{insight['thought']}</p>
  <p>{insight['learned']}</p>
  <p>{insight['changed']}</p>
  <div class="stand">{insight['matters']}</div>
  <p>{insight['caveats']}</p>
  <p style="font-family:'Inter',sans-serif;font-size:0.78rem;color:var(--muted)">Source: {insight['source']}</p>
</section>
"""

def v10b_homepage():
    teaser_items = [
        ("/verify.html", TRAIL_TEASERS["verify_hero"], "Dispatch · Verify"),
        ("/programs/chc.html", TRAIL_TEASERS["chc"], "Program · CHC"),
        ("/programs/kmc.html", TRAIL_TEASERS["kmc"], "Program · KMC"),
        ("/programs/ecd.html", TRAIL_TEASERS["ecd"], "Program · ECD"),
        ("/programs/readers.html", TRAIL_TEASERS["readers"], "Program · Readers"),
        ("/learn.html", TRAIL_TEASERS["learn"], "Platform · Learn"),
        ("/deliver.html", TRAIL_TEASERS["deliver"], "Platform · Deliver"),
        ("/verify.html", TRAIL_TEASERS["verify"], "Platform · Verify"),
        ("/pay.html", TRAIL_TEASERS["pay"], "Platform · Pay"),
        ("/insights.html", TRAIL_TEASERS["insights"], "All claims · Insights"),
    ]
    trail = "\n".join(
        f'<li><a href="{href}">{teaser}<div class="sub">{sub}</div></a></li>'
        for href, teaser, sub in teaser_items
    )
    body = f"""
{render_v10b_nav('index.html')}
<header class="hero">
  <div class="dateline">A Dispatch · April 2026 · From the Field</div>
  <h1>We pay for <em>verified delivery</em>, not intentions — and we publish what didn't work.</h1>
  <p class="lede">Connect by Dimagi is a platform for funding the frontline. Across 12 countries and 5,000+ workers, we've learned things you usually only see in private foundation reports. This is where they live in public.</p>
  <div class="byline"><div><strong>Tagline.</strong> Powering the Frontline. Paying for Results.</div><div><strong>Funding.</strong> $5.9M raised vs $2M target</div><div><strong>Direct FLW payments.</strong> $90,000+</div></div>
</header>
<main class="dispatch-body single">
  <div class="body-col">
    <section class="dispatch-entry" style="border-top:none;padding-top:0">
      <div class="kicker">From the editor</div>
      <h2>What you'll find inside this dispatch</h2>
      <p>Each link below is the verbatim claim you'll meet, expanded, on the page it points to. The home page is no place to bury substance behind a "Learn more" button. We chose the link text after a foundation officer told us — politely — that "Explore" tells them nothing.</p>
      <div class="metrics-strip">
        <div class="m"><div class="num">880K+</div><div class="lab">Verified CHC visits, 14 months</div></div>
        <div class="m"><div class="num">5,000+</div><div class="lab">FLWs trained, 12 countries</div></div>
        <div class="m"><div class="num">22%</div><div class="lab">CHC cost reduction as scaled</div></div>
        <div class="m"><div class="num">0.91</div><div class="lab">Fraud detection AUC, adversarial test</div></div>
      </div>
      <ul class="trail-list">{trail}</ul>
    </section>
  </div>
</main>
{render_v10b_footer()}
"""
    return v10b_html("Dispatch — Home", body)

def v10b_ldvp_page(step_key):
    step = LDVP[step_key]
    insights = [insight_by_id(i) for i in step["insight_ids"]]
    sections = "".join(v10b_insight_dispatch(ins) for ins in insights)
    pullquote = insights[0]["title"] if insights else step["tagline"]
    next_idx = LDVP_ORDER.index(step_key) + 1
    next_link = ""
    if next_idx < len(LDVP_ORDER):
        nxt = LDVP[LDVP_ORDER[next_idx]]
        next_link = f'<a class="video-link" href="/{LDVP_ORDER[next_idx]}.html">Next dispatch → {nxt["name"]}</a>'
    else:
        next_link = '<a class="video-link" href="/programs.html">Next → The programs</a>'
    body = f"""
{render_v10b_nav(step_key + '.html')}
<header class="hero">
  <div class="dateline">Platform Dispatch · {step['name']} · Step {LDVP_ORDER.index(step_key)+1} of 4</div>
  <h1>{step['name']}: <em>{step['tagline']}</em></h1>
  <p class="lede">{step['summary']}</p>
  <div class="byline"><div><strong>{step['headline_metric'][0]}</strong> {step['headline_metric'][1]}</div></div>
</header>
<main class="dispatch-body">
  <div class="body-col">
    {sections}
    {open_questions_html(step_key)}
    <div style="margin-top:32px">{next_link}</div>
  </div>
  <aside class="side-col">
    <div class="sticky">
      <div class="pullquote">"{pullquote}"</div>
      <div class="meta-block"><div class="lab">Step</div><div class="val">{LDVP_ORDER.index(step_key)+1} of 4 in the Connect lifecycle</div></div>
      <div class="meta-block"><div class="lab">Headline</div><div class="val">{step['headline_metric'][0]} — {step['headline_metric'][1]}</div></div>
      <div class="meta-block"><div class="lab">Insights on this page</div><div class="val">{len(insights)}, each ~250–600 words, with the team's evolving thinking traced step by step.</div></div>
      <div class="meta-block"><div class="lab">Pattern</div><div class="val">Pattern D — Progression of Thinking. We show the timeline of how we figured this out, including what we got wrong first.</div></div>
    </div>
  </aside>
</main>
{render_v10b_footer()}
"""
    return v10b_html(f"Dispatch — {step['name']}", body)

def v10b_program_page(prog_key):
    prog = PROGRAMS[prog_key]
    insights = [insight_by_id(i) for i in prog["insight_ids"]]
    sections = "".join(v10b_program_dispatch(ins) for ins in insights)
    if not insights:
        sections = '<section class="dispatch-entry"><h2>Status: pre-launch</h2><p>This program has been contracted but field-performance data does not yet exist. We will publish learnings as the first cohort closes.</p></section>'
    pullquote = insights[0]["title"] if insights else prog["tagline"]
    metrics = "".join(f'<div class="m"><div class="num">{n}</div><div class="lab">{l}</div></div>' for n, l in prog["metrics"])
    video_block = ""
    if prog["video"]:
        video_block = f'<a class="video-link" href="{prog["video"]}" target="_blank" rel="noopener">▶ {prog["video_title"]}</a>'
    body = f"""
{render_v10b_nav('programs')}
<header class="hero">
  <div class="dateline">Program Dispatch · {prog['name']}</div>
  <h1>{prog['name']}: <em>{prog['tagline']}</em></h1>
  <p class="lede">{prog['challenge']}</p>
  <div class="byline">
    <div><strong>Regions.</strong> {prog['regions']}</div>
    <div><strong>Scale.</strong> {prog['scale']}</div>
    <div><strong>Funder(s).</strong> {prog['funders']}</div>
  </div>
  {video_block}
</header>
<main class="dispatch-body">
  <div class="body-col">
    <section class="dispatch-entry" style="border-top:none;padding-top:0">
      <div class="kicker">The approach</div>
      <h2>How this program works on the ground</h2>
      <p>{prog['approach']}</p>
      <div class="metrics-strip">{metrics}</div>
    </section>
    {sections}
    {open_questions_html(prog_key)}
    <div style="margin-top:32px"><a class="video-link" href="/programs.html">← All programs</a></div>
  </div>
  <aside class="side-col">
    <div class="sticky">
      <div class="pullquote">"{pullquote}"</div>
      <div class="meta-block"><div class="lab">Partners</div><div class="val">{prog['partners']}</div></div>
      <div class="meta-block"><div class="lab">Pattern</div><div class="val">Pattern B — Two-column long-form. The body reads like a New Yorker dispatch; the right rail carries methodology, partners, and the open questions.</div></div>
      <div class="meta-block"><div class="lab">Insights on this page</div><div class="val">{len(insights)}, scoped to {prog['name']}.</div></div>
    </div>
  </aside>
</main>
{render_v10b_footer()}
"""
    return v10b_html(f"Dispatch — {prog['name']}", body)

def v10b_programs_index():
    cards = []
    for key in ["chc", "kmc", "ecd", "readers"]:
        prog = PROGRAMS[key]
        cards.append(f'<li><a href="/programs/{key}.html">{TRAIL_TEASERS[key]}<div class="sub">{prog["name"]} · {prog["regions"]}</div></a></li>')
    coming = ["MBW", "Chlorine", "WellMe", "RUTF", "Interviews", "Rooftop Sampling"]
    coming_items = "".join(f'<li style="border-bottom:1px dotted var(--rule);padding:14px 0;font-style:italic;color:var(--muted)">{c} — coming 2026</li>' for c in coming)
    body = f"""
{render_v10b_nav('programs.html')}
<header class="hero">
  <div class="dateline">Programs · All Active</div>
  <h1>Each program is its own dispatch.</h1>
  <p class="lede">CHC, KMC, ECD, and Readers each carry their own scoped claims. Click for the full feature, or skim the <a href="/insights.html">/insights buffet</a> for everything in one place.</p>
</header>
<main class="dispatch-body single">
  <div class="body-col">
    <ul class="trail-list">{"".join(cards)}</ul>
    <h2 style="font-family:'Source Serif Pro',serif;font-weight:400;margin-top:48px;margin-bottom:18px">Pre-launch</h2>
    <ul style="list-style:none">{coming_items}</ul>
  </div>
</main>
{render_v10b_footer()}
"""
    return v10b_html("Dispatch — Programs", body)

def v10b_insights_page():
    by_scope = {"CHC": [], "KMC": [], "ECD": [], "Readers": [], "Platform": []}
    for n in NUGGETS: by_scope.setdefault(n["scope"], []).append(n)
    for ins in INSIGHTS:
        by_scope.setdefault(ins["scope"], []).append({
            "claim": f"{ins['title']} {ins['matters']}",
            "scope": ins["scope"],
            "evidence_tier": ins["evidence_tier"],
            "tier_label": ins["tier_label"],
            "open_question": ins["caveats"],
            "home": ins["homes"][0] if ins["homes"] else "insights",
            "judge_score": 7,
        })
    groups = []
    for s in ["CHC", "ECD", "KMC", "Readers", "Platform"]:
        items = by_scope.get(s, [])
        if not items: continue
        items_sorted = sorted(items, key=lambda x: -x.get("judge_score", 5))
        rows = []
        for it in items_sorted:
            home = it.get("home", "insights")
            home_href = f"/programs/{home}.html" if home in PROGRAMS else f"/{home}.html"
            rows.append(f"""
<li>
  <div class="claim">{it['claim']}</div>
  <div class="meta"><span>Scope · {it['scope']}</span><span>Evidence · {it['tier_label']}</span><a href="{home_href}">→ where it lives</a></div>
  <div class="open-q">Open: {it['open_question']}</div>
</li>""")
        groups.append(f'<div class="insights-group"><h2>{s}</h2><ul class="insights-list">{"".join(rows)}</ul></div>')
    body = f"""
{render_v10b_nav('insights.html')}
<header class="hero">
  <div class="dateline">Insights · The Buffet View</div>
  <h1>Every claim, <em>scoped to its evidence.</em></h1>
  <p class="lede">A foundation officer evaluating a $10M grant can spend 15 minutes here and leave knowing exactly what we believe is true and how confident we are about each claim. This is the entire intellectual surface of the site.</p>
</header>
<main class="dispatch-body single">
  <div class="body-col">
    {''.join(groups)}
    {open_questions_html('insights')}
    <div class="method-footer">
      <h3>How we decide what makes the cut</h3>
      <p>Each claim is scoped to its evidence. A program-specific finding (CHC's 22% cost reduction, ECD's +33% knowledge gain) stays scoped to the program. We never strip the program name to make a claim sound platform-wide.</p>
      <p>Numbers without benchmarks are not on this page. "94% coverage" only appears here paired with the comparator (82–84% non-Connect coverage in similar regions).</p>
      <p>Findings still under validation are named with the evaluation underway. Things that didn't work — both contracted CAR LLOs dropping out; microplans failing in dispersed settlements — appear because the alternative is what diligence readers learn to discount.</p>
    </div>
  </div>
</main>
{render_v10b_footer()}
"""
    return v10b_html("Dispatch — Insights", body)

# ----- v10c (Knowledge graph) ------------------------------------------------

def render_v10c_nav(current):
    return f"""
<nav class="graph">
  <div class="inner">
    <a class="brand" href="/index.html">connect/dimagi</a>
    <ul>{page_meta_links('c', current)}</ul>
    <a class="demo" href="#contact">Request access</a>
  </div>
</nav>
"""

def render_v10c_footer():
    return """
<footer class="graph-footer">
  <div class="inner">
    <div>connect/dimagi · 5,000+ FLWs · 12 countries · 1M+ verified services · $5.9M raised</div>
    <div><a href="/insights.html">/insights →</a> &nbsp; <a href="#contact">contact →</a></div>
  </div>
</footer>
"""

def v10c_html(title, body):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · connect/dimagi</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Newsreader:ital,wght@0,400;1,400;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>
{body}
</body>
</html>"""

def v10c_insight_node(insight, anchor=True):
    tier = slug_tier(insight["evidence_tier"])
    anchor_attr = f' id="{insight["id"]}"' if anchor else ""
    return f"""
<section class="entry"{anchor_attr}>
  <div class="header-row">
    <span class="id-tag">{insight['id']}</span>
    <span class="scope-badge">scope: {insight['scope']}</span>
    <span class="tier-badge {tier}">{insight['tier_label']}</span>
  </div>
  <h2>{insight['title']}</h2>
  <div class="struct"><h3>The question we had</h3><p>{insight['thought']}</p></div>
  <div class="struct"><h3>What we tried &amp; what we found</h3><p>{insight['learned']}</p></div>
  <div class="struct"><h3>What changed</h3><p>{insight['changed']}</p></div>
  <div class="struct"><h3>Why it matters</h3><p>{insight['matters']}</p></div>
  <div class="struct"><h3>What's still open</h3><p>{insight['caveats']}</p></div>
  <div class="source">source: {insight['source']}</div>
</section>
"""

def v10c_program_node(insight):
    # Pattern E: question-led — frame insight as a question with structured answer
    question = f"How did we handle this — {insight['title'][:-1] if insight['title'].endswith('.') else insight['title']}?"
    tier = slug_tier(insight["evidence_tier"])
    return f"""
<section class="entry" id="{insight['id']}">
  <div class="header-row">
    <span class="id-tag">{insight['id']}</span>
    <span class="scope-badge">scope: {insight['scope']}</span>
    <span class="tier-badge {tier}">{insight['tier_label']}</span>
  </div>
  <div class="question">"{question}"</div>
  <div class="struct"><h3>What we assumed</h3><p>{insight['thought']}</p></div>
  <div class="struct"><h3>What the data showed</h3><p>{insight['learned']}</p></div>
  <div class="struct"><h3>What we did about it</h3><p>{insight['changed']}</p></div>
  <div class="struct"><h3>What it implies</h3><p>{insight['matters']}</p></div>
  <div class="struct"><h3>What we don't know</h3><p>{insight['caveats']}</p></div>
  <div class="source">source: {insight['source']}</div>
</section>
"""

def v10c_homepage():
    teaser_items = [
        ("/verify.html", TRAIL_TEASERS["verify_hero"], "Platform / Verify", "hard"),
        ("/programs/chc.html", TRAIL_TEASERS["chc"], "Program / CHC", "hard"),
        ("/programs/kmc.html", TRAIL_TEASERS["kmc"], "Program / KMC", "hard"),
        ("/programs/ecd.html", TRAIL_TEASERS["ecd"], "Program / ECD", "hard"),
        ("/programs/readers.html", TRAIL_TEASERS["readers"], "Program / Readers", "lived"),
        ("/learn.html", TRAIL_TEASERS["learn"], "Platform / Learn", "hard"),
        ("/deliver.html", TRAIL_TEASERS["deliver"], "Platform / Deliver", "hard"),
        ("/verify.html", TRAIL_TEASERS["verify"], "Platform / Verify", "hard"),
        ("/pay.html", TRAIL_TEASERS["pay"], "Platform / Pay", "hard"),
        ("/insights.html", TRAIL_TEASERS["insights"], "Index / Insights", "hard"),
    ]
    trail = "\n".join(
        f'<li><a href="{href}"><div class="claim">{teaser}</div><div class="badges"><span class="scope-badge">{sub}</span><span class="tier-badge {tier}">{tier}</span></div></a></li>'
        for href, teaser, sub, tier in teaser_items
    )
    body = f"""
{render_v10c_nav('index.html')}
<header class="hero">
  <div class="breadcrumb">/ home</div>
  <h1>A knowledge graph for verified service delivery — <span class="accent">every claim, every source, every open question, scoped.</span></h1>
  <p class="lede">Connect by Dimagi pays locally-led organizations against measured results. This site is not a brochure. It's the public face of our learning graph: 10 insights, 19 nuggets, 4 programs, with evidence tier and open question on every node.</p>
  <div class="meta"><span>build · v10c</span><span>nodes · {len(INSIGHTS)} insights + {len(NUGGETS)} nuggets</span><span>scopes · 4 programs + platform</span><span>countries · 12</span></div>
</header>
<main class="graph-body">
  <div class="metrics-grid">
    <div class="m"><div class="num">880K+</div><div class="lab">Verified CHC visits in 14 months</div></div>
    <div class="m"><div class="num">5,000+</div><div class="lab">FLWs across 12 countries</div></div>
    <div class="m"><div class="num">22%</div><div class="lab">CHC cost reduction as it scaled</div></div>
    <div class="m"><div class="num">AUC 0.91</div><div class="lab">Fraud detection under adversarial test</div></div>
    <div class="m"><div class="num">94%</div><div class="lab">Population coverage with microplans (CHC)</div></div>
    <div class="m"><div class="num">$5.9M</div><div class="lab">Raised vs $2M target</div></div>
  </div>

  <h2 style="font-family:'JetBrains Mono',monospace;font-size:0.92rem;color:var(--accent);text-transform:uppercase;letter-spacing:0.16em;margin:48px 0 16px">trail teasers · click any node to enter the graph</h2>
  <ul class="trail-list">{trail}</ul>

  <div class="method-footer">
    <h3>about the graph</h3>
    <p>Every link above is a verbatim claim, scoped to its evidence. Click through — the depth page expands the claim with the exact study, sample size, comparator, and the open question we still have. Numbers without benchmarks aren't included; findings under validation are named with the evaluation underway.</p>
    <p>The /insights page is the buffet view of every node. Use it to understand our epistemic posture before drilling into any program.</p>
  </div>
</main>
{render_v10c_footer()}
"""
    return v10c_html("Home", body)

def v10c_ldvp_page(step_key):
    step = LDVP[step_key]
    insights = [insight_by_id(i) for i in step["insight_ids"]]
    sections = "".join(v10c_insight_node(ins) for ins in insights)
    next_idx = LDVP_ORDER.index(step_key) + 1
    next_link = ""
    if next_idx < len(LDVP_ORDER):
        nxt = LDVP[LDVP_ORDER[next_idx]]
        next_link = f'<a class="transition-link" href="/{LDVP_ORDER[next_idx]}.html">next node → {nxt["name"]}</a>'
    else:
        next_link = '<a class="transition-link" href="/programs.html">next → programs</a>'
    body = f"""
{render_v10c_nav(step_key + '.html')}
<header class="hero">
  <div class="breadcrumb"><a href="/index.html">/ home</a> &nbsp;/&nbsp; platform &nbsp;/&nbsp; {step_key}</div>
  <h1>{step['name']} <span class="accent">— {step['tagline']}</span></h1>
  <p class="lede">{step['summary']}</p>
  <div class="meta"><span>step · {LDVP_ORDER.index(step_key)+1} of 4</span><span>headline · {step['headline_metric'][0]} {step['headline_metric'][1]}</span><span>insights · {len(insights)}</span><span>pattern · A engineering retrospective</span></div>
</header>
<main class="graph-body">
  {sections}
  {open_questions_html(step_key)}
  <div style="margin-top:32px">{next_link}</div>
</main>
{render_v10c_footer()}
"""
    return v10c_html(step["name"], body)

def v10c_program_page(prog_key):
    prog = PROGRAMS[prog_key]
    insights = [insight_by_id(i) for i in prog["insight_ids"]]
    sections = "".join(v10c_program_node(ins) for ins in insights)
    if not insights:
        sections = '<section class="entry"><div class="header-row"><span class="scope-badge">status: pre-launch</span></div><h2>Field-performance data does not yet exist</h2><div class="struct"><p>This program has been contracted but the first cohort has not yet run. We will add nodes to the graph as learnings close.</p></div></section>'
    metrics = "".join(f'<div class="m"><div class="num">{n}</div><div class="lab">{l}</div></div>' for n, l in prog["metrics"])
    video_block = ""
    if prog["video"]:
        video_block = f'<a class="video-link" href="{prog["video"]}" target="_blank" rel="noopener">▶ {prog["video_title"]}</a>'
    body = f"""
{render_v10c_nav('programs')}
<header class="hero">
  <div class="breadcrumb"><a href="/index.html">/ home</a> &nbsp;/&nbsp; <a href="/programs.html">programs</a> &nbsp;/&nbsp; {prog_key}</div>
  <h1>{prog['name']} <span class="accent">— {prog['tagline']}</span></h1>
  <p class="lede">{prog['challenge']}</p>
  <div class="meta"><span>regions · {prog['regions']}</span><span>scale · {prog['scale']}</span><span>funder · {prog['funders']}</span><span>insights · {len(insights)}</span></div>
  {video_block}
</header>
<main class="graph-body">
  <section class="entry">
    <div class="header-row"><span class="scope-badge">approach</span></div>
    <h2>How this program works on the ground</h2>
    <div class="struct"><p>{prog['approach']}</p></div>
    <div class="metrics-grid">{metrics}</div>
  </section>
  {sections}
  {open_questions_html(prog_key)}
  <div style="margin-top:32px"><a class="transition-link" href="/programs.html">← all programs</a> &nbsp; <a class="transition-link" href="/insights.html">all insights →</a></div>
</main>
{render_v10c_footer()}
"""
    return v10c_html(prog["name"], body)

def v10c_programs_index():
    cards = []
    for key in ["chc", "kmc", "ecd", "readers"]:
        prog = PROGRAMS[key]
        cards.append(f'<li><a href="/programs/{key}.html"><div class="claim">{TRAIL_TEASERS[key]}</div><div class="badges"><span class="scope-badge">program · {prog["name"]}</span><span class="scope-badge">{prog["regions"][:30]}{"…" if len(prog["regions"])>30 else ""}</span></div></a></li>')
    coming = ["MBW", "Chlorine", "WellMe", "RUTF", "Interviews", "Rooftop Sampling"]
    coming_items = "".join(f'<li style="background:var(--bg-2);padding:14px 22px;border-radius:5px;border:1px dashed var(--rule);color:var(--muted);font-style:italic">{c} — coming 2026</li>' for c in coming)
    body = f"""
{render_v10c_nav('programs.html')}
<header class="hero">
  <div class="breadcrumb"><a href="/index.html">/ home</a> &nbsp;/&nbsp; programs</div>
  <h1>Programs <span class="accent">— each is a sub-graph of the platform.</span></h1>
  <p class="lede">CHC, KMC, ECD, and Readers each carry their own scoped nodes. Or skim the <a href="/insights.html">/insights buffet</a> to see every node across all programs in one place.</p>
</header>
<main class="graph-body">
  <ul class="trail-list">{"".join(cards)}</ul>
  <h2 style="font-family:'JetBrains Mono',monospace;font-size:0.88rem;color:var(--muted);text-transform:uppercase;letter-spacing:0.16em;margin:48px 0 16px">pre-launch</h2>
  <ul class="trail-list" style="display:grid;gap:8px;list-style:none">{coming_items}</ul>
</main>
{render_v10c_footer()}
"""
    return v10c_html("Programs", body)

def v10c_insights_page():
    by_scope = {"CHC": [], "KMC": [], "ECD": [], "Readers": [], "Platform": []}
    for n in NUGGETS: by_scope.setdefault(n["scope"], []).append(n)
    for ins in INSIGHTS:
        by_scope.setdefault(ins["scope"], []).append({
            "claim": f"{ins['title']} {ins['matters']}",
            "scope": ins["scope"],
            "evidence_tier": ins["evidence_tier"],
            "tier_label": ins["tier_label"],
            "open_question": ins["caveats"],
            "home": ins["homes"][0] if ins["homes"] else "insights",
            "judge_score": 7,
        })
    groups = []
    for s in ["CHC", "ECD", "KMC", "Readers", "Platform"]:
        items = by_scope.get(s, [])
        if not items: continue
        items_sorted = sorted(items, key=lambda x: -x.get("judge_score", 5))
        rows = []
        for it in items_sorted:
            home = it.get("home", "insights")
            home_href = f"/programs/{home}.html" if home in PROGRAMS else f"/{home}.html"
            tier = slug_tier(it["evidence_tier"])
            rows.append(f"""
<li>
  <div class="badges"><span class="scope-badge">{it['scope']}</span><span class="tier-badge {tier}">{it['tier_label']}</span><a href="{home_href}" class="mono" style="font-size:0.74rem;color:var(--muted)">→ where it lives</a></div>
  <div class="claim">{it['claim']}</div>
  <div class="open-q">open: {it['open_question']}</div>
</li>""")
        groups.append(f'<div class="insights-group"><h2>{s} · {len(items_sorted)} nodes</h2><ul class="insights-list">{"".join(rows)}</ul></div>')
    body = f"""
{render_v10c_nav('insights.html')}
<header class="hero">
  <div class="breadcrumb"><a href="/index.html">/ home</a> &nbsp;/&nbsp; insights</div>
  <h1>The full graph <span class="accent">— every node, every evidence tier, every open question.</span></h1>
  <p class="lede">A foundation officer evaluating a $10M grant can spend 15 minutes here and leave knowing exactly what we believe is true and how confident we are about each claim.</p>
  <div class="meta"><span>nodes · {sum(len(v) for v in by_scope.values())}</span><span>scopes · 5</span><span>tiers · hard / triangulated / lived / hypothesis</span></div>
</header>
<main class="graph-body">
  {''.join(groups)}
  {open_questions_html('insights')}
  <div class="method-footer">
    <h3>methodology · what makes it onto the graph</h3>
    <p>Each claim is scoped to its evidence. A program-specific finding stays scoped — we never strip the program name to make a claim sound platform-wide. Numbers without benchmarks are not on this page. Findings still under validation are named with the evaluation underway (e.g., IPA RCT 2026, $1.5M, PRO Impact, on CHC).</p>
    <p>Things that didn't work — both contracted CAR LLOs dropped out; microplans failed in dispersed settlement; encouragement-of-autonomy is at 47% endline — appear because the alternative (silence) is what diligence readers learn to discount.</p>
  </div>
</main>
{render_v10c_footer()}
"""
    return v10c_html("Insights — the graph", body)

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def write_variant(variant_dir, css, pages):
    variant_dir.mkdir(parents=True, exist_ok=True)
    (variant_dir / "programs").mkdir(exist_ok=True)
    (variant_dir / "styles.css").write_text(css)
    for path, content in pages.items():
        full = variant_dir / path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content)
    print(f"  wrote {len(pages)+1} files to {variant_dir}")

def build_v10a():
    print("Building v10a (Foundation memo)...")
    pages = {
        "index.html": v10a_homepage(),
        "learn.html": v10a_ldvp_page("learn"),
        "deliver.html": v10a_ldvp_page("deliver"),
        "verify.html": v10a_ldvp_page("verify"),
        "pay.html": v10a_ldvp_page("pay"),
        "programs.html": v10a_programs_index(),
        "insights.html": v10a_insights_page(),
        "programs/chc.html": v10a_program_page("chc"),
        "programs/kmc.html": v10a_program_page("kmc"),
        "programs/ecd.html": v10a_program_page("ecd"),
        "programs/readers.html": v10a_program_page("readers"),
    }
    write_variant(OUT_BASE / "v10a", V10A_CSS, pages)

def build_v10b():
    print("Building v10b (Field dispatch)...")
    pages = {
        "index.html": v10b_homepage(),
        "learn.html": v10b_ldvp_page("learn"),
        "deliver.html": v10b_ldvp_page("deliver"),
        "verify.html": v10b_ldvp_page("verify"),
        "pay.html": v10b_ldvp_page("pay"),
        "programs.html": v10b_programs_index(),
        "insights.html": v10b_insights_page(),
        "programs/chc.html": v10b_program_page("chc"),
        "programs/kmc.html": v10b_program_page("kmc"),
        "programs/ecd.html": v10b_program_page("ecd"),
        "programs/readers.html": v10b_program_page("readers"),
    }
    write_variant(OUT_BASE / "v10b", V10B_CSS, pages)

def build_v10c():
    print("Building v10c (Knowledge graph)...")
    pages = {
        "index.html": v10c_homepage(),
        "learn.html": v10c_ldvp_page("learn"),
        "deliver.html": v10c_ldvp_page("deliver"),
        "verify.html": v10c_ldvp_page("verify"),
        "pay.html": v10c_ldvp_page("pay"),
        "programs.html": v10c_programs_index(),
        "insights.html": v10c_insights_page(),
        "programs/chc.html": v10c_program_page("chc"),
        "programs/kmc.html": v10c_program_page("kmc"),
        "programs/ecd.html": v10c_program_page("ecd"),
        "programs/readers.html": v10c_program_page("readers"),
    }
    write_variant(OUT_BASE / "v10c", V10C_CSS, pages)

if __name__ == "__main__":
    build_v10a()
    build_v10b()
    build_v10c()
    print("Done.")
