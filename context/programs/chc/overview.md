# Connect CHC — Child Health Campaign

Sources: Confluence "Connect - Child Health Campaign (CHC) (2025)", Founders Pledge Final Report (Feb 2026)

## Program Basics
- **Regions:** Nigeria, DRC, CAR, Kenya, Uganda, Tanzania, Zambia, Sierra Leone (8+ countries)
- **Sector:** Child Health & Nutrition
- **Scale:** 1,016,000+ visits in 2025; 880,000+ verified visits in 14 months (Founders Pledge campaign)
- **Funders:** GiveWell, Founders Pledge, Gavi (multi-funder)
- **Partners:** 28+ active LLOs (11 in Nigeria; 16+ others); 44 contracted total via Founders Pledge grant

## What It Delivers
Door-to-door child health campaigns delivering:
- **Vitamin A supplementation** (VAS)
- **Deworming**
- **Oral rehydration salts (ORS)** for dehydration treatment
- **Malnutrition screening** (MUAC measurements)
- **Immunization / vaccine promotion**

Target: vulnerable children ages 0-59 months.

## Key Innovation: Microplanning
Before each campaign, Dimagi overlays a grid onto the target area using open-source satellite data (Google Open Buildings, OpenStreetMap, Microsoft). Grid cells with buildings become **Delivery Units (DUs)**. DUs group into **Service Areas** sized for 1-2 weeks of work per FLW. Workers must close all DUs in their current Service Area before unlocking the next one.

**This pushes workers into areas they'd otherwise skip.**

## Coverage Results (from Founders Pledge report)
| Campaign Type | % populated cells visited | % population in visited cells | % cells to cover 95% of pop |
|---------------|--------------------------|-------------------------------|-----------------------------|
| CHC with microplans | **65%** | **94%** | **91%** |
| CHC without microplans (experienced LLO) | 55% | 84% | 72% |
| Well-run CommCare campaign (non-Connect) | 53% | 82% | 66% |

**Thoroughness:** In microplan-supported campaigns, workers averaged 1.4 visits per estimated child across visited cells, vs only 0.4 in Trial Run campaigns without geographic saturation requirements.

## Key Innovation: AI-Powered Supervision (Kenya pilot)
- AI chatbot on Dimagi's Open Chat Studio platform, accessed via WhatsApp
- Handled **500 of 511 queries (97.8%) without human escalation**
- Average response time: 5 seconds
- Independent evaluation: 88.7% accuracy, 81.5% usefulness

## Cost Reduction (Founders Pledge grant)
- Started at $2.20 per verified visit, dropped to **$1.70 per verified visit — 22% reduction**
- In Nigeria (including ORS/Zinc co-packs): avg $1.30 per visit across 14 LLO contracts
- Outside Nigeria (Vit A + deworming, no ORS): avg $0.78 per visit across 17 contracts
- Setup fees: avg $0.40/visit during grant, expected to fall to ~$0.10/visit at scale

## LLO Activation Model (Founders Pledge learnings)
- **Simple EOI process** — brief scope doc + Google Form + Dimagi network circulation
- Single EOI for CHC yielded ~100 applications
- **Trial Run model** — new LLOs get small initial contract ($3K setup for 3K visits); evaluated on actual delivery
- Of 37 contracted LLOs: 24 entered Trial Runs; 10 underperformed (not continued); 3 went straight to larger campaigns
- 17 organizations completed campaigns following successful trials

## Fraud Detection (Adversarial Testing)
Paid experienced FLWs to submit 100 fake visit records each across 3 rounds. Using only 3 data elements (age, gender, MUAC), a Random Forest model achieved **AUC of 0.91 ± 0.09** — excellent discrimination between real and fabricated data. Only 2.5% of real workers received higher fraud risk scores than even the lowest-scoring fabricator.

**Conclusion:** Large-scale data fabrication is statistically detectable even without GPS or photo verification, which Connect also applies to every visit.

## RCT
Dimagi is conducting an RCT for CHC in 2026 with IPA as evaluation partner (funded by PRO Impact, $1.5M).

## Public Resources
- **Video: Inside the Child Health Campaign in Kenya** — https://www.youtube.com/watch?v=VRbvUj9LTUg
- **Video: CommCare Connect Demo** — https://www.youtube.com/watch?v=oiUuT5v6ir0
