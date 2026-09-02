---
name: genesis-status
description: "Genesis Sentiment 2.0 -- first release = Sentiment Overview, Figma V3 in progress. Matt has Databricks access (big win), working on table data view. Feature requirements delivered to working team ~Aug 19. Ulf departed. Genesis Validation series ended; Matt joining Core Team. As of Sep 2, 2026."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4b881dac-e446-4b63-b338-c9ba1f6228ea
  modified: 2026-09-02T14:46:12.649Z
---

## Current State (Aug 31, 2026)

**First release scope narrowed to Sentiment Overview only.** Workshop consensus (Aug 25): ship one really good widget rather than overwhelming users. Heatmap and other features deferred to subsequent releases. Late September / early October target.

**First release components:**
- Donut chart with sentiment breakdown (Positive / Neutral / Negative)
- Tab view showing ALL drivers per sentiment category (not limited to top N)
- Overview landing with top drivers per category at a glance
- Driver display: compact (title + bar + metadata) with expand for full AI summary; no truncated previews
- Export functionality re-elevated as important (was deprioritized)
- Confidence threshold: only findings > 0.7 shown
- "Save Study" renamed to "Save" or "Save Analysis"

**Key category change: "Uncertain" renamed to "Negative."** Full consensus from Caitlin, Kristen, Adi, and Patrick at Aug 25 workshop. "Mixed" category also removed for now.

