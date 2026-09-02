from __future__ import annotations

import base64
import json
import re
from io import BytesIO
from pathlib import Path

import streamlit as st

import parsers
import utils

_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
_IMAGE_MEDIA_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}

_DEFAULT_MODEL = "claude-sonnet-4-20250514"

_SYSTEM_PROMPT = """\
You are a transcript processor for the Merck V&I engagement at JPA Health. \
You analyze meeting transcripts and extract structured updates for the project's \
knowledge base.

The engagement has 4 workstreams:
1. **Congress AI** (file: congress-ai-status.md) — AI-powered congress planning, \
abstract triage, write-up workflows. EPAM is the dev partner. Targeting ESMO \
(late October 2026).
2. **Genesis** (file: genesis-status.md) — Merck's internal AI platform for \
analyzing MSL field insights. Sentiment 2.0 redesign.
3. **MRL Debrief** (file: mrl-debrief-status.md) — Automated MRL congress debrief \
generation. SEP integration.
4. **Asset Reporting** (file: asset-reporting-status.md) — Two-layer asset \
normalization framework for congress reporting.

Cross-cutting file:
- **merck-stakeholders.md** — Stakeholder directory with tables per organization.

Common transcription errors to correct:
- "SCP" -> "SEP" (Scientific Engagement Priorities)
- "SMRL" -> "SLRM" (Scientific Liaison & Resource Manager)
- "Larval" / "Laravel" -> "Larvol" (congress data vendor)

## Your Task

Analyze the transcript and return a JSON object with proposed updates. Be \
conservative — only propose changes supported by clear evidence in the transcript. \
Do not infer or speculate.

## Output Schema

Return ONLY valid JSON (no markdown fencing) matching this structure:

{
  "transcript_summary": "2-3 sentence summary of the meeting",
  "meeting_date": "YYYY-MM-DD if determinable, otherwise null",
  "workstreams_touched": ["Congress AI"],
  "changes": [
    {
      "type": "update_current_state",
      "file": "congress-ai-status.md",
      "workstream": "Congress AI",
      "reason": "Why this update is needed, citing transcript evidence",
      "new_content": "Full replacement markdown for the Current State section body"
    },
    {
      "type": "add_action_items",
      "file": "congress-ai-status.md",
      "workstream": "Congress AI",
      "reason": "Evidence from transcript",
      "items": [
        {"owner": "Matt", "description": "Follow up with Shannon on data rights"}
      ]
    },
    {
      "type": "complete_action_items",
      "file": "congress-ai-status.md",
      "workstream": "Congress AI",
      "reason": "Evidence that these items are done",
      "descriptions": ["Submit TPA to Shannon"]
    },
    {
      "type": "add_key_development",
      "file": "congress-ai-status.md",
      "workstream": "Congress AI",
      "reason": "Evidence from transcript",
      "title": "Descriptive title for the development",
      "content": "Markdown body of the development entry"
    },
    {
      "type": "add_stakeholder",
      "file": "merck-stakeholders.md",
      "reason": "New person mentioned in transcript not in current directory",
      "person": {
        "name": "Full Name",
        "role": "Their role",
        "organization": "Which org section (Merck V&I Operations, EPAM, JPA Health, Genesis Technical Team, Sentiment Super Users, Additional Stakeholders)",
        "workstreams": "Comma-separated workstream names",
        "notes": "Context from the transcript"
      }
    },
    {
      "type": "general_note",
      "workstream": "Congress AI or Cross-cutting",
      "reason": "Important context that does not fit other categories",
      "note": "The note content"
    }
  ]
}

Guidelines:
- For update_current_state: rewrite the FULL section body incorporating new \
information alongside existing facts that were not contradicted. Be thorough — \
this replaces the entire section.
- For add_action_items: only include clearly assigned action items with an \
identifiable owner. Use first names for JPA staff (Matt, Grace, Cinnamon, Talia, \
Colin). Use full names for Merck/EPAM staff.
- For complete_action_items: only mark items done when there is explicit \
confirmation. The "descriptions" values should contain enough keywords to match \
against the existing action item text.
- For add_key_development: include significant decisions, milestones, or events \
worth tracking. Use a concise, descriptive title.
- For add_stakeholder: only for people not already in the directory who played a \
meaningful role in the discussion.
- For general_note: use sparingly for important cross-cutting context.
- Correct transcription errors (SCP->SEP, SMRL->SLRM, Larval->Larvol).
- Be specific and cite evidence from the transcript in every "reason" field.
- Omit change types that have no instances — do not return empty arrays.
"""


