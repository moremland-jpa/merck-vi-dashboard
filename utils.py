from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

import parsers

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"

# Use bundled data/memory/ in the repo; fall back to local Claude memory dir
_BUNDLED_MEMORY = DATA_DIR / "memory"
_LOCAL_MEMORY = Path(
    r"C:\Users\MattOremland\.claude\projects"
    r"\C--Users-MattOremland-OneDrive---JPA-Health-Sandbox-Merck\memory"
)
MEMORY_DIR = _BUNDLED_MEMORY if _BUNDLED_MEMORY.is_dir() else _LOCAL_MEMORY

_LOCAL_PROJECT = Path(
    r"C:\Users\MattOremland\OneDrive - JPA Health\Sandbox\Merck"
)
PROJECT_DIR = _LOCAL_PROJECT if _LOCAL_PROJECT.is_dir() else APP_DIR

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

FOLDER_WORKSTREAM_MAP = {
    "CongressAI": "Congress AI",
    "Genesis": "Genesis",
    "MRL Debrief": "MRL Debrief",
    "Asset reporting": "Asset Reporting",
    "transcripts": "Transcripts",
    "screenshots": "Screenshots",
    "background documents": "Background Documents",
}

EXCLUDED_DIRS = {
    "venv", "__pycache__", ".git", ".claude", ".streamlit",
    "node_modules", "streamlit",
}

EXCLUDED_EXTENSIONS = {".pyc", ".pyo"}


def _read_file_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _file_mtime(path: Path) -> float:
    try:
        return path.stat().st_mtime
    except Exception:
        return 0.0


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
        meeting: dict[str, str] = {"name": name}
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


def _human_size(size_bytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if abs(size_bytes) < 1024:
            return f"{size_bytes:.0f} {unit}" if unit == "B" else f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024  # type: ignore[assignment]
    return f"{size_bytes:.1f} TB"


@st.cache_data(ttl=120)
def scan_documents() -> pd.DataFrame:
    records: list[dict] = []

    try:
        for p in PROJECT_DIR.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix.lower() in EXCLUDED_EXTENSIONS:
                continue

            rel = p.relative_to(PROJECT_DIR)
            parts = rel.parts
            if any(part in EXCLUDED_DIRS for part in parts):
                continue

            top_folder = parts[0] if len(parts) > 1 else ""
            workstream = FOLDER_WORKSTREAM_MAP.get(top_folder, "Other")

            try:
                stat = p.stat()
                size = stat.st_size
                modified = datetime.fromtimestamp(stat.st_mtime)
            except Exception:
                size = 0
                modified = None

            records.append(
                {
                    "Name": p.name,
                    "Folder": str(rel.parent) if str(rel.parent) != "." else "",
                    "Type": p.suffix.lower(),
                    "Size": _human_size(size),
                    "size_bytes": size,
                    "Modified": modified,
                    "Workstream": workstream,
                    "path": str(rel),
                }
            )
    except Exception:
        pass

    if not records:
        return pd.DataFrame(
            columns=["Name", "Folder", "Type", "Size", "size_bytes", "Modified", "Workstream", "path"]
        )

    df = pd.DataFrame(records)
    df.sort_values("Modified", ascending=False, inplace=True, na_position="last")
    return df


def get_workstream_doc_count(workstream: str) -> int:
    docs = scan_documents()
    if docs.empty:
        return 0
    return int((docs["Workstream"] == workstream).sum())


def get_stakeholders_for_workstream(workstream: str, limit: int = 3) -> list[str]:
    df = load_stakeholders()
    if df.empty:
        return []
    mask = df["Workstreams"].str.contains(workstream, case=False, na=False)
    return df.loc[mask, "Person"].head(limit).tolist()
