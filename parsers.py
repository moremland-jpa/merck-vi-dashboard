from __future__ import annotations

import re
from datetime import date
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


ACTION_PATTERN = re.compile(
    r"^[\s]*[-*]\s+"
    r"(?P<strike>~~)?"
    r"\*\*(?P<head>[^*]+)\*\*"
    r"(?:~~)?"
    r"(?P<tail>.*)",
)

NUMBERED_PATTERN = re.compile(
    r"^[\s]*\d+\.\s+"
    r"(?P<strike>~~)?"
    r"\*\*(?P<head>[^*]+)\*\*"
    r"(?:~~)?"
    r"(?P<tail>.*)",
)


def parse_action_items(text: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for line in text.splitlines():
        m = ACTION_PATTERN.match(line) or NUMBERED_PATTERN.match(line)
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

    seen: set[str] = set()
    deduped: list[dict[str, str]] = []
    for item in items:
        key = item["description"].strip().lower()
        if key not in seen:
            seen.add(key)
            deduped.append(item)
    return deduped


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


def extract_open_questions(body: str) -> list[str]:
    sections = parse_sections(body, level=2)
    for header, content in sections.items():
        if "open question" in header.lower():
            return parse_bullet_items(content)
    return []


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

def extract_date_from_title(title: str, year: int | None = None):
    today = date.today()
    if year is None:
        year = today.year

    m = _DATE_RE.search(title)
    if not m:
        return None
    month_num = _MONTH_MAP.get(m.group(1).lower())
    if month_num is None:
        return None
    try:
        result = date(year, month_num, int(m.group(2)))
    except ValueError:
        return None
    if (result - today).days > 60:
        try:
            result = result.replace(year=year - 1)
        except ValueError:
            return None
    return result
