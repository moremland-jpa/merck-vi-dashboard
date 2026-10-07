---
name: mrl-debrief-status
description: "MRL Debrief -- reliability solved (Uri normalizer, zero 502s Sep 24); draft format rebuilt to match medical writers' decks with selectable sections; tool is a next-morning debrief of a talk already given, built from RMSD screenshots on the fly (confirmed from transcripts); waiting on Uri re capture intake + safety section and on data rights; one-pager v3 + Confluence updated Sep 24; Sep 28 update: Matt wants an individual meeting with Shannon to review progress, Sep 25 ESMO data may make testing more robust. Oct 5: demo done with Shannon; her feedback = writeups have a multi-row comparable-studies table, so a CT.gov comparator finder was built and pushed (bbea580). Oct 6: demo server now pulls LIVE Congress Library data on the VDI (static dev token, Node TLS-cert fix); Matt asking Jan where to host it for Shannon's team; Confluence page updated to Oct 6. As of Oct 6, 2026."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4b881dac-e446-4b63-b338-c9ba1f6228ea
  modified: 2026-10-07T15:49:33.221Z
---

## Current State (Oct 7, 2026) -- read this first

**Technical status**
- **Hosting handoff to Jan (Oct 7):** Jan Chmelar has the MRL Debrief repo plus all tokens and credentials needed to stage via AWS on the Merck side. This should give live access to the Congress Library and let anyone with the link (e.g. Shannon) use it. **Still waiting on final deploy as of Oct 7.**
- **Matt to show latest demo to Shannon on Oct 12.**
- **Live demo working (Oct 6):** Matt confirmed the demo server pulls live ASCO abstracts from Congress Library on the VDI and builds writeup drafts (congress/abstract picker, section toggles, cached samples as fallback). Congress AI moved to a static dev token, so no more cookie/token refreshing. Node needed the Merck TLS-inspection root cert (`scripts/export-root-ca.ps1` + `NODE_EXTRA_CA_CERTS`). Errors such as "no content yet" show as a large red banner.
- **Comparator table (Oct 5-6):** Shannon's demo feedback was that real writeups carry a multi-row comparable-studies table. A rule-based ClinicalTrials.gov finder now pre-fills candidate trials (identity, regimen, population, N, primary endpoint name, linked reference); result numbers stay a writer prompt. No LLM; comparator rows are copied from CT.gov records. Worked well for HARMONi-6, weaker for aspirin/CRC.
- **Capture intake: Shannon's answer (Teams, Sep 28-29):** screenshot parsing runs through the **abstract library like any poster/presentation**, not through a separate MRL Debrief process. At ESMO Shannon will upload the captures herself; eventually the assigned person uploads, same as abstract write-ups. She wants a **%-accuracy measure** for correct data representation and asked what Uri support Matt had in mind (the experiment was kept separate from the dev team except reconnecting Destiny's debrief generator to Congress AI). Matt framed two pieces to finalize with Shannon + Uri: (1) the connection works but is not automated or permanent (the static token since Oct 1 helps), (2) screenshot parsing needing EPAM. Matt floated that MRL Debrief might be an extra step inside the write-up workflow (generating the write-up also creates the debrief slides) rather than a separate workstream. Outcome of the Sep 29 call is not recorded in the transcripts.
- **Reliability solved:** Uri's normalizer is live. 100 ASCO abstracts: 89 x 200 on the first call, 11 x 422 (no content), **zero 502s** (was 50-85%). HR in 17%, full CI in 24% of the 200s (Sep 22: 0/4). The earlier "encoding bug" was our own PowerShell capture, not Congress AI (closed).
- **Draft format rebuilt to match the medical writers' ASCO 2026 master files** (`MRL Debrief/actual writeups/`), with selectable sections, in the engine (`layout: 'writeup'`). Sample: `mrl-debrief-engine/local-samples/LBA3508_writeup.pptx`. Detail in [[project-mrl-debrief-engine]].
- **Remaining gaps:** no safety/AE section in the Congress AI schema; deployment location + sign-in for users (today a shared static dev token; needs a storage and access plan on a shared host).

