---
name: congress-ai-status
description: "Congress AI -- Citeline mirror dead end (Greg Bryman); Congress Excellence 100+ activities inventoried; Linda Kollmar governance meeting Sep 12; serial wizard; demo Sep 17. As of Sep 11, 2026."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4b881dac-e446-4b63-b338-c9ba1f6228ea
  modified: 2026-09-11T17:12:21.122Z
---

## Current State (Aug 31, 2026)

**Target:** ESMO (late October 2026) as first scaled execution. AHA two weeks after ESMO -- tentative commitment to go live with CV team.

**Shannon's Priority Stack (Jul 27, confirmed through Aug):**
1. Write-Up workflow with Assignments link (foundation mostly built; need assignments tab on left side)
2. Abstract Library (Larvol data uploaded, sortable/queryable/filterable)
3. Personal + team tags; agreement markers (most important tag = Congress Planner tag for Write-Up/Debrief assignment)
4. Comprehensive Congress Summary / AI-first draft (3 sections: CI abstracts, company abstracts, full report)
5. Report readership tracking (Shannon convinced Congress Ops to pilot digital links at ESMO)

**Explicitly deprioritized:** Role-based comments (SKIP FOR NOW), AI prioritization/historical context (nice-to-have, pairs with CI database), role-based comments with author/timestamp

**Three ESMO Must-Haves (Shannon Jul 27):**
1. Abstract Library with updated Larvol, sort/query, tagging for Write-Up, assignment cascading
2. Write-Ups reviewed by MSL & PDT, finalized within Congress AI interface
3. Comprehensive Congress Summary drafted once CI + company abstract write-ups complete; EDSAs give go/no-go on AI first draft for 2026

## Key Developments (Aug)

- **Apex AI rejection (Aug 12):** Evaluated but criteria (enterprise repeatability) didn't match exploratory nature. All use cases returned. Shannon views it as a "blessing in disguise."
- **MRL Debrief: JPA leading on-site prototype (Aug 14):** Not currently viable for Apex to work with them per update from Jan Feltman. JPA back in the hot seat -- goal is to have a prototype available on-site at ESMO for Shannon to show leaders for feedback both real-time and post-event. See [[mrl-debrief-status]].
- **Peter Baumeister / ACE team (Aug 13-14):** V&I Data Lake lead, 30 data scientists (ACE team). Already sync Citeline data to datalake. Scheduling follow-up between ACE and Greg Bryman's team. Working on API access to Northern Lights and Larvol (Jeff Jamer).
- **Assignment workflow in dev (Aug 12):** EPAM has it visible in dev environment. Rita demoed assignment flow, wrong-assignment rejection, AI relevance validation.
- **Congress Excellence recognition (Aug 13-14):** Shannon spoke with Mladen (Ph I excellence portion of Congress Work Group) and Abiola (PM for Melissa Mimms & Miguel) about the abstract library. Abiola requested one slide explaining current process and vision for abstract library as a reusable knowledge asset / how to start using for different types of reporting once in place.
- **Critical demos coming:** Amar Mesic / MRL IT demo Monday Aug 18 (High Importance). Mladen & Abiola follow-up Tuesday Aug 19 (need slide). ESMO core planning team demos Sep 1 (JPA to cover -- Shannon on vacation) and Sep 15. Core ESMO planning deck already includes one of JPA's slides.
- **AHA parallel deployment (Aug 10):** Same features rolling to AHA alongside ESMO. CVRG data feed identified as earlier source than Larvol for AHA. Medical writers won't know about digital workflow initially (bridge via email export).
- **Larvol freeze:** No extract updates until LBAs release (September). CI team hasn't requested API access from Larvol, though capability exists.
- **Shannon vacation Aug 26 through day after Labor Day (Sep 8).** JPA to cover Sep 1 demo/training.
- **Asset reporting resurfaced (Aug 14):** SAC TMT vs. specific tumor type use case. Slated for future experiment pipeline. Northern Lights has a Beta deep research module Shannon has access to -- she did a 1-pass research on SAC-TMT, shared with Josephine a month ago ("they loved it"). Would repeat for priority assets. Shannon to share research plan, JPA can help update.
- **MAPS 2027 (Aug 13):** Abstract co-submission opportunity identified (JPA + Shannon). Finding deadline.