def _get_client():
    try:
        import anthropic
    except ImportError:
        return None
    api_key = st.secrets.get("anthropic_api_key", "")
    if not api_key:
        return None
    return anthropic.Anthropic(api_key=api_key)


def is_image(filename: str) -> bool:
    return Path(filename).suffix.lower() in _IMAGE_EXTENSIONS


def extract_text(uploaded_file) -> str:
    name = uploaded_file.name.lower()
    if name.endswith(".docx"):
        import docx

        doc = docx.Document(BytesIO(uploaded_file.read()))
        return "\n".join(p.text for p in doc.paragraphs)
    return uploaded_file.read().decode("utf-8", errors="replace")


def _encode_image(uploaded_file) -> dict:
    ext = Path(uploaded_file.name).suffix.lower()
    media_type = _IMAGE_MEDIA_TYPES.get(ext, "image/png")
    data = base64.standard_b64encode(uploaded_file.read()).decode("ascii")
    return {
        "type": "image",
        "source": {"type": "base64", "media_type": media_type, "data": data},
    }


def _build_context() -> str:
    parts: list[str] = []
    for _key, cfg in utils.WORKSTREAMS.items():
        path = utils.MEMORY_DIR / cfg["status_file"]
        content = utils._read_file_safe(path)
        if content:
            parts.append(f"### {cfg['status_file']}\n```\n{content}\n```")
    path = utils.MEMORY_DIR / "merck-stakeholders.md"
    content = utils._read_file_safe(path)
    if content:
        parts.append(f"### merck-stakeholders.md\n```\n{content}\n```")
    return "\n\n".join(parts)


def process_transcript(
    text: str | None = None,
    images: list | None = None,
) -> dict | None:
    client = _get_client()
    if not client:
        return None

    context = _build_context()
    model = st.secrets.get("anthropic_model", _DEFAULT_MODEL)

    content_blocks: list[dict] = []

    if images:
        for img in images:
            img.seek(0)
            content_blocks.append(_encode_image(img))
        file_names = ", ".join(img.name for img in images)
        content_blocks.append(
            {
                "type": "text",
                "text": (
                    f"## Current Memory Files\n\n{context}\n\n"
                    f"## Screenshots\n\n"
                    f"The above image(s) ({file_names}) are screenshots from "
                    f"Teams messages, slides, or other project materials. "
                    f"Extract all relevant information and propose updates."
                ),
            }
        )
    elif text:
        content_blocks.append(
            {
                "type": "text",
                "text": (
                    f"## Current Memory Files\n\n{context}\n\n"
                    f"## Transcript\n\n{text}"
                ),
            }
        )
    else:
        return None

    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": content_blocks}],
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()

    return json.loads(raw)


# ── Apply helpers ──


def apply_change(change: dict) -> bool:
    handlers = {
        "update_current_state": _apply_current_state,
        "add_action_items": _apply_add_actions,
        "complete_action_items": _apply_complete_actions,
        "add_key_development": _apply_key_dev,
        "add_stakeholder": _apply_stakeholder,
        "general_note": lambda _c: True,
    }
    handler = handlers.get(change.get("type", ""))
    if not handler:
        return False
    return handler(change)


def _read_lines(filename: str) -> tuple[Path, list[str]] | None:
    path = utils.MEMORY_DIR / filename
    raw = utils._read_file_safe(path)
    if not raw:
        return None
    return path, raw.splitlines(keepends=True)


def _body_start(lines: list[str]) -> int:
    if lines and lines[0].strip() == "---":
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                return i + 1
    return 0


def _apply_current_state(change: dict) -> bool:
    result = _read_lines(change["file"])
    if not result:
        return False
    path, lines = result

    start = _body_start(lines)
    section_start = None
    for i in range(start, len(lines)):
        if lines[i].startswith("## ") and "current state" in lines[i].lower():
            section_start = i + 1
            break
    if section_start is None:
        return False

    section_end = len(lines)
    for i in range(section_start, len(lines)):
        if lines[i].startswith("## "):
            section_end = i
            break

    new_content = "\n" + change["new_content"].rstrip() + "\n\n"
    new_lines = lines[:section_start] + [new_content] + lines[section_end:]
    path.write_text("".join(new_lines), encoding="utf-8")
    return True


