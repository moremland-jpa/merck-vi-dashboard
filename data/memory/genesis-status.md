---
name: genesis-status
description: "Genesis Sentiment 2.0 -- Patrick reframing first release as 'statement of principles' + bespoke report tools (Sep 11). Production release Sep 12 (backend enrichment only). Demo feature with static real data. As of Sep 11, 2026."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4b881dac-e446-4b63-b338-c9ba1f6228ea
  modified: 2026-09-11T15:16:48.814Z
---

## Current State (Sep 4, 2026)

**First release scope narrowed to Sentiment Overview only.** Workshop consensus (Aug 25): ship one really good widget rather than overwhelming users. Late September / early October target.

**Patrick's detailed roadmap (Sep 3 weekly check-in):**
- **Release 1 (late Sept/early Oct):** Donut widget only (sentiment overview). Filter from regular Genesis, jump to slightly newer sentiment UI. Donut breakdown → clickable positive/negative/neutral drivers → AI summaries → findings with metadata + insight code link back to X-fly. Export: minimally a file, ideally PowerPoint. Full report with original insight text for trust/verify. Topic heatmap may or may not make first release.
- **Release 2 (late Oct):** Bug fixes, immediate low-hanging fruit improvements.
- **Release 3 (Nov):** Re-unify Genesis UI (currently bifurcated old vs. sentiment views). Continue widget rollout.
- **Longitudinal trends:** Deferred until SME agreement on data enrichment quality. "Before we say trends over time, we want to make sure the way we're enriching and displaying has large agreement."

**Critical architecture advantage:** Sentiment data is pre-processed daily (unlike Genesis summaries which generate in real-time). This eliminates the performance/scale issues that sometimes impact existing Genesis. "Really what you see is filtering because all the work has been done." Learnings will be applied back to summary side.

**Data enrichment pipeline currently self-hosted.** Eventual goal: done on Databricks side, but BI team has too many deliverables. Steve and Peter aware. Probably moves next year.

**Brandon Palermo emphasis (Sep 3):** Brandon told Eric directly: "sentiment is the most important thing for him." Eric now putting extra emphasis. Patrick presenting to Brandon + Eric Sep 3 afternoon. Patrick confident (has shown Brandon before, gotten feedback/encouragement), but showing Figma mock-up, not real software -- wishes he could show the real thing. Colin's advice: prepare for "ask for the moon" scenario; have roadmap answers ready.

**DAC preview next Tuesday (Sep 9).** Growing stakeholder exposure beyond the 6 USMA SMEs.

**Jan's SME validation plan (Sep 3):** Wants to put insights + enriched findings in front of SMEs to validate agreement with how data is broken down. Using Genesis Champions Network (may also leverage DAC per Gem's suggestion). Gem offered to participate. Finally happening after months of discussion -- waited until data enrichment pipeline matured.

**First release components:**
- Donut chart with sentiment breakdown (Positive / Neutral / Negative)
- Tab view showing ALL drivers per sentiment category (not limited to top N)
- Overview landing with top drivers per category at a glance
- Driver display: compact (title + bar + metadata) with expand for full AI summary; no truncated previews
- Export functionality re-elevated as important (was deprioritized)
- Confidence threshold: only findings > 0.7 shown
- "Save Study" renamed to "Save" or "Save Analysis"

**Key category change: "Uncertain" renamed to "Negative."** Full consensus from Kate Lynn, Kristen, Adi, and Patrick at Aug 25 workshop. "Mixed" category also removed for now.

**Figma V3 prototype (Aug 28-29):** Patrick shared updated Figma (Sentiment-Analysis-2.0-V3-Sep) with Kristen and Kate Lynn. Seven design changes implemented. Michal posted 8 agreed next steps targeting Sept 1.

**Requirements doc shared with dev team (Aug 21):** High-level features requirement with user research pull quotes. Also serves as JPA onboarding artifact and post-Ulf continuity document.

