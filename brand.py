from __future__ import annotations

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
        f"<h3>{title}</h3>"
        f"{body_html}"
        f"</div>"
    )


def workstream_chip(name: str) -> str:
    color = WORKSTREAM_COLORS.get(name, TEAL)
    bg = WORKSTREAM_BG_COLORS.get(name, LIGHT_GRAY)
    return f'<span class="chip" style="background:{bg}; color:{color};">{name}</span>'


def status_badge(label: str, color: str = TEAL) -> str:
    return (
        f'<span class="status-badge" style="background:{color}15; color:{color};">'
        f"{label}</span>"
    )


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
