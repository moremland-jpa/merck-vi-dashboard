from __future__ import annotations

import re
from pathlib import Path

import yaml


def parse_frontmatter(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            return {}
        end = text.index("---", 3)
        fm_text = text[3:end]
        fm = yaml.safe_load(fm_text) or {}
        modified = ""
        if "metadata" in fm and isinstance(fm["metadata"], dict):
            modified = fm["metadata"].get("modified", "")
        return {
            "name": fm.get("name", ""),
            "description": fm.get("description", ""),
            "modified": str(modified),
        }
    except Exception:
        return {}


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text
    try:
        end = text.index("---", 3)
        return text[end + 3 :].lstrip("\n")
    except ValueError:
        return text


def parse_sections(text: str, level: int = 2) -> dict[str, str]:
    prefix = "#" * level + " "
    sections: dict[str, str] = {}
    current_header = None
    current_lines: list[str] = []

    for line in text.splitlines():
        if line.startswith(prefix) and not line.startswith(prefix + "#"):
            if current_header is not None:
                sections[current_header] = "\n".join(current_lines).strip()
            current_header = line[len(prefix) :].strip()
            current_lines = []
        elif current_header is not None:
            current_lines.append(line)

    if current_header is not None:
        sections[current_header] = "\n".join(current_lines).strip()

    return sections


def parse_markdown_table(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    lines = [l for l in text.strip().splitlines() if l.strip().startswith("|")]
    if len(lines) < 2:
        return rows

    headers = [c.strip() for c in lines[0].strip().strip("|").split("|")]

    for line in lines[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != len(headers):
            continue
        row = dict(zip(headers, cells))
        if all(v == "" or set(v) <= {"-", " "} for v in row.values()):
            continue
        rows.append(row)

    return rows


def parse_all_tables(text: str) -> list[tuple[str, list[dict[str, str]]]]:
    body = strip_frontmatter(text)
    sections = parse_sections(body, level=2)
    results: list[tuple[str, list[dict[str, str]]]] = []
    for header, content in sections.items():
        table = parse_markdown_table(content)
        if table:
            results.append((header, table))
    return results


_ACTION_PATTERN = re.compile(
    r"^[\s]*[-*]\s+"
    r"(?P<strike>~~)?"
    r"\*\*(?P<head>[^*]+)\*\*"
    r"(?:~~)?"
    r"(?P<tail>.*)",
)

_NUMBERED_PATTERN = re.compile(
    r"^[\s]*\d+\.\s+"
    r"(?P<strike>~~)?"
    r"\*\*(?P<head>[^*]+)\*\*"
    r"(?:~~)?"
    r"(?P<tail>.*)",
)


def parse_action_items(text: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for line in text.splitlines():
        m = _ACTION_PATTERN.match(line) or _NUMBERED_PATTERN.match(line)
        if not m:
            continue

        head = m.group("head").strip()
        tail = m.group("tail").strip().lstrip("-").lstrip().rstrip()
        done = m.group("strike") is not None or "DONE" in tail.upper()

        owner = ""
        description = head
        if ":" in head:
            parts = head.split(":", 1)
            owner = parts[0].strip()
            description = parts[1].strip()

        if tail:
            description = f"{description} -- {tail}"

        items.append(
            {
                "owner": owner,
                "description": description,
                "status": "Done" if done else "Pending",
                "due_date": "",
                "completed_on": "",
                "notes": "",
            }
        )

    return items


def parse_bullet_items(text: str) -> list[str]:
    items: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- ") or stripped.startswith("* "):
            items.append(stripped[2:].strip())
    return items


def extract_current_state(body: str) -> str:
    sections = parse_sections(body, level=2)
    for header, content in sections.items():
        if header.lower().startswith("current state"):
            return content
    return ""


def extract_key_developments(body: str) -> list[tuple[str, str]]:
    sections = parse_sections(body, level=2)
    devs: list[tuple[str, str]] = []
    for header, content in sections.items():
        if "key development" in header.lower():
            subsections = parse_sections(content, level=3)
            if subsections:
                for sub_header, sub_content in subsections.items():
                    devs.append((sub_header, sub_content))
            else:
                devs.append((header, content))
    return devs


def extract_action_items(body: str) -> list[dict[str, str]]:
    sections = parse_sections(body, level=2)
    for header, content in sections.items():
        lower = header.lower()
        if any(
            kw in lower
            for kw in ["action item", "deliverable", "pending update", "recommendation"]
        ):
            return parse_action_items(content)

    for header, content in sections.items():
        lower = header.lower()
        if "action" in lower:
            return parse_action_items(content)

    return []


def extract_key_developments_grouped(
    body: str,
) -> list[tuple[str, list[tuple[str, str]]]]:
    sections = parse_sections(body, level=2)
    groups: list[tuple[str, list[tuple[str, str]]]] = []
    for header, content in sections.items():
        if "key development" not in header.lower():
            continue
        subsections = parse_sections(content, level=3)
        items = list(subsections.items()) if subsections else [(header, content)]
        groups.append((header, items))
    return groups


def extract_open_questions(body: str) -> list[str]:
    sections = parse_sections(body, level=2)
    for header, content in sections.items():
        if "open question" in header.lower():
            return parse_bullet_items(content)
    return []


# ── Key development classification ──

_MONTH_MAP: dict[str, int] = {
    "jan": 1, "january": 1, "feb": 2, "february": 2,
    "mar": 3, "march": 3, "apr": 4, "april": 4,
    "may": 5, "jun": 6, "june": 6, "jul": 7, "july": 7,
    "aug": 8, "august": 8, "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10, "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}

_DATE_RE = re.compile(
    r"\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
    r"Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|"
    r"Nov(?:ember)?|Dec(?:ember)?)\s+(\d{1,2})\b",
    re.IGNORECASE,
)

_PROVENANCE_RE = re.compile(r"\(from\s+(.+?)\)", re.IGNORECASE)


def _extract_date_from_title(title: str, year: int = 2026):
    from datetime import datetime as _dt

    m = _DATE_RE.search(title)
    if not m:
        return None
    month_str = m.group(1).lower()
    for prefix, num in _MONTH_MAP.items():
        if month_str.startswith(prefix):
            try:
                return _dt(year, num, int(m.group(2))).date()
            except ValueError:
                return None
    return None


def _extract_provenance(title: str) -> str:
    m = _PROVENANCE_RE.search(title)
    return m.group(1).strip() if m else ""


def _infer_status(content: str) -> str:
    lower = content.lower()
    if any(kw in lower for kw in ("blocker", "blocked", "cannot", "can't")):
        return "Blocked"
    lines = [l.strip() for l in content.splitlines() if l.strip().startswith("-")]
    if lines:
        done_count = sum(1 for l in lines if "~~" in l or "DONE" in l.upper())
        if done_count > len(lines) / 2:
            return "Done"
    if any(
        kw in lower
        for kw in (
            "waiting",
            "pending",
            "need to",
            "coordinating",
            "scheduling",
            "open question",
        )
    ):
        return "Waiting"
    return "Active"


def _extract_summary(content: str, max_len: int = 120) -> str:
    for line in content.splitlines():
        stripped = line.strip().lstrip("-").lstrip("*").strip()
        if len(stripped) < 10:
            continue
        stripped = stripped.replace("**", "")
        if len(stripped) > max_len:
            return stripped[: max_len - 3] + "..."
        return stripped
    return ""


def classify_key_developments(
    devs: list[tuple[str, str]],
) -> tuple[list[dict], list[dict]]:
    from datetime import date

    today = date.today()

    # Build items, deduplicating by normalized title (last wins)
    deduped: dict[str, dict] = {}
    for title, content in devs:
        if title.lower().startswith("key development"):
            continue

        norm = re.sub(r"\s*\(.*?\)\s*$", "", title).strip().lower()
        dt = _extract_date_from_title(title)

        item = {
            "title": title,
            "content": content,
            "summary": _extract_summary(content),
            "status": _infer_status(content),
            "provenance": _extract_provenance(title),
        }
        if dt:
            item["date"] = dt
            item["is_past"] = dt <= today

        deduped[norm] = item

    events = [it for it in deduped.values() if "date" in it]
    threads = [it for it in deduped.values() if "date" not in it]

    events.sort(key=lambda x: x["date"])

    status_order = {"Blocked": 0, "Waiting": 1, "Active": 2, "Done": 3}
    threads.sort(key=lambda x: status_order.get(x["status"], 2))

    return events, threads