**Ulf Nielsen departed Aug 31.** JPA positioned as strategic-technical bridge. Backfill timeline unclear (months). Patrick: "Ulf wasn't a data scientist, but he was a jack of all trades... we have no other strong data people."

**Databricks access (Sep 2-3):** Matt has access to Databricks. Can see insights data is there but can't see the data itself yet. Jan has been super helpful in pushing access through. Matt expects resolution Sep 3 afternoon. "Minor technical hurdle."

**Genesis Validation weekly series ended.** Matt now on Genesis Core Team meeting invites (as of Sep 3). Next few weeks' meetings will be on adjusted schedule due to Patrick's travel.

**Grace Abrahams left JPA (Sep 4).** "Databricks FOMO" -- she's sad to miss the data access they just got. New staff member **Molly** starting Sep 14 (NJ-based). Other new hires being considered, partly because of new system access.

## Stakeholder Buy-in (Strong)

- **Brandon pre-meeting (Aug 26):** Patrick presented expected first release deliverables at Gem's regular check-in (replaced original ELT presentation).
- **Kate Lynn Bill:** No longer asking "what will be there" -- trusts delivery. Pivoting to 2027 USMA strategy integration. Endorsed shift away from forced actionability in insights. First use case: institution-level sentiment filtered and bookmarked for OMP meetings. Longer-term: an agent that continuously tracks her institutions.
- **Kristen Slangerup:** Confirmed sentiment overview with pie chart is "exactly what we're looking for" for high-level leadership reporting. Wants all drivers visible. Notes timely alignment with growing global interest in sentiment -- Genesis becomes the answer to "how do we do it consistently."
- **Patrick tying sentiment explicitly to 2027 USMA objectives** (discussed with Kate Lynn Aug 20).

## Workshop Findings (Aug 25)

Key shifts from the user feedback session with Kate Lynn, Kristen, Gem, Adi, Ted:

**Insight Actionability SOP Changing:**
- Adi removed the "insight quality equation" from training curriculum (got approval). Moving away from requirement that insights must be actionable.
- Vision: "Enter what you hear, let AI analyze the volume." Context-rich intelligence > pre-structured insights.
- Gem requested inclusion in actionability SOP discussions (affects her Insights Coaching Agent, built on current SOP).
- Organizational resistance still exists; Adi taking incremental steps. Kate Lynn/Kristen's backing is significant new support.
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

## Key Developments (Sep 8-9)

### Production Release Friday Sep 12 (Sep 8 call)
- **Data enrichment pipeline deployed to dev.** Code crunching ~80K dev insights and extracting findings. GPTL API (internal wrapper for Azure-hosted GPT models) hit rate limits -- shared Azure throttle across all Merck projects. Solution: batch insights into ~100-insight packages with automatic retry on failure.
- **One-time weekend processing:** Initial run over the weekend when traffic is low. After that, only daily incremental processing of new insights (couple dozen to a few hundred per day). Not weeks of catch-up -- just a weekend of heavy processing.
- **Nothing user-visible in this release.** Backend data enrichment only. Front-end connection comes in the next release.

