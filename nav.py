from __future__ import annotations

import streamlit as st

NAV_ITEMS = [
    ("Overview", "app.py"),
    ("Workstreams", "pages/1_Workstreams.py"),
    ("Action Items", "pages/6_Action_Items.py"),
    ("Calendar", "pages/5_Calendar.py"),
    ("Stakeholders", "pages/7_Stakeholders.py"),
]


def render_nav(active: str = "Overview") -> None:
    active_idx = next(
        (i for i, (label, _) in enumerate(NAV_ITEMS) if label == active), -1
    )
    nth = active_idx + 1  # CSS nth-child is 1-based

    st.markdown(
        f"""
        <style>
        /* ── Nav bar layout ── */
        div[data-testid="stHorizontalBlock"]:first-of-type {{
            gap: 0.4rem !important;
            margin-bottom: 0.75rem !important;
        }}
        div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="stColumn"] {{
            padding: 0 !important;
            flex: 1 1 0% !important;
            min-width: 0 !important;
            width: 0 !important;
        }}

        /* ── Force all wrappers inside nav columns to fill width ── */
        div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stElementContainer"] {{
            width: 100% !important;
        }}
        div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stPageLink"] {{
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
        }}
        div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stPageLink"] > div {{
            width: 100% !important;
        }}
        div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stPageLink"] a {{
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            box-sizing: border-box !important;
            width: 100% !important;
            height: 40px !important;
            padding: 0 0.25rem !important;
            margin: 0 !important;
            font-family: 'Open Sans', Arial, sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.8rem !important;
            letter-spacing: 0.02em !important;
            color: #FFFFFF !important;
            background: linear-gradient(180deg, #00607a 0%, #004153 50%, #003040 100%) !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 6px rgba(0,65,83,0.35), inset 0 1px 0 rgba(255,255,255,0.2) !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            text-decoration: none !important;
            transition: background 0.2s, box-shadow 0.2s !important;
        }}
        div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stPageLink"] a:hover {{
            background: linear-gradient(180deg, #007a99 0%, #005a6e 50%, #004153 100%) !important;
            box-shadow: 0 4px 12px rgba(0,65,83,0.45), inset 0 1px 0 rgba(255,255,255,0.25) !important;
        }}
        div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stPageLink"] a span {{
            color: #FFFFFF !important;
            font-weight: 600 !important;
            margin: 0 !important;
            line-height: 1 !important;
        }}
        div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stPageLink"] a p {{
            color: #FFFFFF !important;
            font-weight: 600 !important;
            margin: 0 !important;
            line-height: 1 !important;
        }}

        /* ── Active tile (nth-child targets the active column) ── */
        div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="stColumn"]:nth-child({nth}) div[data-testid="stPageLink"] a {{
            background: linear-gradient(180deg, #f5922e 0%, #E37222 45%, #c4601a 100%) !important;
            box-shadow: 0 2px 8px rgba(227,114,34,0.4), inset 0 1px 0 rgba(255,255,255,0.3) !important;
            border: 1px solid rgba(255,255,255,0.12) !important;
            cursor: default !important;
        }}
        div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="stColumn"]:nth-child({nth}) div[data-testid="stPageLink"] a:hover {{
            background: linear-gradient(180deg, #f5922e 0%, #E37222 45%, #c4601a 100%) !important;
            box-shadow: 0 2px 8px rgba(227,114,34,0.4), inset 0 1px 0 rgba(255,255,255,0.3) !important;
        }}
        div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="stColumn"]:nth-child({nth}) div[data-testid="stPageLink"] a span {{
            font-weight: 700 !important;
        }}

        /* ── Sidebar: rename "app" to "Merck V&I" ── */
        [data-testid="stSidebarNav"] li:first-child {{
            display: none !important;
        }}
        [data-testid="stSidebarNav"]::before {{
            content: "Merck V&I";
            display: block;
            font-family: 'DM Serif Display', Georgia, serif;
            font-size: 1.2rem;
            font-weight: 700;
            color: #004153;
            padding: 0.25rem 0.75rem 0.5rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(len(NAV_ITEMS))
    for i, (label, page_file) in enumerate(NAV_ITEMS):
        with cols[i]:
            st.page_link(page_file, label=label)
