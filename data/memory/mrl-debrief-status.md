---
name: mrl-debrief-status
description: "MRL Debrief -- live Congress AI connection working; generation reliability is the open issue (Uri rolling out a server-side normalizer, re-test once live); HR/CI + safety still missing; one-pager + Confluence page delivered Sep 23; SEP retrospective now follows the abstract tiering experiment. As of Sep 23, 2026."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4b881dac-e446-4b63-b338-c9ba1f6228ea
  modified: 2026-09-24T13:27:41.471Z
---

## Current State (Sep 23, 2026)

- **Live connection working:** the JPA engine now talks to Congress AI's debrief endpoint (auth resolved Sep 22). Destiny's original backend source is in hand.
- **Main open issue is generation reliability:** many live calls fail schema validation. Uri diagnosed the causes and is rolling out a server-side normalizer (first deploy attempt on Sep 23 didn't succeed). Re-test the same ASCO abstracts as soon as it's live; that before/after comparison is the most important next check.
- **Data gaps confirmed on successful calls:** hazard ratios and confidence intervals come back empty, and the Congress AI schema has no safety / adverse-event section.
- **ESMO (Oct 23-27):** abstracts mostly have no content yet, which is expected pre-congress. Real ESMO testing waits for content to arrive.
- **Delivered Sep 23:** user-facing one-pager slide for Shannon, and a rewritten Confluence status page.
- **Sequencing:** the SEP retrospective now follows a new abstract tiering experiment (Ante Harxhi, CV) that Shannon wants first (see [[congress-ai-status]]).

Full technical detail (architecture, tests, VDI setup, retry-convergence hypothesis, Uri's exact confirmations) is in [[project-mrl-debrief-engine]]. Check that first when resuming.

## Key Developments (Sep 21-23)

### Live Connection and Auth Resolved (Sep 22)
- Congress AI debrief endpoint works end to end with the access-token cookie as a Bearer token; the earlier "Viewer" role error was a stale token.

### Live Testing Against ASCO 2026 (Sep 22)
- 10-abstract sample: 6 failed schema validation, 4 succeeded. Successes had some real values (event rates, p-values) but no hazard ratio / CI, no safety data, and generic program relevance.
- 500-abstract sample: ~85% failed on the first pass; re-running the same abstracts minutes later gave markedly more successes, pointing to intermittent per-call failures rather than fixed data gaps.

### Destiny's Backend Source Reviewed (Sep 22)
- Production calls come from the browser because Congress AI is only reachable on Merck's network. On any failure the prototype silently falls back to ClinicalTrials.gov data, which likely explains some of the thin output in the August review.

### Uri Working Session (Sep 23)
- Uri confirmed the failure causes (missing sections, empty required fields, phase-label mismatches, one-sided CIs), confirmed whole-section failures are deliberate and the service never invents data, recommended a client-side retry (3 attempts, 5 s apart), and shared the backend schema definition.
- He's rolling out a server-side normalizer to fix the formatting failures at the source.

### ESMO Survey (Sep 23)
- 97.9% of general and 13 of 13 randomized-trial ESMO abstracts failed, and retries didn't help (99 of 100). Expected: ESMO content isn't available until the congress.

### One-Pager and Confluence Page Delivered (Sep 23)
- One-pager slide "MRL Debrief: Leadership-Ready by Morning" for Shannon, plus the rewritten Confluence status page. Shannon had asked for an MRL Debrief one-pager (Teams, Sep 22).

### Technical Catch-up With Uri in This Week's Open Call Slot (Sep 23)
- Shannon and Patrick are out of this week's call; Matt and Uri are using the time to go over MRL Debrief technical findings.

## Action Items (Sep 23)

- **Matt + Uri: Re-test live generation once the normalizer is live** -- same ASCO 500-abstract sample plus the retry test; before/after comparison
- **Uri: Server-side normalizer rollout** -- fixes the formatting causes of the schema-validation failures
- **Matt + Uri: MRL Debrief technical catch-up** -- during this week's open call slot
- **Matt: Report text-encoding issue to Uri** -- character corruption in extracted text (e.g. "HER2" minus sign garbled)
- **Matt: Request an adverse-event section in the Congress AI debrief schema** -- none exists in the backend schema
- **Matt: Client-side resilience if the normalizer falls short** -- retry (3x / 5 s), envelope unwrap, accept partial responses; publication fallback for missing values
- **Matt: Run retry-convergence survey on a fresh ASCO sample** -- quantify how many failures recover on retry
- **Legal: Clear use of Congress AI generated content and PubMed abstract quoting** -- the ENABLE_CONGRESS_AI_CONTENT setting stays off until cleared
- **Team: Decide where the production version runs** -- Congress AI is only reachable inside Merck's network
- **JPA: SEP retrospective on ASCO 2026 content** -- now after the abstract tiering experiment
- ~~**Matt: MRL Debrief one-pager for Shannon**~~ DONE (Sep 23)
- ~~**Matt: Rewrite MRL Debrief Confluence page**~~ DONE (Sep 23)

## Core Purpose and Messaging Notes (Sep 23)

**Delivered Sep 23 (separate from the technical investigation): a user-facing one-pager slide** for Shannon — `MRL Debrief/MRL Debrief - Process One-Pager.pptx`, built via `build_mrl_debrief_onepager.py` (Sandbox/Merck root) on the official Merck V&I theme template. **v1 was rejected as "very light"** — a generic Select→Gather→Draft→Refine→Deliver flow that missed what the debriefs are actually FOR. **v2 (final):** titled "MRL Debrief: Leadership-Ready by Morning," an illustrative overnight timeline (~5 PM talk delivered → ~8 PM draft ready → evening writer review, target ~30 min → overnight leadership pre-read → 6 AM briefing) plus four value cards (Time, Consistency, Coordination, Context). Timeline and the ~30-min figure come from Shannon's own description in the Jul 30 "Prototype introductory session and MRL Debrief" transcript and are labeled illustrative/target on-slide; no invented hours-saved stats. Still zero mention of the 502 bug, ESMO timing, or any blockers — Shannon's ask was "capture what the process is, not document its failings."

**Confluence page rewritten Sep 23:** `MRL Debrief/MRL Debrief Automation - Confluence.md` replaced the stale Aug 7 "handoff to Apex" version with a current status page (purpose, status table, Sep 16 root causes, live-test findings, Uri's confirmations, what the rebuild does, next steps with If successful / If not successful branching). Merck-internal audience, so it's candid about open issues. It's the paste-ready source for Merck's Confluence (Congress AI space); JPA can't edit Confluence directly. Keep it in sync when status changes (e.g., after Uri's normalizer re-test). **Tone rule from Matt:** Uri/EPAM read this page, so don't call out their misfires by name — the normalizer line says "rolling out," not that the first deploy failed. Candid about system issues, diplomatic about people.

**Core purpose of MRL Debrief (don't lose this again — v1 missed it):** per Shannon (Jul 30), an RMSD/MSL is assigned a talk (typically a late-breaker) and owes a debrief to **senior leadership the next morning** (~6 AM meeting). RMSD fills the template → medical writer consolidates into the format leaders want → Executive Director of Scientific Affairs co-presents and fields questions. Formats vary across congresses today; leaders want one consistent format across ASCO/ESMO/etc. Shannon's target state: data ~5 PM, draft in the tool ~8 PM, ~30 min to tailor and approve, leaders pre-read before the room instead of seeing it cold at 6 AM. Value framing = time saved for writers, consistency, coordinated handoffs, informed leaders. Source transcript: `transcripts/Congress AI_ Prototype introductory session and MRL Debrief 2026 07 30.docx`.

## Current State (Sep 18, 2026) — Engine built, live Congress Library test blocked on Uri

Moved from analysis (Sep 16) to a working engine rebuild, tested on both the dev machine and the Merck VDI (33/33 tests passing on both), pushed to `github.com/moremland-jpa/merck-mrl-debrief-engine`. Live-testing against the real Congress Library API on Sep 18 confirmed auth works for read (GET) endpoints, found the real ESMO 2026 congress_id, but hit a wall on the one endpoint that matters most: `POST /api/debrief/generate` returns a CSRF error Uri's original instructions didn't cover. A question was sent to Uri Sep 18; **next session should check for his reply first** — that answer determines whether the Congress Library schema migration actually closed the Results/safety gap this whole analysis is about.

**Why work on the codebase now (Matt, Sep 16 team-update note):** still blocked on the Databricks compute resource ticket, so the actual Congress Library API reconnection is on hold. In the meantime, using raw sample data Uri already provided to build/test code against, plus leaning on external sources (CT.gov, per the enrichment path found the same day) to improve fields and layout ahead of the live reconnection.

Also installed Node.js locally and on the VDI (portable, added to PATH). `Merck/CLAUDE.md` updated to reflect this (Sep 24).

## Current State (Sep 16, 2026) — Root cause analysis update delivered

Compared all 6 of Destiny's prototype ASCO 2026 debrief decks against the corresponding sections of the 3 real "MASTER FILE" writeup decks, abstract by abstract. Also read the prototype's surviving repo code (backend Azure Functions code is missing, only frontend/schema/docs survive) and Uri's Sep 14 Teams screenshot showing the actual API call shape. Delivered a new doc: `MRL Debrief/MRL Debrief Automation - Root Cause Analysis and Path to Parity (Update Sep 2026).docx`, extending the Aug 7 one-pager.

**Four confirmed root causes (replacing the single "CT.gov as sole source" framing):**
1. Results are endpoint names only, no values (HR/CI/p-value/ORR) — verified the data schema (`full_clinical_schema`) already fully supports these fields, so the bottleneck is the upstream Congress Library data being too thin, not the schema/template. Testable once the ~3→~20 column migration (see [[congress-ai-status]]) is confirmed live.
2. Safety/AE data has nowhere to go — verified directly by reading the schema: no adverse-event/TRAE/safety object exists anywhere in it. This is a required schema addition, not just a data-sourcing fix.
3. Late-breaking abstracts fail almost completely (2 of 6 — LBA4, LBA5 — were near-total "Unknown" stubs) despite being the two richest real writeups in the set — a timing/coverage failure, not a logic bug.
4. No competitive/strategic layer anywhere (no named comparator trials, no named Merck assets like MK-2010/MK-2750/MK-3120/MK-4716) — this requires institutional judgment no external source has; recommended to stay human-authored with AI-assisted research, not fully automated.

Also flagged unresolved: 3 conflicting descriptions of the auth model (env-var tokens vs. user-pasted bearer token vs. Uri's header-only `x-user-id`/`x-user-role` scheme) and 2 conflicting descriptions of the delivery mechanism (base64 download vs. SharePoint webUrl) — need reconciliation with Uri/EPAM/Destiny before reconnection work proceeds. Core backend files (`functionApp.js`, `debriefPipeline.js`, 6 slide files, `congressAuth.js`, `powerAutomate.js`) are missing from the repo and need to come from Destiny/Merck IT.

Recommended phasing (scoped strictly around the two unresolved legal blockers — congress-content AI rights, and the Sightline/Pharma Projects addendum): verify new schema + reconcile auth (now–Sep 19) → reconnect/validate + ship low-effort completeness-flag/"Not yet reported" wins as the Sept 30 wrap (not feature-complete) → SEP retrospective as offline test (early Oct) → human-reviewed (not self-serve) late-breaking upload path, since prior usability testing showed most RMSDs struggle with basic upload workflows (mid-late Oct) → ESMO live test (late Oct).

**Live CT.gov check + new enrichment path found (Sep 16).** Queried the live ClinicalTrials.gov API for all 6 ASCO comparison trials: none has a posted resultsSection even 3+ months post-congress (all still active/recruiting, completion dates 2027-2031) — confirms CT.gov's own Results module is not a viable near-term source for this trial class. But CT.gov's auto-linked PubMed citations already pointed to full journal publications for the two worst-performing abstracts (LBA4→Lancet, LBA5→NEJM), both epubbed May 31, 2026 — the day before the June 1 ASCO presentation, not months later. Pulled both abstracts via NIH's free E-utilities API; they contain the same HRs/CIs/AE rates as the real decks, matching almost verbatim. This is a live-usable technique (check CT.gov's linked-publication metadata at generation time), not a retrospective one — simultaneous journal publication is a known convention specifically for late-breaking/plenary-tier readouts, i.e. exactly the sub-category where the prototype fails worst. Doesn't help the other 4 (non-LBA) abstracts, which had no linked publication. One flagged caveat: at least one publisher (Elsevier/Lancet) attaches a copyright notice reserving AI-training/TDM rights — a different legal question than the congress-content contract issue, lower risk, but worth a quick legal check before wiring into a live pipeline. Folded into the updated Findings doc as new Section 3.6.

**Important framing correction from Matt (Sep 16):** the 6 ASCO abstracts are historical benchmarks for validating approach, not live abstracts needing fixes — don't confuse "found a new source" with "let's go update these old decks." Also: success bar is NOT 100% automation — if the tool fully replaced a medical writer's judgment there'd be no need for one. Goal is getting the AI draft as close as possible (content + formatting) so the medical writer's actual writing job is faster/easier — a co-pilot framing, not a replacement one. Apply this bar to all future recommendations for this workstream.

## Current State (Sep 10, 2026)

**API fix is now concrete and scoped.** Per Uri (via Shannon, Sep 10 weekly check-in), reconnecting isn't a big deal -- Matt just needs a meeting with EPAM to get access to the backend tunnel into the **Congress Library tables** (the same ones Destiny's prototype pulled from). Root cause of the break: Congress Library went through a major schema transformation since ASCO (~3 columns → ~20 columns); EPAM is finishing testing, expected ready **end of week ~Sep 11-12**. Matt is not blocked on his own environment setup -- this connects directly to Destiny's existing work via EPAM.

**Sequencing confirmed (Talia + Shannon, Sep 10):** MRL Debrief targeted to wrap by **end of September**, ahead of the SEP retrospective which picks up **early October**. SEP materials (ASCO 2026 samples) are already sitting in the "ASCO 2026 folder" per Shannon -- no new collection needed, just capacity.

**Databricks as a dev environment:** Matt's Databricks access (see [[genesis-status]] for the compute-resource hurdle) can double as a code environment for the MRL Debrief prototyping work -- point it at a data folder as the source, useful once the API/tables are reconnected.

## Current State (Sep 4, 2026)

**Priority #1** in the Congress AI experiment stack (per Aug 20 weekly check-in). Patrick approved as exception to his desire to limit POCs, because Shannon made a strong case it ties into existing deliverables.

**"Waiting in the wings" (Sep 3 weekly check-in).** Talia confirmed MRL Debrief and SEP integration will pick up as digital planning goes back to EPAM for development and execution. Not actively in sprint right now -- focus is on ESMO demo roadshow.

**Met with Destiny** (completed). Software request submitted. Technical need is light.

**API connection to abstract library broke.** Root cause: Merck migrating to new centralized API platform. Migration in progress, no firm completion date. Underlying Kong API still works. Matt + Rita/Uri to troubleshoot; if portal migration is the blocker, wait.

**Have sample data from Uri** -- will use this to update the prototype in the meantime while API is down.

**Goal: On-site ESMO prototype.** JPA leading, working prototype for Shannon to demo at ESMO for leader feedback.

## SEP Integration Experiment (Priority #3)

Targeting late September / early October (Q4). Shannon described as a traditional 30-day retrospective POC: take 5 abstract samples with SEPs (a couple from each tumor type), run through summarization/LLM prompts, see what happens. Expected ~2 weeks, not full-time.

## CI Database (Priority #2)

Fields of interest identified. Adam Canigiani is the contact. Jakub (RWDE) suggested waiting until end of September when data syncs to Databricks, rather than dealing with Immuta licenses and RWDE training. Matt to discuss with Adam and Jakub. API call data (free text) may be separate from local access.

## What the Assessment Found

**Working:** Correct trial identification, strong study design capture, readable summaries (no hallucination), directionally accurate efficacy/safety.

**Missing:** Exact efficacy metrics (OS, PFS, ORR, DOR, HRs, grade 3+ AEs), safety detail, subgroup/biomarker nuance, interpretation/"so what" layer.

**Root cause:** ClinicalTrials.gov as sole data source.

## Original Three Recommendations (Aug 7)

1. **Integrate SEPs** for strategic framing (Preamble/Key Implications typically from unrecorded MRL Debrief discussion)
2. **Enable end-user content upload** from field (photos, slides, notes)
3. **Enrich source layer** beyond ClinicalTrials.gov (abstracts, posters, publications, press releases, internal archives)

## Technical Context

Destiny Miller's prototype: JavaScript (PowerPointGenJS + Automizer), Azure Functions, React/SharePoint. Pulls from ClinicalTrials.gov + Congress AI API. The 5-slide debrief template is a data collection point for medical writers, not a direct output.

## Preamble/KI Gap

Preamble and Key Implications built from unrecorded MRL Debrief discussion, scribed by med writer. Rita less certain Citeline data will improve preambles (more Merck-specific strategic assessments than data-detail-driven).

## Related Memories

See [[congress-ai-status]] for the broader Congress AI context this sits within.