### Demo Feature in First Release (Sep 8)
- **Static demo with real data.** Jan preparing a pre-processed subset using the same enrichment pipeline. All numbers will be real, everything clickable/browsable/exportable. Users CAN'T change filters -- locked to one meaningful data view.
- **Needs help selecting filter set.** "Oncology last 30 days" too broad to be meaningful. Need a set of filters with business value that people would understand. Team to advise.
- **Export: PowerPoint is Brandon's expectation.** PDF and Word also technically feasible (code libraries available). Design work needed for polished output -- "not just clumsily exported charts."
- **Demo accessible via pop-up panel** in Genesis UI (per Michal's design). "Explore the demo" button.
- **Optional for this release:** Chat functionality for individual findings, product tour tooltips.

### Brandon's Expectations / Stakeholder Pressure (Sep 8)
- **"Sentiment is the most important thing for him."** Town hall featured sentiment. Patrick: "He is counting on us to deliver what he needs. We have such an amazing opportunity."
- **Scope change inevitable:** Patrick preparing team emotionally -- "we're going to put this out there and our stakeholders are going to say, this is great, but I need these 17 things." Jan confident: once enriched data is in DB, new visualizations are just front-end work ("pie chart in a week").
- **Data contract designed universally** so any chart type can be built on the same enriched data without touching the backend.

### Topic Monitoring / Trending (Sep 8)
- **Brandon anchored on domain-specific topics** (e.g., "food effect" -- oddly specific but critical). Two types of topics:
  - **Stable topics:** 11 identified through data analysis; labels can be decided. Shown in current Figma.
  - **Emerging topics:** Unsolved. Ulf left without a solution for detecting when the field starts talking about something new. Need to distinguish noise from real signal.
- **Adi's bridge idea:** Manually collect specific topic requests from Brandon's stakeholders and add them as custom topics until emerging topic detection is built. Patrick: "Good idea."
- **Trending over time:** Adi and Kate Lynn Bill both want ability to see how a topic's sentiment has changed over time. Gem relayed Kate Lynn's suggestion: classify topics first, THEN do sentiment analysis on those (rather than the reverse).

### Patrick Travel / Team Coverage (Sep 8)
- **Patrick on business travel this week (Sep 8), vacation next week.** Relying on Matt, Adi, Gem, Ted to keep things moving with Jan/Michal.
- **Jan's methodology presentation:** Wants to walk team through the data enrichment science (how insights become findings). Couldn't fit in Sep 8 meeting -- targeting later this week or next Monday.
- **Jan requested to add dates to release roadmap** -- rough timeline for rest of year to help Adi's team plan testing. Not enterprise-level documentation, just high-level dates per release.

### Sentiment Category Debate (Sep 8)
- **"Uncertain" makes sense only in study data context** (e.g., HIV DOR/ISL -- people uncertain they can act on the data). In general Genesis analytics, positive/negative/neutral is the right framework.
- **Ted's concern:** "Neutral" might mask negative sentiment. "Are they saying there are no negative sentiments, or are they just afraid to say it?"
- **Resolution:** Genesis keeps positive/negative/neutral for standardized analytics. Users can interpret sub-categories in their own PowerPoint exports. Need universal sentiment terminology across the org -- town hall showed everyone presenting the same data in their own language.

### Joe Cianciulli / Jason Shaffer Genesis Slides (screenshots Sep 10)
- **DOR/ISL CROI 2026 sentiment analysis output** -- shows the donut chart format Genesis is building toward: 65% positive, 20% neutral, 15% negative (N=84 RMSD insights). Includes driver summaries per category.
- **M184I/V focused effort timeline** -- CROI → Insights & Publication → IDVYNSO Approval → MRL Plan. Shows sentiment evolution across three time windows (30/60/90 days post-CROI). Positive sentiment declined from 72% to 45% while negative grew from 10% to 30%.
- Reference material for what Genesis produces today and what the new Sentiment 2.0 UI should match/improve upon.

### Feature Request / Intake Process (Sep 8)
- **JPA took action to define process** -- prioritization framework with rationale for what's being worked on and what's not. Matt: "Get ahead of it... otherwise the well gets poisoned because they'll talk to Brandon and say we're giving suggestions and they don't do any of them." Jan agreed: "worst thing is you ask for feedback and then you don't act on it or you don't get back."
- Matt to work with Yun and Michal on this while Patrick is out.

## Key Developments (Sep 11)

### Patrick's Sentiment Reframing (Teams Sep 11, 6:39 AM)
Based on recent conversations with additional USMA stakeholders, Patrick shared two strategic shifts:

1. **First release as "statement of principles."** Sentiment needs to get into users' hands as planned, but it probably won't meet everyone's specific needs. First Sentiment Analysis release for Genesis will be a "statement of principles" of where we are and where we want to go -- expectation-setting, not feature-complete.

2. **Dashboard + bespoke report tools.** Sentiment Analysis in Genesis may end up being a dashboard AND a set of tools for people to make their own bespoke reports. Patrick: "I don't know if that is completely different from what we were already planning, but our positioning might be better" (message cut off in screenshot -- may contain more).

**Implication:** This aligns with the "export is critical" feedback from Kristen and the workshop, and with Kate Lynn's institution-level filtering use case. The framing shift lowers the bar for first release (demo feature with static data fits this positioning) while raising the long-term ambition (self-service reporting platform, not just a dashboard).

## JPA Action Items (Sep 10)

1. **Continue strategic-technical bridge role post-Ulf** -- architecture, strategy, stakeholder facilitation. Patrick's specific ask: "listen to what we're doing and make sure we're not doing something completely asinine" on data science assumptions.
2. **Lean into first release delivery** -- partner with Jan, Michal, and devs. Next couple weeks = finishing backend data enrichment. Last couple weeks = enabling something.
3. KPI template (operational vs. strategic impact, kept separate)
4. Document on why system of record matters vs. ad-hoc GPTeal (up to 20% variance, no validation)
5. User guide / one-pager for Sentiment 2.0 rollout
6. ~~Databricks access for Matt~~ DONE (Matt has access as of Sep 2). Working on table data view (minor technical hurdle -- expects resolution Sep 3).
7. **Matt offered working session with Gem** on Insights Coach Agent (Studio/node config issues)
8. **Get access to insights data in Databricks** -- Matt has platform access, need actual table/data view. Jan (formerly listed as "Joanna") helping.
9. ~~**Get invite from Patrick** for Genesis Core Team meetings (replacing Validation series)~~ DONE (Matt on invites as of Sep 3)
10. **JPA: Define feature request/intake process** -- Matt working with Yun and Michal while Patrick travels. Prioritization framework with rationale.
11. **Help Jan select meaningful filter set** for demo data -- needs business-relevant filters, not "oncology last 30 days"
12. **Attend Jan's methodology presentation** -- enrichment pipeline deep dive (this week or next Monday)

## Insights Coach Agent (Gem Roy)

- Moved from Agent Builder to Studio for more consistent output. Works in Studio test but breaks when shared via Teams chat or Copilot space.
- Problem: agent uses search-and-retrieve (keyword matching) instead of evaluating against SOP as guidance. Working on fixing node/generative configuration.
- Catching fire in the org -- stakeholders asking about production timeline. Gem bringing to Studio.
- SOP dependency: currently built on "insights must be actionable" SOP that is now changing.

## HTA/Outcomes Research / GPTeal (updated Sep 3)

Michael Hamann's (EMEAC hub lead) project: global value dossiers in Gemini Notebook for HTA assessments. **Status: wait-and-see.** SRO (Strategic Realization Office, Sashin's team under Eric) setting up small workshops. Patrick suggested starting with Gemini Notebook + upload GVD. They're scheduling during Patrick's vacation, broken into 15 small meetings. JPA involvement only if they decide it's promising and need a larger virtual workshop. Patrick explicitly trying to keep JPA out -- focus should be Congress and Genesis.

## Viva/X-fly Future (Sep 3 discussion)

- Patrick frustrated with Viva Medical Insights progress. "What are you doing? We don't want half this stuff."
- Colin: JPA's official position is everyone should wait a year because of the Viva roadmap. It may turn around.
- If Merck builds own system, would need to connect to MDM for institution/account resolution.
- Institution tagging is a major data quality problem: "Other" overwhelmingly selected for institution field. Not a Genesis problem -- it's a data input problem. Germany country directors curate/filter insights before entry.
- Gem's Insights Coach Agent could help with tagging best practices ("just a reminder, do you need to include...").
- Patrick envisions: "Genesis becomes the brand of scientific insights."

## MAPS 2027 (Sep 3)

- **Gem formally accepted for Boston AI Ethics Panel.** Recommended by USMA stakeholder, spoke with Robin Wintersberry (Americas leader). Easy acceptance process.
- Colin and Gem meeting Sep 3 afternoon to ideate on AI ethics content.

## Related Memories

See [[merck-stakeholders]] for full stakeholder map including Genesis-specific people.