**How the tool is actually used (confirmed from transcripts, Sep 24)**
- It's a **next-morning debrief of an assigned talk that already happened**, not a pre-talk "what to go see" briefing. Matt asked about the pre-talk idea; the transcripts don't support it. Citations: Shannon, Jul 30 MRL Debrief session 12:27 (assigned the talk, debrief "for the senior leaders the next morning") and 36:18 (info at 5, in the tool by 8, leaders pre-read); Shannon, Aug 12 EPAM Ways of Working 14:06 ("this data won't come available until that day"; depends on whoever is assigned "taken screenshots"). "What to go see today" belongs to the Congress AI Digital Planning side.
- Pre-talk pieces that do exist: the early-September planning calls pick which abstracts become debriefs vs write-ups (Round 2 Digital Planning interview); some content may be in Congress AI if the poster/presentation was uploaded the night before (Jul 30, 21:31), so Background/Methods could be pre-built with results added after the talk (idea worth raising with Shannon).
- **Sep 24 call (no transcript in `transcripts/`; newest is Sep 16; from Matt's verbal report):** Shannon wants it used on the fly at the congress. Source = RMSD screenshots, so a 422 is the normal state for same-day late-breakers. Envisioned flow: RMSD uploads captures, checks/unchecks sections (she said this Jul 30 42:16 and Aug 12 too), generates, writer reviews.
- **Who processes the captures (open, waiting on Uri):** (a) Uri/EPAM ingest them and we consume the same `debrief/generate` output (preferred; Congress AI already lists "poster, slide text, enhancements" as sources and has `poster_enhanced`/`poster_filename` fields), or (b) we process them ourselves (needs GPTeal access inside Merck's network + legal, breaks the engine's no-LLM design). Destiny's code does no screenshot processing (JSON input only; `parseMultipart.js` is unused dead code).
- **Data-rights flag:** the Jul 8 constraint (contracts allow screenshots, no AI rights for automation) applies directly to AI-processing RMSD captures. Needs Shannon's escalation answered before building either option.
- **Usability tension:** earlier field testing found upload workflows are a struggle for many RMSDs; the capture step must be very light (phone photos) or supported.

**Deliverables current as of Oct 6:** one-pager v3 (`MRL Debrief/MRL Debrief - Process One-Pager.pptx`, Sep 24; does not mention the comparator table or live demo), Confluence page (`MRL Debrief/MRL Debrief Automation - Confluence.md`, updated Oct 6, paste-ready, Matt pastes it into Confluence), engine at `06c0af7`+ on GitHub (`10044a2` added the root-cert script).

Full technical detail (architecture, tests, VDI setup, scripts, Uri's confirmations) is in [[project-mrl-debrief-engine]].

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

## Key Developments (Sep 28, dashboard team update, Molly)

- **Matt has made progress understanding the current state** of the engine/workstream; wants to schedule an individual meeting with Shannon to go over it in more detail.
- **ESMO data updates land Sep 25** (per congress-ai-status.md's data-drop item) -- may make Matt's MRL Debrief testing more robust once that content is available.

## Key Developments (Sep 28-29, Shannon Teams on screenshot parsing)

- **Shannon (Sep 28 8:56 AM), replying to Matt's Sep 25 note:** the summary slide looks great; screenshot-parsing data will run through the abstract library just like any poster/presentation, not through the MRL Debrief process separately. She wants to see **%accuracy for correct data representation**, and asked what Matt had in mind for Uri to support, since the experiment was intentionally kept separate from the dev team beyond reconnecting the broken link between Destiny's debrief generator and Congress AI. She is also receiving the ESMO planner raw data soon.
- **Matt (Sep 28 12:04 PM):** two pieces to finalize with Shannon and Uri: (1) the connection isn't exactly broken but isn't automated (no permanent connection for pinging the library), (2) screenshot parsing is the big one; the tech works for the write-up workflow, so a similar widget would be built into her script, and that piece needs EPAM support.
- **Shannon (12:17 PM):** (1) will the connection suffice for ESMO? It is an experiment, permanence can be decided later. (2) Screenshots can be uploaded to the abstract library and then reflected in the abstract summary; is a separate upload widget needed? At ESMO she will be the one uploading. Eventually the MRL Debrief uses the same workflow as abstract write-ups, with the assigned person uploading content.
- **Matt (1:30 PM):** discuss Sep 29; can demo how he envisions it with real data, and clarify the difference between the write-up workflow and MRL Debrief, possibly just an extra step in the write-up workflow (generating the write-up also creates the debrief slides).
- **Implications:** preferred intake option (a) from the Sep 24 notes (Uri/EPAM ingest, we consume the same `debrief/generate` output) is now Shannon's stated model; the permanent-connection gap is largely addressed by the static dev token (Oct 1); a measurable accuracy check is now expected; and Matt's framing of MRL Debrief as a step within the write-up workflow is on the table.

## Key Developments (Oct 5, demo feedback from Shannon)

- **Matt demoed the engine (section-toggle demo) to Shannon.** Her feedback: the real writeups contain a table of comparable results from related studies; ours generated only one row. She asked whether related studies could be identified, at least enough to get the rows even if the table can't be fully filled.
- **Built and pushed (`bbea580`, checklist `74a9d2b`):** a deterministic ClinicalTrials.gov comparator finder (same drug / same control, Phase 3, citable reference required). Pre-fills trial, regimen, population, N, primary endpoint name and reference; result numbers stay a writer prompt. Demo server has an "Auto-identify comparator trials" checkbox (needs internet). It surfaced RATIONALE-307 and HARMONi-A for HARMONi-6, both comparators the writers used; weaker for aspirin/CRC. Detail in [[project-mrl-comparator-finder]].
- **Partially answers root cause #4** (no competitive layer): candidate trials can now be auto-suggested, but selecting them and filling results still needs writer/CI judgment, and the writers' tables include subpopulation columns and trials registry search won't find.
- **Not yet shown to Shannon:** the finder's output itself. Ask which trials writers actually cite and whether CI databases could supply result numbers (fits the data-rights workaround).

## Key Developments (Oct 6, live data and hosting)

- **Live Congress Library data in the demo, working on the VDI (`ae5ed9c`).** Congress + abstract picker, `POST /api/debrief/generate`, CT.gov/PubMed enrichment, section toggles; cached LBA4/LBA3508 samples remain as the offline fallback. Matt confirmed it loads live ASCO data.
- **Static dev token.** Olca (Congress AI) moved the Debrief API to a static token kept in 1Password, so there is no more cookie grabbing or refreshing. Matt saved it as user env var `MRL_DEBRIEF_ACCESS_TOKEN`; live mode also needs `CONGRESS_USER_ID` and `ENABLE_CONGRESS_AI_CONTENT=true` (the legal gate, set by Matt himself; legal still unresolved).
- **Node vs. Merck TLS inspection.** Node's `fetch` failed with `SELF_SIGNED_CERT_IN_CHAIN` (curl and browsers were fine); VDI Node is v20.20.2 (no `--use-system-ca`), fixed with `scripts/export-root-ca.ps1` + `NODE_EXTRA_CA_CERTS`.
- **All diagnostic scripts fixed for UTF-8** (`scripts/lib-utf8.ps1`, `11ac609`); anything captured before Oct 6 may contain mojibake.
- **Jan = Jan Chmelar** (Genesis dev business owner, has system access, helped with Databricks access). Matt confirmed Oct 6 that "Jan" means him; Matt does not know Jan Feltman.
- **Hosting question.** The code is now on Merck GitHub (merck-gen/cdds-ese-mrl-debrief, internal repo, pushed Oct 6 over SSH) but that alone does not let Shannon run it (she would need Node, a clone, token, cert fix). Matt is asking Jan where a small web app can run inside Merck's network for roughly 10-20 users; options noted: internal VM/app platform, Databricks, or EPAM building it into Congress AI. Details and the message sent in [[project-mrl-debrief-engine]].
- **Shannon's Sep 28-29 capture-intake answer and the %-accuracy ask** are reflected on the Confluence page (status table row, Next steps 2 and 2a).
- **Confluence page updated to Oct 6** (`MRL Debrief/MRL Debrief Automation - Confluence.md`) for Matt to paste.

## Next Steps / Action Items (Oct 6)

- **Matt: ask Jan Chmelar where the tool can be hosted inside Merck's network** -- internal VM/app platform, Databricks, or EPAM adding it to Congress AI; also approval path and token storage/sign-in. Fallback: Matt generates drafts on request from his VDI during ESMO.
- ~~**Matt: put the engine repo on Merck GitHub**~~ DONE (pushed Oct 6 to merck-gen/cdds-ese-mrl-debrief; prerequisite for IT hosting, but GitHub alone does not make it usable for Shannon)
- **Matt: paste the Oct 6 Confluence page** -- file is ready in `MRL Debrief/`.
- **Matt: show Shannon the comparator table output** -- ask which trials writers actually cite and whether CI databases could supply the result numbers.
- **JPA: comparator follow-ups** -- wire the finder into `generateDebrief` and the build route; add result numbers via the cited abstract (verbatim) or CI databases; confirm CT.gov search stays reachable from a hosted environment.
- **Matt: propose an accuracy measure to Shannon** -- she asked for %accuracy of correct data representation on capture-derived drafts; define how it is scored (e.g. fields correct against the writers' final deck) before ESMO.
- **Waiting on Uri** (Shannon's Sep 28-29 answer: captures go through the abstract library like posters, uploaded by Shannon at ESMO; still open: what Uri/EPAM support is needed, upload-to-draft latency, phone photos OK?). **Plus:** can a safety/AE section be added to the output? **Plus (minor):** his normalizer writes an unvalidated CI into `notes` as a Python dict (6/102 endpoints; we strip it).
- **Shannon: data-rights answer** for AI processing of captures (via Congress Excellence Workgroup).
- **Matt -> Shannon (drafted but not yet sent, offered):** send the LBA3508 writeup + one-pager v3; ask for format review with a medical writer, which sections are on by default, how the Presenter / PDT-EDT Partner fields get filled (engine assumes rmsd_presenter / mrl_discussant); flag the data-rights point and the upload-usability tension.
- **ESMO (Oct 23-27) pilot:** a few assigned late-breakers, captures in, drafts out, writers time their review. Needs the Uri answers + data rights by early October; otherwise fall back to drafts from abstract content + same-day publications, with writers adding figures/numbers.
- **Needed for any live use by others:** decide where it runs inside Merck's network and how users sign in (the shared static dev token no longer expires, but needs a storage/access plan on a shared host).
- **Engine follow-ups:** filter/flag empty 200s from industry symposia (ESMO Pfizer example); consider pre-building Background/Methods before the talk.
- **Legal:** ENABLE_CONGRESS_AI_CONTENT (off until cleared); PubMed abstract quoting.
- **JPA: SEP retrospective** -- after the abstract tiering experiment.
- ~~Re-test after normalizer~~ DONE Sep 24 (zero 502s). ~~Report encoding bug~~ moot (ours). ~~Client-side resilience layer~~ moot for 502s. ~~One-pager / Confluence~~ updated Sep 24.

## Core Purpose and Messaging Notes (Sep 23)

**Delivered Sep 23 (separate from the technical investigation): a user-facing one-pager slide** for Shannon — `MRL Debrief/MRL Debrief - Process One-Pager.pptx`, built via `build_mrl_debrief_onepager.py` (Sandbox/Merck root) on the official Merck V&I theme template. **v1 was rejected as "very light"** — a generic Select→Gather→Draft→Refine→Deliver flow that missed what the debriefs are actually FOR. **v2 (final):** titled "MRL Debrief: Leadership-Ready by Morning," an illustrative overnight timeline (~5 PM talk delivered → ~8 PM draft ready → evening writer review, target ~30 min → overnight leadership pre-read → 6 AM briefing) plus four value cards (Time, Consistency, Coordination, Context). Timeline and the ~30-min figure come from Shannon's own description in the Jul 30 "Prototype introductory session and MRL Debrief" transcript and are labeled illustrative/target on-slide; no invented hours-saved stats. Still zero mention of the 502 bug, ESMO timing, or any blockers — Shannon's ask was "capture what the process is, not document its failings."

**One-pager v3 (Sep 24), after Shannon's on-the-fly reframe:** same title, timeline, and four value cards, but stage 1 now says the RMSD uploads captures of key slides (not "already in Congress AI"), stage 2 says the RMSD chooses what the writeup covers and then generates, and stage 3 is add competitive context + program relevance, then approve. Also added a row of section "chips" (8 checked, 2 unchecked, labelled "Example: sections an RMSD selects for one writeup") that mirrors the engine's WRITEUP_SECTIONS. CONSISTENCY card now reads "Drafts follow the debrief format medical writers already use". Sep 23 version backed up in the session scratchpad only.

**Confluence page updated Sep 24:** now reflects zero schema-validation failures after the normalizer (ASCO 89/100 first-call success, 11 no-content), HR/CI improvement, the encoding issue corrected as JPA-side, Shannon's on-the-fly reframe (RMSD captures + section selection), the writeup format, and new next steps (intake route with Uri, data rights, safety section, format review, ESMO pilot with a fallback, SEP after tiering). It keeps the earlier usability finding that upload workflows are hard for many RMSDs, since that sits in tension with self-upload.

**Confluence page rewritten Sep 23:** `MRL Debrief/MRL Debrief Automation - Confluence.md` replaced the stale Aug 7 "handoff to Apex" version with a current status page (purpose, status table, Sep 16 root causes, live-test findings, Uri's confirmations, what the rebuild does, next steps with If successful / If not successful branching). Merck-internal audience, so it's candid about open issues. It's the paste-ready source for Merck's Confluence (Congress AI space); JPA can't edit Confluence directly. Keep it in sync when status changes (e.g., after Uri's normalizer re-test). **Tone rule from Matt:** Uri/EPAM read this page, so don't call out their misfires by name — the normalizer line says "rolling out," not that the first deploy failed. Candid about system issues, diplomatic about people.

**Core purpose of MRL Debrief (don't lose this again — v1 missed it):** per Shannon (Jul 30), an RMSD/MSL is assigned a talk (typically a late-breaker) and owes a debrief to **senior leadership the next morning** (~6 AM meeting). RMSD fills the template → medical writer consolidates into the format leaders want → Executive Director of Scientific Affairs co-presents and fields questions. Formats vary across congresses today; leaders want one consistent format across ASCO/ESMO/etc. Shannon's target state: data ~5 PM, draft in the tool ~8 PM, ~30 min to tailor and approve, leaders pre-read before the room instead of seeing it cold at 6 AM. Value framing = time saved for writers, consistency, coordinated handoffs, informed leaders. Source transcript: `transcripts/Congress AI_ Prototype introductory session and MRL Debrief 2026 07 30.docx`.

## History: Sep 18, 2026 (superseded) — Engine built, live Congress Library test blocked on Uri

Moved from analysis (Sep 16) to a working engine rebuild, tested on both the dev machine and the Merck VDI (33/33 tests passing on both), pushed to `github.com/moremland-jpa/merck-mrl-debrief-engine`. Live-testing against the real Congress Library API on Sep 18 confirmed auth works for read (GET) endpoints, found the real ESMO 2026 congress_id, but hit a wall on the one endpoint that matters most: `POST /api/debrief/generate` returns a CSRF error Uri's original instructions didn't cover. A question was sent to Uri Sep 18; **next session should check for his reply first** — that answer determines whether the Congress Library schema migration actually closed the Results/safety gap this whole analysis is about.

**Why work on the codebase now (Matt, Sep 16 team-update note):** still blocked on the Databricks compute resource ticket, so the actual Congress Library API reconnection is on hold. In the meantime, using raw sample data Uri already provided to build/test code against, plus leaning on external sources (CT.gov, per the enrichment path found the same day) to improve fields and layout ahead of the live reconnection.

Also installed Node.js locally and on the VDI (portable, added to PATH). `Merck/CLAUDE.md` updated to reflect this (Sep 24).

## History: Sep 16, 2026 (superseded) — Root cause analysis update delivered

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

## History: Sep 10, 2026 (superseded)

**API fix is now concrete and scoped.** Per Uri (via Shannon, Sep 10 weekly check-in), reconnecting isn't a big deal -- Matt just needs a meeting with EPAM to get access to the backend tunnel into the **Congress Library tables** (the same ones Destiny's prototype pulled from). Root cause of the break: Congress Library went through a major schema transformation since ASCO (~3 columns → ~20 columns); EPAM is finishing testing, expected ready **end of week ~Sep 11-12**. Matt is not blocked on his own environment setup -- this connects directly to Destiny's existing work via EPAM.

**Sequencing confirmed (Talia + Shannon, Sep 10):** MRL Debrief targeted to wrap by **end of September**, ahead of the SEP retrospective which picks up **early October**. SEP materials (ASCO 2026 samples) are already sitting in the "ASCO 2026 folder" per Shannon -- no new collection needed, just capacity.

**Databricks as a dev environment:** Matt's Databricks access (see [[genesis-status]] for the compute-resource hurdle) can double as a code environment for the MRL Debrief prototyping work -- point it at a data folder as the source, useful once the API/tables are reconnected.

## History: Sep 4, 2026 (superseded)

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
