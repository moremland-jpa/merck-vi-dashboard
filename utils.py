from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd
import streamlit as st

import db
import parsers

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
MEMORY_DIR = DATA_DIR / "memory"

WORKSTREAMS = {
    "Congress AI": {
        "status_file": "congress-ai-status.md",
        "doc_folder": "CongressAI",
    },
    "Genesis": {
        "status_file": "genesis-status.md",
        "doc_folder": "Genesis",
    },
    "MRL Debrief": {
        "status_file": "mrl-debrief-status.md",
        "doc_folder": "MRL Debrief",
    },
    "Asset Reporting": {
        "status_file": "asset-reporting-status.md",
        "doc_folder": "Asset reporting",
    },
}


def _read_file_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""





@st.cache_data(ttl=60)
def load_workstream_status(key: str) -> dict:
    cfg = WORKSTREAMS.get(key)
    if not cfg:
        return {}

    path = MEMORY_DIR / cfg["status_file"]
    fm = parsers.parse_frontmatter(path)
    raw = _read_file_safe(path)
    body = parsers.strip_frontmatter(raw)

    return {
        "name": key,
        "description": fm.get("description", ""),
        "summary": fm.get("summary"),
        "modified": fm.get("modified", ""),
        "current_state": parsers.extract_current_state(body),
        "key_developments": parsers.extract_key_developments(body),
        "action_items": parsers.extract_action_items(body),
        "open_questions": parsers.extract_open_questions(body),
        "raw_body": body,
    }


@st.cache_data(ttl=60)
def load_all_statuses() -> dict[str, dict]:
    return {key: load_workstream_status(key) for key in WORKSTREAMS}


@st.cache_data(ttl=60)
def load_stakeholders() -> pd.DataFrame:
    path = MEMORY_DIR / "merck-stakeholders.md"
    raw = _read_file_safe(path)
    if not raw:
        return pd.DataFrame(columns=["Person", "Role", "Workstreams", "Notes", "Organization"])

    tables = parsers.parse_all_tables(raw)
    all_rows: list[dict[str, str]] = []

    for section_name, rows in tables:
        for row in rows:
            normalized = {
                "Person": row.get("Person", ""),
                "Role": row.get("Role", ""),
                "Workstreams": row.get("Workstreams", ""),
                "Notes": row.get("Notes", row.get("Context", "")),
                "Organization": section_name,
            }
            all_rows.append(normalized)

    if not all_rows:
        return pd.DataFrame(columns=["Person", "Role", "Workstreams", "Notes", "Organization"])

    return pd.DataFrame(all_rows)


@st.cache_data(ttl=60)
def load_meeting_cadence() -> list[dict]:
    path = MEMORY_DIR / "merck-meeting-cadence.md"
    raw = _read_file_safe(path)
    body = parsers.strip_frontmatter(raw)
    sections = parsers.parse_sections(body, level=2)
    meetings_text = sections.get("Recurring Meeting Series", body)
    meeting_sections = parsers.parse_sections(meetings_text, level=3)

    meetings: list[dict] = []
    for name, content in meeting_sections.items():
        concluded = any(
            kw in name.upper() for kw in ("CONCLUDED", "COMPLETED")
        )
        for line in content.splitlines():
            if line.strip().startswith("- **Status:**"):
                status_text = line.split(":**", 1)[1].upper()
                if any(kw in status_text for kw in ("ENDED", "CONCLUDED", "COMPLETED")):
                    concluded = True

        meeting: dict[str, str] = {"name": name, "concluded": concluded}
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("- **Cadence:**"):
                meeting["cadence"] = stripped.split(":**", 1)[1].strip()
            elif stripped.startswith("- **Attendees:**"):
                meeting["attendees"] = stripped.split(":**", 1)[1].strip()
            elif stripped.startswith("- **Covers:**"):
                meeting["covers"] = stripped.split(":**", 1)[1].strip()
            elif stripped.startswith("- **Transcript pattern:**"):
                meeting["transcript_pattern"] = stripped.split(":**", 1)[1].strip().strip("`")
        meetings.append(meeting)

    return meetings


@st.cache_data(ttl=60)
def load_milestones() -> list[dict]:
    path = DATA_DIR / "milestones.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []









def get_stakeholders_for_workstream(workstream: str, limit: int = 3) -> list[str]:
    df = load_stakeholders()
    if df.empty:
        return []
    mask = df["Workstreams"].str.contains(workstream, case=False, na=False)
    return df.loc[mask, "Person"].head(limit).tolist()
