---
name: genesis-status
description: "Genesis Sentiment 2.0 -- Oct 28 update: UAT underway; beta for MRL users only targeted Thu Oct 29 with go/no-go on the Wed Oct 28 call; HH access delayed ~2-3 weeks; Oct 23 go/no-go slipped (test DB still processing); Excel export phase 1; scope frozen; XFly team split/remap Oct 30-Nov 3; upload-your-own-insights debated Oct 12. Earlier -- Oct 1-2 Teams: duplicate-findings case was a faulty extraction that was re-run; Jan Chmelar says 500K+ findings will never be 100% right, 105 compute-hours to re-extract all, proposes sample-based quality assessment (Sentiment Analysis part 2 with Peter Baumeister's data scientists Oct 2); filter order decision = one global custom order matching XFly (Adi, Patrick agree). Sep 28 weekly: 'findings' confirmed as launch terminology, real concern is finding-quality not the label; Matt to get code access via Steve Bridgeman and quantify finding-identification issues ASAP; Patrick meeting the former-BI team (Ulf's backfill) Sep 29; adoption risk may be workflow inertia, not awareness. Also Sep 25: confirmed findings-extraction duplicate-findings defect (v2d prompt, fix exists in v2e but not canonical), independently flagged by Matt via dashboard note too; Matt's field-team manual-labeling idea (training data + trust-building) not yet raised with the team; ESMO sentiment ask blocked on 3 open questions; RMSD dropped as Figma source filter; PowerPoint export agreed for demo but Export button still broken. As of Sep 28, 2026."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4b881dac-e446-4b63-b338-c9ba1f6228ea
  modified: 2026-10-28T15:08:14.041Z
---

## Current State (Sep 4, 2026; updated Oct 28)