def _apply_add_actions(change: dict) -> bool:
    result = _read_lines(change["file"])
    if not result:
        return False
    path, lines = result
    raw = "".join(lines)

    bounds = utils._find_action_section(raw)
    if not bounds:
        return False
    section_start, section_end = bounds

    last_num = 0
    for i in range(section_start, section_end):
        m = re.match(r"^\s*(\d+)\.", lines[i])
        if m:
            last_num = int(m.group(1))

    insert_at = section_end
    for i in range(section_end - 1, section_start - 1, -1):
        if lines[i].strip():
            insert_at = i + 1
            break

    new_items: list[str] = []
    for item in change.get("items", []):
        last_num += 1
        owner = item.get("owner", "").strip()
        desc = item.get("description", "").strip()
        bold = f"{owner}: {desc}" if owner else desc
        new_items.append(f"{last_num}. **{bold}**\n")

    new_lines = lines[:insert_at] + new_items + lines[insert_at:]
    path.write_text("".join(new_lines), encoding="utf-8")
    return True


def _apply_complete_actions(change: dict) -> bool:
    result = _read_lines(change["file"])
    if not result:
        return False
    path, lines = result
    raw = "".join(lines)

    bounds = utils._find_action_section(raw)
    if not bounds:
        return False
    section_start, section_end = bounds

    targets = [d.lower() for d in change.get("descriptions", [])]
    if not targets:
        return False

    for i in range(section_start, section_end):
        m = parsers._ACTION_PATTERN.match(lines[i]) or parsers._NUMBERED_PATTERN.match(
            lines[i]
        )
        if not m or m.group("strike"):
            continue

        head = m.group("head").strip().lower()
        tail = (m.group("tail") or "").strip().lower()
        line_text = head + " " + tail

        for desc in targets:
            words = [w for w in desc.split() if len(w) > 3]
            if not words:
                continue
            hits = sum(1 for w in words if w in line_text)
            if hits >= max(2, len(words) * 0.5):
                stripped = lines[i].lstrip()
                leading = lines[i][: len(lines[i]) - len(stripped)]
                num_m = re.match(r"(\d+)\.\s+", stripped)
                prefix = f"{num_m.group(1)}. " if num_m else "- "
                bold = m.group("head").strip()
                t = (m.group("tail") or "").strip()
                body = f"~~**{bold}**~~"
                if t:
                    body += f" {t}"
                body += " DONE"
                lines[i] = f"{leading}{prefix}{body}\n"
                break

    path.write_text("".join(lines), encoding="utf-8")
    return True


def _apply_key_dev(change: dict) -> bool:
    result = _read_lines(change["file"])
    if not result:
        return False
    path, lines = result

    start = _body_start(lines)
    title = change.get("title", "Untitled")
    content = change.get("content", "")
    entry = f"\n### {title}\n\n{content}\n"

    kd_body = None
    for i in range(start, len(lines)):
        if lines[i].startswith("## ") and "key development" in lines[i].lower():
            kd_body = i + 1
            break

    if kd_body is not None:
        lines.insert(kd_body, entry)
    else:
        action_bounds = utils._find_action_section("".join(lines))
        insert_at = (action_bounds[0] - 1) if action_bounds else len(lines)
        lines.insert(insert_at, f"\n## Key Developments\n{entry}\n")

    path.write_text("".join(lines), encoding="utf-8")
    return True


def _apply_stakeholder(change: dict) -> bool:
    path = utils.MEMORY_DIR / "merck-stakeholders.md"
    raw = utils._read_file_safe(path)
    if not raw:
        return False

    person = change.get("person", {})
    org = person.get("organization", "")
    lines = raw.splitlines(keepends=True)

    in_target = False
    target_end = len(lines)
    for i, line in enumerate(lines):
        if line.startswith("## "):
            if in_target:
                target_end = i
                break
            if org.lower() in line.lower():
                in_target = True

    if not in_target:
        target_end = len(lines)

    insert_at = target_end
    for i in range(target_end - 1, -1, -1):
        if lines[i].strip().startswith("|") and "|---" not in lines[i]:
            insert_at = i + 1
            break

    name = person.get("name", "")
    role = person.get("role", "")
    ws = person.get("workstreams", "")
    notes = person.get("notes", "")
    lines.insert(insert_at, f"| {name} | {role} | {ws} | {notes} |\n")

    path.write_text("".join(lines), encoding="utf-8")
    return True
