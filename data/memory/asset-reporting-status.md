---
name: asset-reporting-status
description: "Asset Reporting -- Shannon creating a Confluence page for early asset reports (Sep 22); first biweekly session with Stephen Leong's group Sep 23 (outcome not yet captured); Talia drafting prompts for remaining priority assets via Northern Lights beta deep research. Updated Sep 23, 2026."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4b881dac-e446-4b63-b338-c9ba1f6228ea
  modified: 2026-09-23T18:43:54.548Z
---

## Current State (Sep 23, 2026)

- **Shannon is creating a Confluence page for early asset reports** (Teams, Sep 22), alongside the pages already set up for MRL Debrief and the ESMO / AHA workflow experiments.
- **First every-other-week session with Stephen Leong's group was scheduled for today (Sep 23).** Outcome not yet captured; add it once known.
- JPA's open ask from Sep 10 (Talia): review the SAC-TMT prompt and draft foundational prompts for the remaining priority assets, run them through the Northern Lights beta deep research module, and share results ahead of that session.

## Action Items (Sep 23)

- **Shannon: Create Confluence page for early asset reports** -- per Shannon's Sep 22 Teams note
- **Talia: Draft foundational prompts for remaining priority assets** -- review the SAC-TMT prompt, test through the Northern Lights beta module, share ahead of the Stephen Leong session
- **Team: Capture outcomes of the first biweekly Stephen Leong session (Sep 23)**
- **JPA: Demo the asset normalization app to Stephen, Danny, and EPAM** -- not yet scheduled
- **JPA: Remaining demo-app updates** -- MUSE pairing integration, NCT registry bucket, additional competitor data

## Current State (Sep 10, 2026)

**Shannon has taken direct ownership of coordinating this** (weekly check-in) -- set up a recurring **every-other-week meeting with Stephen Leong's group**, first session **Wed Sep 23** (Talia copied). Shannon has access to the Northern Lights beta deep research module and set up a shared folder with the SAC-TMT baseline example.

**Ask of JPA (Talia):** Review the SAC-TMT prompt and help draft foundational prompts for the remaining 4-5 priority assets, run test outputs through the Northern Lights beta module, and share results **in advance of the Sep 23 meeting** so stakeholders can react/validate before the live session.

**Shannon's framing to the stakeholder group:** explicitly experimental, not yet part of the Congress AI tool. Notably, she's declined to do the final polish/report-writing herself this time (a role she'd fallen into with this group ~1.5 years ago) -- pushing ownership of prompt-writing back onto the asset leads.

## Current State (Sep 1, 2026)

**Demo app complete and delivered.** Streamlit app on port 8502 with 9 sections demonstrating two-layer asset normalization. JPA-branded pitch deck delivered (23-slide July update).

**Seed data:** 6 molecules (4 Merck + 2 competitors), 8 indications, 2 TAs, 4 products, 11 studies. All four F2F/Jul 2 updates implemented (studies bucket, competitor-first labeling, always-on ingestion, MUSE pairing).

## Sac-TMT Deep Research (Jun-Aug 2026 email chain)

Shannon shared Northern Lights deep research reports on sac-TMT with Susan Shetzline, Stephen Leong, Josefine Roemmler-Zehrer, and Danny Hsu in mid-June. **Susan's LT (Melissa & Miguel) liked Report 1** and gave concrete ESMO requirements:

**Requirements from Susan's LT:**
- Post-congress report available within **48 hours** of congress
- Medical perspective limited to **Tier 1 abstracts** with First Impressions captured by field teams
- Medical perspective **highlighted upfront** in the report (not embedded)
- Include **AI-platform summaries/sentiment** on Tier 1 abstracts

**Action items from LT feedback:**
1. Leverage First Impressions for presentation summaries and integrate into post-congress summary
2. Build capability of capturing AI-platform summaries/sentiment on Tier 1 abstracts
3. Evolve report to make Medical perspective more prominent
4. **Expand to 8 priority assets:** SubQ, pembro (KN-689, KN-B15, KN-905), sac-TMT (TF-005), Belzutifan (LS-011, LS-012, LS-022), Precision Medicine, V-940 (melanoma), Opeve (prostate cancer)

**Stephen Leong's aspirational wish list (Jun 25):**
- All abstracts/posters/presentations downloaded within 24 hours
- Merck's own LLM for integrating data
- SL insights via Genesis (phone app for quick input)
- PDT adds "relevance to our program" to selected abstracts
- GenAI for summarization, comparisons, clinical questions, slide generation, direct trial comparisons

**Shannon's strategic framing (Aug 21):** Forwarded the thread to Patrick noting this is what all leaders want. Suggested Peter Baumeister's ACE data science team could tackle it. Conscious of Patrick's scope-expansion concerns.

**Talia's experiment design (Aug 21):** Shannon forwarded to Talia asking for prioritization. Talia proposed:
1. Adapt sac-TMT research plan/prompts for priority assets, test against existing **ASCO content** to validate approach
2. If successful, rerun refined approach against **ESMO content** and assess as complement to Congress Debrief
3. Timeline: pick up late Aug/early Sept, ASCO retrospective completed by **end of September**
4. JPA role: advisory/design-focused. ACE data science team for execution.
5. Need to clarify: how original research plan was developed (must recreate for other assets) and priority/timing vs. other work.

## Pending Updates (Streamlit app)

- Demo to Stephen, Danny, and EPAM (not yet scheduled)
- MUSE pairing integration
- NCT 3 registry bucket
- Additional competitor data

## Strategic Context

- **Ellie Norris discovery:** Merck doing internal discovery on Asset Reporting workflow with Ellie Norris (Head of Data Products). Before building further, investigate whether similar enterprise capabilities already exist (Databricks, Muse, registries).
- **Northern Light license:** HH paid for enterprise license (via Amy Caswell). Could provide congress event dashboards.
- **Peter Baumeister / ACE team:** V&I Data Lake team already syncs Citeline data to datalake. His team (30 data scientists) scrapes "all the sites." Planning "Congress Data as a Product." May eliminate need for some vendor feeds.
- **Josefine Roemmler-Zehrer (MSD Germany):** Asked how AI derives implications for Merck program and which data sources it relies on. Key stakeholder for global buy-in.
- **Veeva Link News:** Stephen Leong asked (Aug 31) about integrating Veeva Link News insights into congress reporting. Not yet explored.
