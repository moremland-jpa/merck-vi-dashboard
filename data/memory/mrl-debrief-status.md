---
name: mrl-debrief-status
description: "MRL Debrief -- Priority #1. Met with Destiny. Have sample data from Uri, will use to update prototype. API connection still broken (Merck API migration). SEP integration targeting late Sept/early Oct. As of Sep 2, 2026."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4b881dac-e446-4b63-b338-c9ba1f6228ea
  modified: 2026-09-02T14:45:49.125Z
---

## Current State (Aug 31, 2026)

**Priority #1** in the Congress AI experiment stack (per Aug 20 weekly check-in). Patrick approved as exception to his desire to limit POCs, because Shannon made a strong case it ties into existing deliverables.

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
