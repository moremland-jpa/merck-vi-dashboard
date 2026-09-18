---
name: mrl-debrief-status
description: "MRL Debrief -- API reconnection is now a concrete, scoped fix (direct EPAM meeting, Congress Library schema finishing testing ~Sep 11-12). Sequencing: wrap by end of Sept, SEP retrospective picks up early Oct. As of Sep 10, 2026."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4b881dac-e446-4b63-b338-c9ba1f6228ea
  modified: 2026-09-18T13:40:26.657Z
---

## Current State (Sep 16, 2026, later) — Engine build started

Moved from analysis to implementation same day. Built a clean backend rebuild ("mrl-debrief-engine") at `Merck/MRL Debrief/mrl-debrief-engine/` — full details, architecture, test status, and critically the **git/GitHub push status** (as of session end: committed locally, remote not yet pushed, waiting on Matt to create the GitHub repo) are in [[project-mrl-debrief-engine]]. Check that memory first when resuming this workstream — it has the concrete "what to do next" list.

**Why work on the codebase now (Matt, Sep 16 team-update note):** still blocked on the Databricks compute resource ticket, so the actual Congress Library API reconnection is on hold. In the meantime, using raw sample data Uri already provided to build/test code against, plus leaning on external sources (CT.gov, per the enrichment path found the same day) to improve fields and layout ahead of the live reconnection.

Also installed Node.js locally (portable, added to PATH) — the Sandbox-wide `Merck/CLAUDE.md` still says "No Node.js on this machine," which is now stale.

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

## Three Recommendations

1. **Integrate SEPs** for strategic framing (Preamble/Key Implications typically from unrecorded MRL Debrief discussion)
2. **Enable end-user content upload** from field (photos, slides, notes)
3. **Enrich source layer** beyond ClinicalTrials.gov (abstracts, posters, publications, press releases, internal archives)

## Technical Context

Destiny Miller's prototype: JavaScript (PowerPointGenJS + Automizer), Azure Functions, React/SharePoint. Pulls from ClinicalTrials.gov + Congress AI API. The 5-slide debrief template is a data collection point for medical writers, not a direct output.

## Preamble/KI Gap

Preamble and Key Implications built from unrecorded MRL Debrief discussion, scribed by med writer. Rita less certain Citeline data will improve preambles (more Merck-specific strategic assessments than data-detail-driven).

## Related Memories

See [[congress-ai-status]] for the broader Congress AI context this sits within.
