from __future__ import annotations

import html

import streamlit as st

TEAL = "#004153"
ORANGE = "#E37222"
CYAN = "#00B3BE"
DARK_TEAL = "#002D36"
CREAM = "#EDE8C4"
LIGHT_GRAY = "#F5F7F8"
MID_GRAY = "#595959"

WORKSTREAM_COLORS = {
    "Congress AI": TEAL,
    "Genesis": CYAN,
    "MRL Debrief": ORANGE,
    "Asset Reporting": DARK_TEAL,
}

WORKSTREAM_BG_COLORS = {
    "Congress AI": "#E8F1F3",
    "Genesis": "#E0F7FA",
    "MRL Debrief": "#FFF0E5",
    "Asset Reporting": "#E8ECEE",
}

UPDATE_CATEGORIES = {
    "Update":      ("&#x1F4AC;", "#004153", "#E8F1F3"),
    "Decision":    ("&#x2705;",  "#1B7A2B", "#E6F4EA"),
    "Blocker":     ("&#x1F6A8;", "#C62828", "#FDECEA"),
    "Action Item": ("&#x1F3AF;", "#E37222", "#FFF0E5"),
    "FYI":         ("&#x1F4CB;", "#595959", "#F5F5F5"),
}


def safe(text) -> str:
    if not text:
        return ""
    return html.escape(str(text))


def inject_brand_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Open+Sans:wght@300;400;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Open Sans', Arial, sans-serif;
        }

        h1, h2, h3, h4, h5, h6,
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3 {
            font-family: 'DM Serif Display', Georgia, serif;
            color: #004153;
        }

        [data-testid="stSidebar"] {
            border-right: 2px solid #EDE8C4;
        }

        .card {
            background: #FFFFFF;
            border-radius: 8px;
            padding: 1.25rem 1.5rem;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
            border-left: 4px solid #004153;
            margin-bottom: 1rem;
            transition: box-shadow 0.2s;
        }
        .card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        }
        .card h3 {
            margin: 0 0 0.5rem 0;
            font-size: 1.15rem;
        }
        .card p {
            margin: 0.25rem 0;
            color: #595959;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        .chip {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-right: 4px;
            margin-bottom: 4px;
        }

        .status-badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .meta-text {
            color: #595959;
            font-size: 0.8rem;
        }

        .divider {
            border: none;
            border-top: 2px solid #EDE8C4;
            margin: 1.5rem 0;
        }

        .stat-number {
            font-family: 'Open Sans', Arial, sans-serif;
            font-weight: 800;
            font-size: 2rem;
            line-height: 1;
        }
        .stat-label {
            font-size: 0.8rem;
            color: #595959;
            margin-top: 0.25rem;
        }

        .update-item {
            padding: 0.6rem 0.75rem;
            border-left: 3px solid #EDE8C4;
            margin-bottom: 0.5rem;
            border-radius: 0 4px 4px 0;
        }
        .update-item.cat-update { border-left-color: #004153; }
        .update-item.cat-decision { border-left-color: #1B7A2B; }
        .update-item.cat-blocker { border-left-color: #C62828; }
        .update-item.cat-action-item { border-left-color: #E37222; }
        .update-item.cat-fyi { border-left-color: #595959; }

        .sync-dot {
            display: inline-block;
            font-size: 0.7rem;
            margin-left: 0.3rem;
            vertical-align: middle;
            cursor: default;
        }

        .new-badge {
            display: inline-block;
            padding: 1px 7px;
            border-radius: 3px;
            font-size: 0.65rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            background: #E37222;
            color: #FFFFFF;
            margin-left: 0.25rem;
            vertical-align: middle;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_card(
    title: str,
    body_html: str,
    border_color: str = TEAL,
) -> str:
    return (
        f'<div class="card" style="border-left-color: {border_color};">'
        f"<h3>{safe(title)}</h3>"
        f"{body_html}"
        f"</div>"
    )


def workstream_chip(name: str) -> str:
    color = WORKSTREAM_COLORS.get(name, TEAL)
    bg = WORKSTREAM_BG_COLORS.get(name, LIGHT_GRAY)
    return f'<span class="chip" style="background:{bg}; color:{color};">{safe(name)}</span>'


def status_badge(label: str, color: str = TEAL) -> str:
    return (
        f'<span class="status-badge" style="background:{color}15; color:{color};">'
        f"{safe(label)}</span>"
    )


def category_badge(category: str) -> str:
    icon, fg, bg = UPDATE_CATEGORIES.get(category, UPDATE_CATEGORIES["Update"])
    return (
        f'<span class="chip" style="background:{bg}; color:{fg}; '
        f'font-size:0.72rem; padding:2px 8px;">'
        f'{icon} {safe(category)}</span>'
    )


def sync_indicator(synced_at: str | None) -> str:
    if synced_at:
        return '<span class="sync-dot" style="color:#1B7A2B;">&#x2714; synced</span>'
    return '<span class="sync-dot" style="color:#9EA7B3;">pending</span>'


def relative_time(iso_str: str) -> str:
    from datetime import datetime, timezone

    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        delta = now - dt
        days = delta.days
        if days == 0:
            hours = delta.seconds // 3600
            if hours == 0:
                return "just now"
            return f"{hours}h ago"
        if days == 1:
            return "yesterday"
        if days < 30:
            return f"{days}d ago"
        months = days // 30
        return f"{months}mo ago"
    except Exception:
        return ""