## Key Developments (Aug 17-19)

- **Citeline data element selection meeting (Aug 17):** Met with Adam Canigiani (Data Enablement, ACE team), Peter Baumeister, Karena Yu, Xiaodong Zhu, Sam Goldberg (SSI). ACE already ingests all of Trial Trove into RWDEX (~590K trials, 45-46 tables in Redshift, monthly refresh -- more frequent syncs possible). Pharma Projects lives in separate Scientific Data Consumption Lake (SSI side). Free text fields NOT in RWDEX -- API only.
- **"Congress as a Data Product" gaining traction:** Peter agreed to host a follow-up call with Patrick, Shannon, Adam, Steve Bridgman.
- **Google medical-grade AI conversation (Aug 19):** Patrick and Eric met with Crystal from Google about exposing med info documents to LLMs. MRL Debrief comparison is the strongest example Merck has. See [[google-medical-ai]].

## Key Developments (Aug 20-31)

### Sept 1 Demo / USMA ESMO Core Planning (IMMINENT)
- Matt met with Rita for thorough walkthrough; has access to all environments (test environment for demo). EPAM pushing features to staging.
- Patrick will do 30-second intro. ~12 USMA attendees at ESMO.
- Quick reference guide needed covering workflow statuses (not started, in progress, reviewed, completed), auto vs. manual status changes, side-by-side comparison with old email process. Reference: "Change Navigator" from 2025 POCs folder (Sam Goldberg's screenshots).
- Backup demo screenshots in case system goes down.
- Recording will be parsed as standalone training reference; fallback: Gemini Notebook explainer from recording + user guide.
- MSL attendee list captured by Cinnamon, sent to Shannon. MSL training may happen week of ESMO (worst case) or late Sept/early Oct.

### Sept 2 Global Planning Meeting
- EDSAs and GDMAs review thousands of abstract lines. First exposure to digital abstract library.
- Planning feature only hitting development Aug 26 (not staging yet). Rita will do 2-minute quick demo as draft/preview, invite volunteers for deeper exploration.
- Official demo kickoff Sept 25 when LBAs become available.
- Automatic submission form now available for access requests (no manual ISID collection). 3 tiers: admin, user, viewer.
- Rita coordinating with Jen Devers Triggiani and Mellie who facilitate the call. Shannon introduced Rita via IM.
- **Stephen Leong inquiry (Aug 31):** Asked whether system can download all ESMO abstracts or requires keywords. Also asked about integrating Veeva Link News. Rita responded (covering for Shannon): search by keywords is supported, all Larvol data is stored but bulk download not supported. Rita offered 1.5-2 min demo at the kick-off meeting.

### Citeline / Trial Trove Data Access
- **Metadata enhancement prioritized** as faster use case (over abstract summarization). Rita sees direct applicability. Shannon confirmed to run with this.
- Matt prepared Excel field mapping (~38 of ~60 fields mapped with priority column). Sent to Adam for "we have it / we don't" assessment.
- **TPA (Third Party Agreement) IS needed** for data access per Adam (Aug 26 confirmation). Matt filling out TPA form; coordinating with Adam and Uri for help with fields. Uri already submitted his.
- RWDEX NOT yet in Databricks -- Adam says end of year (not end of Sept as Jakub said). Databricks migration won't bypass access requirements.
- Adam confirmed RWDEX already has: therapeutic classes, mechanism of action, company name, drug database.
- **Two use cases identified:** (1) metadata enhancement for abstract library, (2) abstract summarization/preamble enrichment. EPAM reviewing priorities.
- Matt to copy Karena Yu on finalized field list. Shannon to follow up with Karena's team separately.
- Offline session planned: Adam to walk Matt through RWDEX tables firsthand.
- NCT number confirmed as common linking identifier (caveat: meta-studies may have multiple NCTs).

### Northern Lights / HH Data Hub
- Northern Lights team admitted they don't know who manages NL due to IT reorgs. Shannon uncovered the product manager. HH Data Hub managed through "HH Data Genie" (contact: woman in Austin). Shannon to set up deep dive when she returns.
- Rebecca Foringer is HH global data hub contact; backup: Lori Moore.

### Congress Excellence Work Group
- Pre-work collected: 50+ reports/activities inventoried for Phase 1. Much of inventory based on abstract reuse, validating abstract library as priority.
- Mladen urged Shannon to position tool as centerpiece of unified portal at mid-Sept F2F.
- Mid-September F2F goal: prioritize abstract library for the whole company, determine which reports to work on next.
- Talia + Shannon to refresh abstract library vision slide before the session.

### MRLIT Alignment
- Amar demo went well. MRLIT aligned and supportive. Committed people to watch from tech perspective. Architect and another team member given access.
- Transition to MRLIT expected 2027; funding/mechanics being worked through.

### Tiering Tags (Shannon Teams msg Aug 20)
- Cross-division ONC Steering Committee tags priority abstracts Tier 1/2/3. Comprehensive Congress Summary typically includes Tier 1 only.
- **Goal:** Tags in Abstract Library by Sept 2 (ESMO EDSA Planning Kickoff). Mladen confirmed he'll send tags when available. Risk: may wait until LBAs post Sept 25.
- **Merck Pubs (GMI-ESKAL):** Consuelo Dominguez (Madrid) posts full glossary of company submissions on SharePoint before Tier 1 events. Shannon + Rita had call with Consuelo to discuss pulling content into abstract summary and tagging Merck content.

### AHA 2026
- CI team member responded positively to request for raw data -- first time ever. Happy to meet. Meeting planned after Shannon returns.
- Cinnamon + Shannon to schedule post-vacation meeting with Ante Harxhi (EDSA for AHA) to walk through goals.

### Legal / Governance
- **Sept 11:** Call with head of legal for division about abstract library risk posture (uploading posters, screenshots, etc.). Current senior leader position: "let them upload whatever" since it's experimental.
- Shannon plans to personally take poster screenshots at ESMO to pre-load and reduce user burden. Official poster downloads likely 2 days after ESMO.
- **Study Map:** Final call with legal on eliminating execution resource when Shannon returns. If legal doesn't agree, execution resource is already drafted. Last blocker to full automation.

### Experimental Governance
- Shannon working with Eleonora to meet Jen Hess (legal/compliance) about governance for ESMO and AHA experiments.
- Patrick notes Jen Hess has been "more understanding" lately about V&I's AI efforts.

### EPAM Technical
- **100-user regression testing passed.** EPAM found bottlenecks, fixed them all. Shannon to inform MAR Messik (MRLIT).
- **API connection to abstract library broke.** Root cause: Merck migrating to new centralized API platform. Underlying Kong API still works. Matt + Rita/Uri to troubleshoot; if portal migration is the blocker, wait.

### Shannon Vacation Aug 26 - Sep 8
- JPA covering demos and coordination. Shannon cleaned up task list before departure.

### "Congress Data as Its Own Dataset" Vision
- With CI databases + Northern Lights + Citeline access, Shannon floated creating Merck's own "Larvol dataset" and potentially walking away from vendors. All data linked by NCT number. Peter's ACE team already scrapes external sites daily. Patrick: enthusiastic but measured.

### Enterprise IT Context
- Alex King (formerly Apex, now enterprise IT) shared that Merck blew entire GitHub token budget by May. Token limits will get worse.

### New Leader (Linda)
- Shannon sent intro blurb. Linda scheduled 30 min on Sept 24. Potential executive sponsor now that Susanna moved over. Patrick has a good relationship with Linda.

## Key Developments (Sep 1-3)

### Sept 1 USMA ESMO Core Planning Demo
- **Demo went well.** JPA covered (Shannon on vacation). Patrick did 30-second intro. Patrick: "Matt seriously killed it."
- Follow-up items documented in `CongressAI/ESMO Demo follow up - QRG and EPAM.docx`.
- QRG slides + Adi bio sent to Adebayo Ogunniyi; embedded in master ESMO deck (Patrick's preference). Live link shared for ongoing updates.

### Sept 1 ESMO Core Team Planning Call
- Third ESMO planning call. ~24 US attendees going to ESMO.
- Next Core Plus call Sept 17, then "Know Before You Go" Oct 14.
- MSD 360 appointment creation locked by Cadence until Sept 21 (not leadership-approved, Cadence internal decision for visibility during planning phase). Full access restored after Sept 21.
- Patrick's group presenting new abstract submission process.

### Sept 2 Ways of Working Updates
- **Eleanor Ford pre-read deck finalized.** Patrick adding "Executive Summary" divider section. Data governance narrative kept off slides (risk tolerance for Jen Hess). Changed "additional experiments underway for ESMO" → "experiments underway for ESMO."
- **HTML presentations idea (Rita):** Suggested moving away from PPTX toward interactive HTML for debriefs. Patrick open but "not yet" -- start with lower-stakes audiences post-ESMO, not Eleanor Ford. Talia: "pick our battles."
- **Co-assignment resolved: EPAM building parallel editing.** Both assignees can edit simultaneously with conflict resolution (notifications when something updates). Rules are team-specific (not congress-specific) -- US RMSDs have different ways of working than ex-US MSLs.
- **Trading/reassignment: keep loose for experiment.** System already supports reassignment. Decision: logging only, no governance gates. Trust the people. Shannon on-site with admin permissions as safety net. Concept floated: "reassign to" button (third option alongside accept/reject).
- **MSL/PDT training postponed.** Rita recommended waiting until feedback from Sep 1 demo is implemented, then re-record demo with updated workflow. Target: by Sept 14 meeting. Recording shared back to RMSDs too. Cinnamon confirming timing and attendee list with Mellie.
- **ESMO scope: US + ex-US.** Shannon confirmed experiment covers all field medical, not just US RMSDs. Patrick was surprised. Additional training session needed for MSLs. ~39 MSLs + ~77 PDTs per Emily Shepherd's list (but only ESMO attendees need training -- Jen can subset).
- **Connectivity concern for ESMO.** Zscaler + congress floor Wi-Fi unreliable. URI noted AWS global outage last week affected Merck systems. Software designed for network weather. Mobile: works on Merck managed devices but tablet optimization postponed after ACC. Hotspot as backup. International iPad data plans unknown.
- **Stephen Leong still pushing real-time data** at Sep 2 planning demo. Says Larvol spreadsheets are "already outdated." Rita positioning direct congress data as "North Star." Patrick: data acquisition is harder than software engineering. Conversations with CI/GMPIA/Eleanor Ford team continue weekly. Larvol API would improve interface but same data/frequency. Direct society access unlikely near-term.
- **AI permissions distinction clarified:** Can't feed ESMO-sourced materials into AI for summarization (contract restriction), but CAN use Larvol-sourced data. Experiment with user-uploaded photos/screenshots is the workaround under experimental posture.

### QRG Follow-Up Items
- **Debrief materials:** Envision Pharma (EP) provides materials for every debrief presentation. Materials outside debrief presentations still gathered manually. EP sends after presentation concludes.
- **Compliance (phone photos):** Acceptable as long as images stay on internal-use platform -- pending final legal review. Patrick noted irony: "they've been taking photos forever, now they care." Decision: don't put compliance note in QRG in writing for now.
- **Upload limits:** 50MB per file, no limit on number of files.
- **Assignment process:** Initial assignments still handled outside the system -- EPAM replicates the EDSA spreadsheet on the backend.

### EPAM Technical Requests (from demo follow-up)
- ~~**Co-assigned write-ups (RMSDs + Clinical Directors):** Can both edit simultaneously or sequential?~~ RESOLVED: EPAM building parallel editing with conflict resolution.
- **Late assignment changes / trading write-ups:** System already supports it. Keeping loose for experiment. Logging changes, no governance gates.

### Citeline / Trial Trove Data Access
- **TPA form submitted** by Matt on Sep 1 after meeting with Adam.
- Matt starting RWDEX trainings (training links broken, possibly Zscaler -- Rita sending alternative link).
- **Need to ping Rita** about Citeline field prioritization so it can move on to Karena.

### Sept 3 Weekly Check-in
- MRL Debrief + SEP integration "waiting in the wings" per Talia -- picking up as digital planning returns to EPAM for development.
- Congress AI described as "roadshow coming up" with several demos. Matt: "in good shape."

## Key Developments (Sep 9)

### Shannon Returns / Workflow Decision (Sep 9)
- **Serial workflow confirmed for ESMO:** Shannon wants RMSD to complete their portion first, then it gets assigned to the PDT -- NOT parallel co-assignment. This reverses the earlier EPAM direction of parallel editing with conflict resolution. Shannon: "I want to stay true to all the interviews we've done... they really do work through a stepwise approach with checks and balances."
- **Rita's wizard implementation (Sep 9 call):** When MSD completes their part, wizard will prompt: change status or reassign to next colleague. PDT step gets one primary field (relevance and impact statement) plus ability to view/edit everything else. Rita (Marharyta) tracking with Shannon's approach.
- **Clinical director layer revealed:** Congress Ops (Jill's team) disclosed there's a clinical director layer between MSD/MSL and PDT -- wasn't captured in any stakeholder interviews. They write the relevance and impact statement with the PDT. Shannon: "Whatever this hierarchy of people on the oncology side... when we get to AHA, their process is a bit different." Wizard needs TA-by-TA and event-by-event flexibility after the RMSD/MSL step.
- **Rita flagged concern:** Needs to talk to an actual PDT or clinical director from last year to understand real workflow before testing -- "I'm a little bit worried about the wizard stuff because it's not that flexible that we think about it."

### Demo Planning (Sep 9)
- **Follow-up demo scheduled Sep 17** for Adebayo's USMA Core Planning team (same audience from 9/1 demo). Shannon doing kickoff intro, Matt doing live demo. Will add slides addressing previous questions and how they've been addressed since.
- **Sep 14 ESMO Abstract Planning (listen-only):** Enterprise-wide kickoff for ESMO, mainly EDSAs and leaders selecting abstracts. Matt should attend (camera off, listen in). No demo this week. Shannon wants a demo in this series closer to ESMO.
- **Shannon forwarding Sep 17 invite** to Rita/Uri, Matt, Talia, Cinnamon, Patrick.

### QRG / Training Materials Hosting (Sep 9)
- **SharePoint Congress AI page proposed:** Shannon wants to create a Congress AI page on the V&I MedOps SharePoint site as single source of truth -- video, QRG, updates all in one place. Avoids version fragmentation and dependency on Patrick hosting. Patrick agreed.
- **Recording plan:** Original Sep 1 demo not being distributed (feedback required tooling changes). Sep 17 follow-up demo will be recorded as the distributable video.
- **QRG still being iterated:** Matt added FAQ slide and format changes per Patrick's feedback. Shannon will locate latest version and regroup with Matt.

### Congress Ops Stress / Office Hours Plan (Sep 9)
- **Jill's team expressing stress and concerns** about ESMO workflow readiness. Shannon met with them Sep 8.
- **Shannon proposing optional office hours** over the next 30 days across multiple time zones (Asia-friendly slots) so field staff can explore the tool. Record sessions, share video + QRG. Goal: prevent day-before-event stress.
- **Cinnamon going on vacation soon.** Matt will be primary admin support for Shannon during this period.

### Medical Writer Email Export (Sep 9)
- **Write-up export to medical writers designed:** When reviewer changes status to "Complete," modal prompts "do you want to send the email?" Pre-populated with medical writer recipient list. Same team for all abstracts (no per-abstract customization). Jill's team CC'd.
- **Word document attachment preferred** (Congress Ops wants format identical to current process so Envision Pharma doesn't request contract changes). EPAM needs: (1) example Word doc from last year, (2) recipient list, (3) CC list.
- **No intermediate steps known** between MSD/PDT completing and sending to medical writers -- but Shannon notes this may vary by TA.

### AHA Kickoff (Sep 9)
- **AHA call held Sep 9 afternoon** with Ante Harxhi and CV team. Informal overview of Congress AI approach for American Heart Association.
- **CV team workflow differs from oncology:** Goes to MSD/MSL, but then Ante himself writes the relevance and impact statement. Justin Harris, Daniel Timko, and Ritu Goyanka are a layer between MSLs and EDSAs -- not RMSDs or MSLs, not EDSAs.
- **Shannon's exec leaders prioritizing ESMO and AHA** for conversations with professional societies about real-time/centralized document access (screenshot Sep 10). Shannon met with AHA leaders twice; interested but new to this type of collaboration. Data rights/copyright driving potential direct contracting with events for data access.

## Key Developments (Sep 10-11)

### Citeline Mirror Dead End (Shannon Teams Sep 10 5:28 PM)
- **Greg Bryman: no clear path forward for enabling a Citeline mirror that hasn't already been created.** Shannon met with Greg this week; he provided quick updates. Shannon wants to discuss with Matt and JPA during weekly call (Sep 11).
- Implication: RWDEX remains the existing access path. No new mirror or API shortcut emerging from Greg's team.

### Congress Excellence Workgroup Inventory (Shannon Teams Sep 10)
- **Jagruti Patel from the CI team attending the live Congress Excellence Workgroup session next week.** This is significant -- first CI team presence at this level.
- **100+ congress-related activities submitted in the enterprise inventory.** Planning team bundled them into ~50 distinct activities that will be the focus of the entire first day.
- Shannon: "Can't wait to listen and hear all of the wildly inefficient work going on within the company."

### Governance Approval -- ESMO and AHA Greenlit (Shannon Teams Sep 11 12:14 PM)
- **Presentation to Jen Hess and Linda Kollmar went "extremely well."** They complimented the work and experimentation model.
- **Approval to move forward with ESMO and AHA.** This resolves the major governance blocker.
- Shannon meeting with the legal team next to introduce them to the work.
- Shannon: "Each of you are part of why this project is so successful... so THANK YOU!"
- Note: Meeting happened Sep 11 (not Sep 12 as originally scheduled).

## JPA Deliverables / Action Items (Sep 10)

- ~~**Matt: Submit TPA form** for Citeline (aka Trial Trove) data access (coordinating with Adam and Uri)~~ DONE (submitted Sep 1 after meeting Adam)
- **Matt: Ping Rita** about Citeline field prioritization so it can move to Karena Yu
- ~~**Matt: Schedule offline session with Adam** to walk through RWDEX tables~~ DONE (met Sep 1)
- **Matt: Complete RWDEX trainings** (training links broken -- Zscaler issue, Rita sending alt link)
- ~~**Matt: Prepare quick reference guide + backup demo slides** for Sept 1 demo~~ DONE (themed backup deck + QRG built Aug 31)
- **Matt + Rita: MRL Debrief -- meet with Destiny** on technical needs; troubleshoot centralized API migration blocker
- ~~**Rita: Coordinate with Jen Devers Triggiani and Mellie** for Sept 2 planning feature preview~~ DONE (demo held Sep 2, discovered a bug, fixing)
- **Matt: Update QRG** with demo follow-up items (upload limits, EP materials info); keep live link current for Adebayo
- **Cinnamon: Confirm MSL/PDT training timing and ESMO attendee subset** with Mellie/Jen
- **EPAM: Implement serial workflow** (RMSD completes → wizard prompts reassign → PDT gets R&I field). Replaces earlier parallel co-editing direction.
- **EPAM: Build medical writer email export** -- Word doc attachment on "Complete" status change, pre-populated recipients, CC to Congress Ops. Needs: last year's example Word doc, recipient list.
- **EPAM: Talk to actual clinical director from last year** to understand real workflow before testing wizard
- **Talia + Shannon: Refresh abstract library vision slide** before mid-Sept F2F
- **Shannon: Create Congress AI page on V&I MedOps SharePoint** -- single source of truth for QRG, video, updates
- **Shannon: Northern Lights deep dive** with HH Data Genie contact
- **Shannon: CI team meeting** for AHA raw data access
- ~~**Shannon: Legal call Sept 11** on abstract library data governance~~ DONE -- Jen Hess + Linda Kollmar approved ESMO and AHA (Sep 11)
- **Shannon: Study Map legal finalization**
- **Shannon: Set up on-site base camp** near corporate suites for ESMO support
- **Shannon: Provide last year's Word doc example + medical writer recipient list** to EPAM
- **Cinnamon + Shannon: Schedule AHA EDSA kickoff** with Ante Harxhi -- initial call held Sep 9, follow-up TBD
- **Matt + EPAM: Prepare follow-up demo for Sep 17** -- Adebayo's USMA Core Planning team. Shannon doing intro, Matt doing demo. Record this one for distribution.
- **Matt + Rita: Plan demo for ESMO Abstract Planning series** -- no demo currently slated; Shannon wants one closer to ESMO. Determine timing and content.

## 2027 Planning

- Everyone wants traditional in-person planning session; unsure if travel schedules permit.
- Cinnamon + Shannon comparing calendars with Gem. Talia offered micro-meeting alternative (focused 2-hour subset session).
- Need to shift back toward original structure: experimentation/POC separated from broader delivery with 30-day cycles.

## Data Rights Constraint

No AI rights in current event contracts. CI databases and publication content are the #1 priority workaround. **Sept 11 governance meeting with Jen Hess + Linda Kollmar: approved to move forward with ESMO and AHA.** Shannon meeting with legal team next to introduce them to the work. Current posture: senior leaders saying "let them upload whatever" for the experiment. Frame as "upload official files when available, screenshots/personal notes as backup."

## Open Questions

- Source of truth for abstract metadata: Larvol, manual input, or AI-generated first pass? CI team breakthrough (positive response to data request) may open new path.
- Preamble/Key Implications: Rita less certain Citeline data will improve preambles (more Merck-specific strategic assessments). May remain a gap.
- PDT reviewer selection workflow: MSL/RMSD selects the PDT reviewer to avoid maintaining org charts.
- Some fields in Matt's spreadsheet marked "no - SSI Lake" may be available through Karena Yu's team. Needs confirmation.

## Related Memories

See [[mrl-debrief-status]] for the debrief automation workstream.
See [[merck-stakeholders]] for full stakeholder map.
See [[google-medical-ai]] for the medical-grade AI conversation.

**ESMO planning rosters (screenshots/):**
- `ESMO USMA core planning team.png` -- Core planning team by tumor team (Breast, GI, GU, Gyn, HN/Mel, Lung), TL/RMSD Congress Leads, and live/virtual attendees. HQ: Uma Srivastava (AVP), Jamie Dettler-Leonard (OMED).
- `ESMO tumor leads.png` -- All tumor teams mapped to EDSAs, GDMAs, and RTLs. ~15 teams including Precision Medicine (Apostolos Pinakidis, PoC congress activities), Keytruda Asset, DS and Moderna.