**Figma V3 prototype (Aug 28-29):** Patrick shared updated Figma (Sentiment-Analysis-2.0-V3-Sep) with Kristen and Caitlin. Seven design changes implemented. Michal posted 8 agreed next steps targeting Sept 1:
1. Add topic/aspect descriptions from aspect repository
2. Findings link opens modal window
3. "1,430 insights" figure becomes clickable (expands right panel)
4. Total findings per driver group (as in Ulf's prototype)
5. Expand disclaimer with clustering context
6. Findings explanation modal with confidence > 0.7 note
7. Findings link to original insight
8. Simplify side panel (only driver-related findings, remove "Original Insights")

**Requirements doc shared with dev team (Aug 21):** Distributed to Michal, Ulf, and Yun. High-level features requirement with user research pull quotes, not a technical/business requirements doc. Also serves as JPA onboarding artifact and post-Ulf continuity document.

**Ulf Nielsen departed Aug 31.** JPA positioned as strategic-technical bridge. Backfill timeline unclear (months).

**Databricks access (Sep 2):** Matt has access to Databricks (big win). Still working on getting actual table data view -- should be a minor technical hurdle.

**Feature requirements delivered** to the Genesis working team (Michal, Ulf, Yun) approximately Aug 19 (~2 weeks ago). High-level features requirement with user research pull quotes.

**Genesis Validation weekly series ended.** Matt has been asked to join the Genesis Core Team meetings -- need to get invite from Patrick.

## Stakeholder Buy-in (Strong)

- **Brandon pre-meeting (Aug 26):** Patrick presented expected first release deliverables at Gem's regular check-in (replaced original ELT presentation).
- **Caitlin Bill:** No longer asking "what will be there" -- trusts delivery. Pivoting to 2027 USMA strategy integration. Endorsed shift away from forced actionability in insights. First use case: institution-level sentiment filtered and bookmarked for OMP meetings. Longer-term: an agent that continuously tracks her institutions.
- **Kristen Slangerup:** Confirmed sentiment overview with pie chart is "exactly what we're looking for" for high-level leadership reporting. Wants all drivers visible. Notes timely alignment with growing global interest in sentiment -- Genesis becomes the answer to "how do we do it consistently."
- **Patrick tying sentiment explicitly to 2027 USMA objectives** (discussed with Caitlin Aug 20).

## Workshop Findings (Aug 25)

Key shifts from the user feedback session with Caitlin, Kristen, Gem, Adi, Ted:

**Insight Actionability SOP Changing:**
- Adi removed the "insight quality equation" from training curriculum (got approval). Moving away from requirement that insights must be actionable.
- Vision: "Enter what you hear, let AI analyze the volume." Context-rich intelligence > pre-structured insights.
- Gem requested inclusion in actionability SOP discussions (affects her Insights Coaching Agent, built on current SOP).
- Organizational resistance still exists; Adi taking incremental steps. Caitlin/Kristen's backing is significant new support.
- Germany example: country directors curate/filter insights before entry, which skews sentiment data.

**Export Concern:**
- Kristen strongly advocated for export capability (FMADs will demand it).
- Risk: users will put exported data into GPTeal/Gemini, undermining Genesis consistency.
- Patrick frames Genesis as a data **platform** not portal; goal is to make it so valuable export feels unnecessary.
- Resolution: export remains important; add a column tagging which sentiment category each insight contributed to. Ask Genesis can help with context in interim.

**Filters:**
- ~~Ted Kwok to create XFly-to-Genesis filter mapping cheat sheet.~~ DONE (Aug 27) -- Ted shared `x-Fly to GENESIS field mappings.xlsx` with Cinnamon, Matt, Grace, and Jan. Patrick suggested a mind map visualization; Ted tried Gemini and CoPilot, CoPilot produced the better result.
- Saved filters/bookmarks already exist in production (not in Figma mock). Shareable canonical team filters concept liked by Patrick.
- SEP-based filtering (future): ability to filter by specific SEP would be very valuable -- some SEPs bias sentiment.
- Institution/organization data critical for launch (Patrick emphasis): "protein for health systems." "Other" overwhelmingly selected for institution field, which is problematic.

**Preview Concept (In-App "Coming Soon"):**
- Michal proposed releasing preview before full rollout. Risk: whichever dataset shown will annoy people not represented. No time for fake data.
- Resolution: keep concept but make it more separate from main Genesis experience. Possibly use Figma interactivity rather than live data.

## X-fly / Platform Evolution

- Viva/X-fly may not have a long-term future for insights. VML (current vendor) is not effective. IAmRemarkable IT is "chomping at the bit" to build a replacement.
- Patrick envisions: "Genesis becomes the brand of scientific insights."
- Colin: third big pharma client to say Viva doesn't have a long-term future for insights.

## Key Decisions and Debates

- **Databricks vs. Genesis DB:** Jan still undecided. Ulf preferred Databricks-native.
- **Emerging themes:** Supervised vs. unsupervised. Not resolved.
- **ACE + BI team merge (Aug 11):** Not yet officially announced.
- **Data quality concern:** Adi raised that Germany country director admits to curating insights before submission. Affects sentiment analysis because quantity matters.
- **Sorcero:** Patrick meeting with VP (Aug 27 follow-up). Personnel changes on their side. Shannon flagged as good match for insights.
- **Jan Folkman:** Met with Shannon Aug 26 for 30-40 min. Taking lead on listing capabilities, reaching out to Patrick for intro.

## JPA Action Items

1. **Continue strategic-technical bridge role post-Ulf** -- architecture, strategy, stakeholder facilitation
2. **Lean into first release delivery** -- partner with Jan, Michal, and devs
3. KPI template (operational vs. strategic impact, kept separate)
4. Document on why system of record matters vs. ad-hoc GPTeal (up to 20% variance, no validation)
5. User guide / one-pager for Sentiment 2.0 rollout
6. ~~Databricks access for Matt~~ DONE (Matt has access as of Sep 2). Working on table data view (minor technical hurdle).
7. **Matt offered working session with Gem** on Insights Coach Agent (Studio/node config issues)
8. **Get access to insights data in Databricks** -- Matt has platform access, need actual table/data view
9. **Get invite from Patrick** for Genesis Core Team meetings (replacing Validation series)

## Insights Coach Agent (Gem Roy)

- Moved from Agent Builder to Studio for more consistent output. Works in Studio test but breaks when shared via Teams chat or Copilot space.
- Problem: agent uses search-and-retrieve (keyword matching) instead of evaluating against SOP as guidance. Working on fixing node/generative configuration.
- Catching fire in the org -- stakeholders asking about production timeline. Gem bringing to Studio.
- SOP dependency: currently built on "insights must be actionable" SOP that is now changing.

## HTA/Outcomes Research / GPTeal (Aug 13-14)

Michael Hamann's (EMEAC hub lead) project: global value dossiers in Gemini Notebook for HTA assessments. Patrick formally requested JPA help. Schedule still pending.

## Related Memories

See [[merck-stakeholders]] for full stakeholder map including Genesis-specific people.