**Where Sentiment 2.0 stands (Oct 28):**
- **Beta launches to MRL users only, targeted Thu Oct 29.** Sentiment 2.0 is in UAT on the test environment (ingesting production data; business team runs UAT from Jan's UAT test plan + release notes R26.6). **Go/no-go is the Wed Oct 28 Genesis touch-base call** (Patrick dialing in from the road; Jan joins despite the Czech holiday). Deployment takes 30-90 min once approvals are in. The ESMO team expects to use it as first impressions turn into approved insights.
- **HH (commercial) access is deliberately delayed ~2-3 weeks** (Patrick's call, Oct 23-26, after Brandon + BI-team concerns): HH users keep Sentiment 1.0 and don't see the 2.0 button. Plan is to run it past USMA / Eric's leadership office hours first, then turn on for HH.
- **Scope freeze:** no new functionality or extraction changes before launch (re-extracting production takes 100+ hours). Only bug fixes and static-text edits; only driver titles/summaries are LLM-generated. Excel export is phase 1; PowerPoint export is next (open: one USMA template vs. TA-specific).
- **Open/unresolved:** Oct 23 go/no-go slipped because the test DB was still processing and the UI was still being finalized (Adi asked for a release-readiness checklist); a leftover guidance-overlay browser extension (Kyle's test) pops up on Genesis and Patrick is escalating to Ops; survey has had essentially no responses (one positive); need an answer for users asking for their own/emerging topics.
- Details in the Oct 12 / Oct 20 / Oct 23 / Oct 26-27 sections below.

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

## Key Developments (Sep 10)

### Databricks Access -- Compute Resource Hurdle
- Matt confirmed (weekly check-in) he now has Databricks access AND permission to see the insight data tables, but still lacks an **allocated compute resource to run any code against it**. This is a separate, deeper permission -- ticket already routed to the right Databricks/IT team with business justification attached; Matt following up directly rather than waiting.
- Once resolved, Databricks also becomes usable as a dev environment for MRL Debrief prototyping code (point at a folder as the data source) -- see [[mrl-debrief-status]].

## Key Developments (Sep 11)

### Patrick's Sentiment Reframing (Teams Sep 11, 6:39 AM)
Based on recent conversations with additional USMA stakeholders, Patrick shared two strategic shifts:

1. **First release as "statement of principles."** Sentiment needs to get into users' hands as planned, but it probably won't meet everyone's specific needs. First Sentiment Analysis release for Genesis will be a "statement of principles" of where we are and where we want to go -- expectation-setting, not feature-complete.

2. **Dashboard + bespoke report tools.** Sentiment Analysis in Genesis may end up being a dashboard AND a set of tools for people to make their own bespoke reports. Patrick: "I don't know if that is completely different from what we were already planning, but our positioning might be better" saying "USMA directors, we'll give you the **tools** to help you make your TA and team-specific reports" rather than "we will make the report." Why: user needs are all probably too different (or believed to be too different) to expect alignment on one way of working, at least for now. The **Dashboard** would serve users (leaders) who want a quick pulse check -- key constraint: the data must stay consistent so the dashboard doesn't contradict what USMA generates for themselves.

3. **Need to capture director user-specific needs and identify trends/commonalities** across them to prioritize features.

4. **Down the road: role-based access vs. user-set preferences.** Patrick floated either role-based access showing more specific user preferences, or letting users set their own preferences directly (possibly easier than building role-based access).

5. **USMA-first, but must be ready for non-USMA feedback** (other TAs, other regions, HH). Patrick flagged this as unresolved -- not sure how to triage requests from outside USMA once they start coming in.

**Implication:** This aligns with the "export is critical" feedback from Kristen and the workshop, and with Kate Lynn's institution-level filtering use case. The framing shift lowers the bar for first release (demo feature with static data fits this positioning) while raising the long-term ambition (self-service reporting platform, not just a dashboard). Points 3-5 also foreshadow a feature-intake/triage problem beyond USMA -- relevant to the [[genesis-feature-process]] work already underway.

### Figma Preview with Joseph Cianciulli (dashboard team update, ~Sep 10)
Previewed Figma board with Joseph Cianciulli, Kate Lynn Bill, and Gem Roy. Key feedback:
- **Driver % breakdown: positive reception.** Joe very positive on the percentages shown in the drivers breakdown.
- **Heatmap topics must be brand-specific.** Generic topics won't be useful -- each brand will want to prescribe its own set of topics, and insights should be bucketed on those. Reinforces the "domain-specific topics" theme from Brandon's feedback (Sep 8).
- **Sentiment as strategy benchmark.** Joe's team uses sentiment analysis as a benchmark for the effectiveness of their strategy -- they want to see that sentiment aligns with strategic direction.
- **Quarterly cadence for reliable signals.** Joe wouldn't recommend using sentiment much more than quarterly to get reliable signals. Contrasts with the daily enrichment pipeline -- the data runs daily but meaningful analysis windows are longer.
- **Trending requested.** Wants to see trending in some fashion -- consistent with Adi and Kate Lynn's earlier trending requests (Sep 8).

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
13. **Matt: Follow up on the benchmark discussion with Jan and the data scientists** -- link sent Oct 6 for further discussion; collect feedback on method and results, and fold in Jan's sample-based quality idea. Matt presented to Patrick and Adi Oct 5; capture their reactions.

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

## Key Developments (Sep 25) -- Teams thread, "Genesis 1-5" screenshots

### Figma prototype feedback loop (Michal <-> Patrick)
- Michal implemented Patrick's requested text edits.
- **RMSD removed as a source-filter option** in the Figma prototype -- it isn't actually supported by the product, so it won't appear in any environment.
- **PowerPoint export**: agreed to support in the demo. Jan Chmelar will share the file; Michal wants to review it before it goes to the dev team to wire up the **Export** button, which currently throws an error on click.

### Oncology demo feedback (demo was Sep 24, relayed Sep 25)
- Oncology asked for access to more of their own disease states so they can analyze ESMO results. Ted suggests a test environment instead of Figma -- still an open discussion, not decided.
- **Data mismatch worth flagging:** the topics/findings shown in that demo were not Oncology data -- they were PH/sotatercept results. Confirm before referencing that demo content as Oncology's own in any follow-up.

### SL vs. HCP terminology -- unresolved
- Ted revised a Patrick statement to reference "SL" (Scientific Leader) instead of "HCP." Ted and Patrick then disagreed on the relationship: Ted thinks SL is used generically to include HCPs; Patrick thought SL is a *subset* of HCP (i.e., HCP is the broader category, including everyday treaters, not just thought leaders). Left open, no resolution in thread.
- Reminder from Ted: insights come from RMSDs, MSLs (ex-US), and some reviewers -- not RMSDs alone.

### ESMO sentiment ask -- three open questions block scoping (Patrick, Sep 25)
- Oncology wants something similar to what Melissa and Miguel already showed their own leadership (findings displayed alongside topics) -- they're sending JPA/Genesis a copy of that format. Adi thinks matching it may be too big an ask by end of ESMO. *(Possibly the same Melissa Mims / Miguel already tracked under Congress AI ESMO planning in [[merck-stakeholders]] -- unconfirmed, worth checking before assuming they're the same people.)*
- Patrick: technically doable -- Sentiment 2.0 Release 1 tech is largely complete -- but three things are still undefined:
  1. What data would actually be analyzed for ESMO (insights aren't instant, there's a lag -- unclear how that's handled for a live congress)
  2. Who from Oncology (ONC) would actually use it, so the team can brief them on Release 1's features/limitations
  3. What ONC actually wants to learn from the analysis (sounds like it would be sent to the Genesis/JPA team to produce, not self-served)
- **The Sep 28 Genesis weekly is the venue for this** -- agenda is the GENESIS launch with the Sentiment demo plus this ESMO ask (effectively: whether/how to launch Sentiment 2.0 Release 1 to users). Jan Chmelar and Michal Libich will miss it (Czech public holiday, Sep 28) -- may need a reschedule or their input gathered separately.

### DIA (formerly ACE team) call rescheduled
- The Genesis call with Alex and Charles from DIA (data-science team, renamed from ACE per the Aug 11 ACE+BI merge -- exact current name unconfirmed) moved from 10:30 AM ET to 11:00 AM ET on Sep 25 due to a conflict on Adi's team. Patrick flagged it as important to keep Sentiment 2.0 on track.

### Findings-extraction duplicate-findings bug -- confirmed defect, fix not yet deployed (Ted, Sep 25)
- Ted used GitHub CoPilot (with access to the Exodus source) to diagnose why some Genesis insights display ~6 near-duplicate "findings" that really restate the same 1-2 underlying claims with slightly reworded subject/product.
- **Root cause confirmed:** the live corpus uses the canonical `extract_findings_v2d` prompt, documented to split one insight into multiple near-duplicate findings that each re-attach the same claim. The UI then shows each duplicate's distinct `self_contained_text`, which is why the wording differs per row even though the claim doesn't.
- **A fix exists but isn't deployed:** a newer `extract_findings_v2e` prompt adds rules -- keep reasons/qualifiers attached to their claim, no two findings from one insight may assert the same thing, drop a finding fully contained in another -- but v2e is **not canonical**. Adopting it requires a full re-extraction, reclassification, re-embedding, and re-clustering of the corpus, not a quick swap.
- Ted has a CoPilot-suggested code patch but is deliberately not touching Exodus code without MRL IT's (Jan Chmelar's) sign-off -- planning to review it with Jan directly.
- Ted found more examples in a random sample, confirming this is widespread, not a one-off: INS1008730 (statin/LDL-C-intolerance claims, ~6 near-duplicates) and INS1016854 (KN-483 OS-difference claims, ~6 near-duplicates).
- Matt independently flagged the same defect via a dashboard team-update note (Sep 25, 2:21 PM): "the current code will break insights down into findings that often repeat/duplicate each other. Anyone who sees this will lose trust in the system." Confirms this is the same v2d/v2e issue Ted diagnosed, from a second observation path -- discussion planned next week on what it would take to re-run all insights through v2e.

### Field-Team Manual Labeling Idea (Matt, dashboard team-update note, Sep 25 3:38 PM)
- Idea: ask field teams whether they'd be willing to manually assign sentiment to a set of insights (i.e., label them by hand), and how many they'd be willing to do.
- Two uses for the labels: (1) training/validation data for the model -- what "right answers" look like -- and (2) a trust-building mechanism, so field teams see the model was built to "think the way they do" rather than having a black-box classification imposed on them.
- Not yet raised with Patrick/Jan/Michal. Worth surfacing at the Sep 28 weekly alongside the ESMO sentiment ask and launch discussion, since it touches both data quality (relevant to the v2d/v2e findings-extraction problem above) and stakeholder trust (relevant to the Kate Lynn/Kristen buy-in track).

## Key Developments (Sep 28) -- Genesis weekly, dashboard team update (Molly)

### Launch Terminology and Findings-Quality Concern
- **"Findings" is the term that ships for the 2.0 launch.** Team open to feedback/renaming after launch if users push back, but the bigger concern right now is the quality of filtering into findings, not the label -- directly relevant to the v2d/v2e duplicate-findings defect above.
- **Matt to get access to code to assess "finding" quality** -- Shannon connected him with Steve Bridgeman.
- **JPA action item, ASAP:** Matt to quantify/define the potential issues with finding identification for Genesis 2.0.

### Org Change -- Former BI Team Steps Into Ulf's Role
- **Patrick has a call tomorrow (Sep 29) with the team formerly known as Business Intelligence** -- described as "the new Ulf," i.e. the data-science backfill since Ulf's Aug 31 departure.

### Adoption / Internal Promotion
- **Potential promotion channels:** the Champions Network (Adi Zmiri) and the newly-integrated former-BI team both seen as opportunities to raise Genesis's internal profile.
- **Real adoption risk reframed:** may not be lack of awareness of the tool, but internal teams' adherence to existing workflows over switching to Genesis.

## Key Developments (Oct 1-2) -- Teams threads, "genesis 1-4" screenshots

### Duplicate-Findings Defect: Extraction Re-run, Remaining Concern Is Quality at Scale (Ted Kwok, Jan Chmelar, Oct 1)
- **Ted re-checked the dermatologist-biopsy insight** and found 11 findings that look like potential duplicates (punch/shave/excisional biopsy variants), differing from the earlier screen capture. Jan Chmelar asked what insight it was so he would not have to look it up in the database.
- **Jan: the earlier screenshot data (available Sep 23-29) came from a faulty extraction, since changed and re-extracted.** The earlier set of 6 findings for that insight was faulty and should have been 2 (Ted agreed). Ted noted Copilot's suggestion targeted the extraction piece, so the re-extraction should have resolved it.
- **Jan on the 11 now shown:** a GPT-5.6 evaluation against the production extraction rules (`extraction-v1`) judged them valid distinct findings, not duplicates: the rules say to create the smallest independently meaningful proposition, one finding per object when a predicate applies to several objects, preserve modality/conditions/qualifications/frequency, and avoid semantic duplicates, while similar findings may stay separate when they differ in modality or condition. Copilot, evaluated without those instructions, calls them redundant. Verification is intentionally permissive (fails only on a clear, objective violation). Treat this as Jan's position and a model's evaluation, not an independent audit.
- **Scale and approach:** the TEST database alone holds more than 500K findings; Jan expects they will never all be 100% right. Re-extracting the whole database takes about **105 hours of compute**, so the proposed way to tune extraction is **representative samples assessed for a statistically significant sample**. The team is prepared to re-extract (for example for a better model or new instructions), tagging the whole database with a version tag (`extraction-v1` now). Quality will always vary somewhat even on one version because requests hit different Azure nodes: "there will always be a black box element." Relevant to Matt's action to quantify finding-identification issues.
- **Patrick:** good topic for **part 2 of the Sentiment Analysis discussion (Oct 2) with Peter Baumeister's data scientists**; Jan said he would join. Ted did not have the meeting on his calendar.

### Filter Order Decision (Jan Chmelar, Adi Zmiri, Patrick, Oct 2)
- **Genesis filters are alphabetical (since April 2026); the goal is the same order as XFly.** Jan, after talking with Steve Bridgman, offered two options (one global setting, or user-specific order) and recommended one global setting; medium urgency.
- **Adi Zmiri prefers the global setting matching XFly** (user-specific sounds complex); Patrick agreed. Gem asked whether users can still keep their own settings: users can still **save filters, but not set their own drop-down menu order.**

## Key Developments (Oct 5-6) -- Genesis benchmark analysis shared (Matt)

### Benchmark Analysis Presented and Shared (Oct 5-6)
- **JPA's benchmark analysis is complete and pushed to GitHub** (`merck-genesis` repo). It tests the unique value of Genesis's finding-decomposition: 100 Genesis insights run as-is (no training or context) through GPTeal and Copilot with a simple prompt, compared with Genesis on findings per insight, sentiment, and topic, plus within-tool repeatability for Copilot and Genesis. Genesis is the reference, not ground truth. Detail in [[project-genesis-benchmark]].
- **Oct 5:** Matt presented it to **Patrick and Adi**.
- **Oct 6:** Matt sent the link to **Jan Chmelar and the data scientists** for further discussion. This lines up with Jan's Oct 1 proposal to assess finding quality on representative samples, and with the Sentiment Analysis discussion (part 2, with Peter Baumeister's data scientists).
- **Not yet captured:** reactions from Patrick and Adi, and the headline results; add them here once Matt shares them.

## Key Developments (Oct 8) -- Weekly check-in notes (Matt)

### Demo Launched; Live Sentiment Release End of Month (Oct 8)
- **Sentiment demo launched Wednesday Oct 7** (2 options, data toggles). **Live sentiment release is targeted for the end of October.**

### Trust From the Start: Let Users Upload Their Own List (Oct 8)
- **Patrick asked Matt to think about users distrusting the tool from the get-go.** Patrick's view: the answer may simply be letting people upload their own bespoke list of findings.
- **Positioning:** Genesis is positioned as the expert, so Matt expects to need to prove the new model is good.
- **Cost / next step:** upload is a high development need, so verify the exact plan with user interviews before committing.

## Key Developments (Oct 12-21) -- screenshots added Oct 21 (meeting-note excerpts, Teams, GitHub docs)

### Global Oncology's Own GPTeal Sentiment Prompt vs. Genesis (Teams, Oct 12)
- **A forwarded Teams message (Rocio Ledesma, Oct 12 1:13 PM) shares the sentiment prompt that members of the global Oncology team use in GPTeal**, which FMAD colleagues in the US run after extracting all the insights. The prompt casts the model as an expert scientific writer, tells it to judge overall sentiment toward a topic (e.g. subcutaneous) as positive/neutral/negative, quantify each as a percentage of the total, identify patterns within each category, and optionally give at least one verbatim insight per category.
- **The sender asks whether the team can also obtain the prompt behind Genesis** so the two can be compared and the differences understood. Open: who supplies the Genesis prompt. This is the manual workflow Genesis sentiment is competing with, and it lines up with Matt's benchmark framing (simple-prompt GPTeal vs. Genesis); see [[project-genesis-benchmark]].

### Andy (Pulmonary Hypertension / COPD) -- How the Field Captures Sentiment Today (meeting-note excerpt, screenshot Oct 21; meeting date not shown)
- **Who:** Andy led implementation and strategic execution for the pulmonary hypertension and COPD teams after recently moving off the CVM team; Daryl works with Andy; Charles and Patrick were also on. Matt introduced as a JPA data scientist; the discussion gathered Andy's feedback on Genesis (data used, how often analysis is done, how it fits the workflow, how it is shared, and whether outputs should be monthly or quarterly).
- **Current process:** PH team moved from tracking 31 high-priority accounts with labor-intensive PowerPoint slides to a **quarterly account-level review** (priority accounts via ACE and DHH enterprise data; accounts lagging peers in guideline-concordant care). Summaries go to Brandon, Dean, and Bjorn. 16 priority accounts in scope; monthly sessions at US MAP meetings (20-30 min).
- **Sentiment capture via Copilot + Microsoft Forms:** RMSDs fill a Form within **5-10 minutes** after an engagement and rate each insight 1-5 (1 = uncertainty, 3 = neutral, 5 = positive) using detailed assessment criteria; each entry is timestamped, and Copilot builds the analysis. Forms feed automated PowerPoint account summaries and quarterly cross-functional workshops. Viva does not yet provide a usable account-level capture. Andy said sentiment capture was initially hard (new method plus double documentation) but is now sustainable.
- **Validation:** Andy and Daryl check RMSD sentiment against enterprise data in a master tracker. The two sources have generally correlated closely enough that Andy considers the form data accurate for telling the account story. ACE shares enterprise data monthly (moved from quarterly); the broader team stays blind to it so sentiment is not biased by prior-quarter trends.
- **Gaps relevant to Genesis:** Insights only captures what RMSDs intentionally enter, so it does not always give the full account picture (hence the Form). **Form entries cannot be linked back to individual XFly insights** because account-level data is de-identified for compliance, and account lists change quarterly so naming is inconsistent (bracketed labels vs. dropdowns). Account-level analysis remains needed through the product lifecycle (pre-approval snapshots, post-approval data/medical-value narrative; COPD narrative changes).
- **Patrick's sentiment 2.0 pitch (same meeting):** described the findings-based approach (LLM decomposes each selected insight into atomic findings and separate topics, analyzes sentiment per finding, runs repeatability checks); UI shows sentiment per driver, an AI summary, and linked findings so users can review the source insight and challenge a negative vs. neutral call; results below a relatively high confidence threshold are excluded; topics are LLM-generated from the full dataset, not predefined (e.g. nutrition, weight gain); roadmap includes following a topic and asking questions via chat. **Release expected "the following week" with two real but non-editable demo datasets (one oncology); a later version lets users filter their own data; initial launch supports Excel export** -- reliable data first, then customizable visuals and reports rather than a fully prescriptive product.

### Oct 2 Sentiment Analysis Part 2 -- LLM Configuration and Follow-ups (meeting-note excerpt, screenshot added Oct 21)
- **Jan clarified that nearly all individual pipeline steps run on "GPT Sol 5.6"** (as written in the notes) with task-specific prompts, instructions, and examples of desired and undesired behavior. Raji asked whether analyses could be compared across multiple LLMs; the transcript did not capture an answer.
- **Follow-ups:** Peter to prioritize consulting support on the sentiment pipeline methodology and define model tests the team can run on its data; Zach to involve senior stakeholders in the insights development process and gather feedback on an effective sentiment and broader insights product.

### Enrichment Stability n=600 -- Table Schema Documentation (GitHub screenshots, Oct 14)
- **Dataset documented for the data scientists:** `insights` (600 rows, stratified TEST sample with design weights by therapy area x region x length tertile), `runs` (3 stability runs; the original 100 insights run 2026-10-02, 500 more processed later with the same input versions and prompt hashes), `findings` (12,174 rows, one per extracted finding per run, with verification and would-store-in-production flags), `classifications` (10,554 rows: aspect, actionability, sentiment labels with confidences and 0-100 strength/weight), and `finding_embeddings` (12,174 rows, text-embedding-3-large at 128 dimensions). Generated by `code/build_tables.py`, published as CSV and Parquet. See [[project-genesis-benchmark]].

## Key Developments (Oct 12) -- Genesis weekly (transcript)

### XFly Team Split Forces a Tag Remap; Upload-Your-Own-Insights Debate (Oct 12)
- **XFly restructure (Oct 12):** general medicine is splitting into specialty medicine and pharma, and the health systems team is also split out (to payer/health system SP&ID), so **3 new TAs**; the change aligns with the Databricks change and lands **Oct 30 or Nov 3** (Steve to confirm). Historical general/specialty-medicine insights stay under the old team in XFly, so the data lake needs a **remapping** (Sundaram, data lake, joined; Kyle's mapping via product/disease state/subtype leaves ~100 unmappable insights). Separate working call with Steve and Sundaram. Must preserve earlier Genesis fixes for insights that weren't mapped correctly. Ted flagged that tag changes can break users' **saved filters/searches**, so users will need to be told.
- **Patrick's framing:** ~150 insights in XFly vs ~132 in Genesis is what erodes trust; job one is not breaking XFly compatibility. Floated an alternate way in: **let users bring their own insights (upload Excel of insight numbers)**, also answering the old "let me exclude some insights" request. Adi suspects reviewers feed GPTeal pre-reviewed Excel files (actionability notes included), which would explain why GPTeal differs from Genesis and would give a like-for-like comparison; also helps team-specific lists without exposing submitters (compliance anonymity). Gem and Ted (upload SEPs to cross-reference) in favor.
- **Matt's cautions (on the call):** upload puts the model front and center (must prove Genesis beats GPTeal on the same input); it is a heavy build because Genesis pre-processes overnight; and it creates an unregulated process with no oversight of what users load (needs a strong disclaimer); also it may not move users off GPTeal if they pre-process anyway, and the real driver may simply be ease of use (a filter agent could solve that).
- **Kate Lynn:** meet needs inside XFly to keep a reproducible methodology; calls GPTeal/Gemini use shadow AI. Asked for past actionability logs to try a small supervised actionability model (needs Claude Code access). Ted: reviewers do actionability in Excel and only ~1% push it back to XFly; a future Genesis review workflow could capture it. Outcome: continue the discussion; Adi suggests piloting upload.
- **Survey:** nobody has answered the banner survey on the sentiment demo (<1 week live); target the cohorts that actually have demo data (breast, PH), Sarah Saidi's breast oncology team asked to explore by Thursday, before ESMO; Chris O'Brien + Michal to pick users. No more demo datasets.
- **Sampling / driver methods:** Jan's team is comparing 3 ways of computing drivers; Matt to do an offline analysis with Jan on whether Genesis should sample the corpus. Michal: redesigning the filter page is a larger planned initiative.

## Key Developments (Oct 20) -- Genesis weekly + DIA sentiment follow-up (transcripts)

### Genesis Weekly: Drivers Demo, Interviews, Proceed With "Beta" (Oct 20)
- **User interviews (Michal):** 5 scheduled with demo-page visitors (first Oct 20, others Oct 21 and 23). Early feedback positive but confused about "negative drivers" and that the side panel shows **findings, not insights**; plan to show "view original insight" instead of the insight number.
- **Drivers method (Jan):** per-aspect consensus clustering with LLM naming, built from the heatmap's top cells (e.g. negative access, 41 findings), recalculated per filter on the fly, results cached 7 days; claims it's stable. **Matt's feedback:** a fixed subtopic taxonomy would be more consistent and could be pre-processed, since LLM-written drivers can change phrasing; also bring-your-own/emerging topics keep coming up. Jan can switch methods (2-3 available).
- **Adi's concerns:** top negative driver was 16%, sentiment splits near even thirds ("wishy-washy", what can I act on?); ~9 findings per insight looks high (production: **138K insights -> ~900K-1M findings, ~7-8 per insight**) and long sentences get split into near-duplicate findings. Matt: improve visualization (size/height by volume) and conjectured the even split comes from on-the-fly drivers; fewer fixed labels would change it. **Kate Lynn:** the data has no question yet; free-text query is on at launch but not yet wired to SEPs.
- **Decision:** proceed to launch; label it **"Sentiment 2.0 beta"**, educate users that it's a first step; Adi wants lifecycle-specific topics (pre-launch / launch / established) later. Patrick asked for a Friday go/no-go check-in.

### DIA Sentiment Follow-up: n-gram Sanity Check, "The World Is Our Pilot" (Oct 20)
- **Charles Davis (DIA)** showed 1-3 word n-grams consistently positive/negative across three runs of the n=600 sample (e.g. encourage/support/enable positive; barrier/lacked/unequal negative), a sanity check that classification is directionally sensible. Jan: the 600 were an agent-picked "representative" sample, and offered the full ~900K findings for bigger runs.
- **Zach Monge** (also Andy PH call): question the business problem; do structured interviews by product lifecycle stage. Patrick: Michal has done months of interviews; goal now is to start the conversation. Kate Lynn: build an asset-lifecycle framework with topics per stage.
- **Rollout:** to everyone ("the world is our pilot"); Raji worried commercial could see it before validation; Patrick: HH has had Genesis since April and he won't turn access off. **Matt:** the thumbs up/down on findings is a "secret weapon" for an expert answer key, so make it front and center (Jan: feedback will tune prompts/examples, not train models; considering a 30-minute ranking task before access). Changing the extraction methodology later would reset the baseline, another reason for "beta".

## Key Developments (Oct 23) -- Go/No-Go Review (transcript): not a go

### Go/No-Go Review Became a Demo; Decision Slipped (Oct 23)
- **HH sentiment excluded for the first launch** (Patrick, after Brandon + BI team): MRL/VNI only first. Adi worried Sentiment 1.0 is so poor that HH might be better off with 2.0 beta; Jan lightly changed the 1.0 prompt to reduce hallucination. Add "coming soon" for HH in the UI and release notes (Patrick, Oct 26).
- **Not ready:** test environment was still processing a backlog of insights (not refreshed daily like production), so the demo showed driver-generation failures and Matt spotted ~2.5 findings per insight on 163 insights (should be ~8), i.e. incomplete processing. Adi suggested pointing test at production data (Jan agreed to copy production data over). Patrick: no go/no-go until UAT; best case go/no-go Wed or Thu.
- **Process critique (Adi):** last-minute UI changes (banner text, 1.0/2.0 entry dropdown that defaults to 2.0) caused slippage; wants a readiness checklist incl. approvals. Patrick: be careful about "possible features" being heard as commitments.
- **Access issue:** users with mixed HH + MRL groups see "unassigned"; Jan can only add, not remove, security groups (Adi affected). **Admin page preview:** typing "admin" in Genesis opens a settings page (feature flags per group, driver-method switching), Jan-only for now.

## Key Developments (Oct 26-27) -- Genesis weekly (transcript) + UAT Teams threads, screenshots Oct 28

### UAT Starts; Go/No-Go Wednesday; Beta Targets Thursday (Oct 26)
- **Weekly cadence proposal (Jan):** plan Monday / build / demo Friday on top of 4-6 week releases; Patrick wants a mechanism to avoid being surprised and a stronger roadmap; Adi deferred it until after launch. New internal Merck engineer **Kapildev Latchubhukta** joined the Genesis dev team.
- **Demo on test (140K insights, production data, separate copy):** results appear instantly, drivers cluster in <20 s; findings list with like/dislike feedback (feedback doesn't change data); drivers named to line up with the heatmap; **14% of findings land in "Miscellaneous"** (could be noise or emerging topics); heatmap cells are clickable (no AI summary yet); chat still disabled until a quick follow-on release; **Excel export** with tabs for insights, findings, filters, high-level percentages, topics (heatmap), drivers (Adi: "super impressive"). Patrick: always show the filter summary bar.
- **Topics answer needed:** users in almost every interview ask to follow their own topic; Patrick wants a talking point (hierarchical taxonomy; maybe suggest trending topics). Adi: use the dynamic driver mechanism rather than reinventing topics; Jan has experimental level 1/2 subtopics; Gem: do users want sentiment on drivers?
- **Release logistics:** UAT by Adi's team (Ted, Rose, Bijou, Kyle; GxP-free, low criticality so loose process). Release notes + UAT steps are generated by Jan's agent (posted Oct 26: UAT Test Plan Excel + R26.6 PDF). Business + technical approval, then 30-90 min deploy, then documentation. **Plan: pass UAT by Tue, decision Wed Oct 28 call, release Thu Oct 29 (European-morning window).** Patrick out the rest of the week (reachable). Matt asked who does UAT and where the process is documented.
- **Odd UAT finds:** an overlay from a leftover guidance browser extension (transcribed as WalkMe/Guide Me/WhatFix) shows on Kyle's test; Patrick took it to Ops/Christine Ellis's team. Info panel/survey entry missing on test (bug, Michal). Usage tracking of Genesis visitors is now live (finally fixes the HH usage report; 200+ HH users, ~250 max). Prior survey feedback: positive, but the user wasn't confident presenting because the demo data wasn't from their TA. XFly TA table upload still blocked (Ravindra / Steve, data not on the data lake yet).

### Teams UAT Threads (Oct 26-27; screenshots Oct 28)
- **Findings count mismatch (Kyle, UAT step 1.3.5):** 11,190 findings on the dashboard vs 11,286 in the Excel export. Jan: findings with **confidence <0.7 (~100) aren't analyzed** but the export includes them; options are to analyze everything or exclude them from Excel; confidence = how sure the model is of the sentiment, low when a sentence is hard to score. Long-term idea: human-in-the-loop classification of low-confidence findings or an admin view of the full data (Patrick: "an opportunity"). Ted asked where to log issues; Jan: UAT chat is fine, scripts/results at the GENESIS 26.6 location.
- **Matt:** asked how on-rails UAT is (Jan: business-unit responsibility, loosely classified). Suggested "Other -- topic undetermined" for the Undefined category (Patrick asked for a definition like "miscellaneous topics without strong signals"; Jan: it's the bucket when the LLM can't assign one of the predefined topics) and dropping the subtext on "Topic Definitions".
- **Classic Genesis issues (not 2.0):** typo "Last 6 Month" -> "Last 6 Months" (Jan fixing); thumbs up/down on classic chat registers clicks but the color change broke (Jan may just remove them); Ted: no clear way to clear a long standard-prompt text when switching to a custom prompt (Ask Anything button was removed June 30, GNS-1288), Michal proposing helper text "Want a custom prompt? Deselect to edit."; All Insights page sort-by-sentiment has no sentiment indicator (backlog **GNS-1465**).
- **Performance (Jan, Oct 26):** TEST build is ~5x faster on the slowest Filters call, ~2.2x on page load with all data, ~10x lower worst-case facet time, ~9x smaller facet response vs PROD (140K insights).
- **Patrick (Oct 26):** release notes should state MRL access available now, HH coming soon.

## Related Memories

See [[merck-stakeholders]] for full stakeholder map including Genesis-specific people.
