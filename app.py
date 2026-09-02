from __future__ import annotations

import streamlit as st

import auth
import brand
import nav
import utils

st.set_page_config(
    page_title="Merck V&I Program Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if not auth.check_password():
    st.stop()

brand.inject_brand_css()
nav.render_nav(active="Overview")


def render_overview() -> None:
    st.markdown("# Merck V&I Program Dashboard")
    st.markdown(
        '<p class="meta-text">Read-only view of workstream status, '
        "stakeholders, documents, and milestones. Data refreshes from "
        "memory files within 60 seconds of update.</p>",
        unsafe_allow_html=True,
    )
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    statuses = utils.load_all_statuses()

    cols = st.columns(2)
    for i, (ws_name, ws_data) in enumerate(statuses.items()):
        col = cols[i % 2]
        color = brand.WORKSTREAM_COLORS.get(ws_name, brand.TEAL)
        bg = brand.WORKSTREAM_BG_COLORS.get(ws_name, brand.LIGHT_GRAY)

        action_items = ws_data.get("action_items", [])
        pending = sum(1 for a in action_items if a.get("status") != "Done")
        done = sum(1 for a in action_items if a.get("status") == "Done")

        description = ws_data.get("description", "")
        modified = ws_data.get("modified", "")
        rel_time = brand.relative_time(modified) if modified else ""

        top_people = utils.get_stakeholders_for_workstream(ws_name, limit=3)
        people_html = ", ".join(top_people) if top_people else ""

        doc_count = utils.get_workstream_doc_count(ws_name)

        body_parts = []
        if description:
            body_parts.append(f"<p>{description}</p>")

        meta_parts = []
        if rel_time:
            meta_parts.append(f"Updated {rel_time}")
        if pending:
            meta_parts.append(
                f'<span style="color:{brand.ORANGE};font-weight:600;">'
                f"{pending} pending</span> action items"
            )
        if done:
            meta_parts.append(f"{done} completed")
        if doc_count:
            meta_parts.append(f"{doc_count} documents")
        if meta_parts:
            body_parts.append(
                f'<p class="meta-text">{" &middot; ".join(meta_parts)}</p>'
            )

        if people_html:
            body_parts.append(
                f'<p class="meta-text"><strong>Key stakeholders:</strong> {people_html}</p>'
            )

        body_html = "\n".join(body_parts)
        card_html = brand.render_card(ws_name, body_html, border_color=color)

        with col:
            st.markdown(card_html, unsafe_allow_html=True)
            page_map = {
                "Congress AI": "pages/1_Congress_AI.py",
                "Genesis": "pages/2_Genesis.py",
                "MRL Debrief": "pages/3_MRL_Debrief.py",
                "Asset Reporting": "pages/4_Asset_Reporting.py",
            }
            st.page_link(page_map[ws_name], label=f"View {ws_name} details", icon=":material/arrow_forward:")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    render_recent_activity(statuses)


def render_recent_activity(statuses: dict[str, dict]) -> None:
    st.markdown("## Recent Activity")

    all_devs: list[tuple[str, str, str]] = []
    for ws_name, ws_data in statuses.items():
        for title, content in ws_data.get("key_developments", []):
            all_devs.append((ws_name, title, content))

    if not all_devs:
        st.info("No recent developments found in memory files.")
        return

    for ws_name, title, content in all_devs[-5:]:
        color = brand.WORKSTREAM_COLORS.get(ws_name, brand.TEAL)
        chip = brand.workstream_chip(ws_name)
        with st.expander(f"{title}", expanded=False, icon=":material/update:"):
            st.markdown(chip, unsafe_allow_html=True)
            st.markdown(content)


render_overview()
