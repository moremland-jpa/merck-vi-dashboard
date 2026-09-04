from __future__ import annotations

import streamlit as st

import auth
import brand
import db
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


def _render_whats_new() -> None:
    previous_visit = st.session_state.get("previous_visit")
    user = st.session_state.get("current_user", "")
    if not previous_visit or not user:
        return

    new_note_counts = db.count_new_notes_since(previous_visit)
    total_new_notes = sum(new_note_counts.values())

    statuses = utils.load_all_statuses()
    updated_ws = [
        ws
        for ws, data in statuses.items()
        if data.get("modified", "") and data["modified"] > previous_visit
    ]

    if not total_new_notes and not updated_ws:
        return

    parts = []
    if total_new_notes:
        parts.append(
            f"{total_new_notes} new team note{'s' if total_new_notes != 1 else ''}"
        )
    if updated_ws:
        parts.append(
            f"{len(updated_ws)} workstream update{'s' if len(updated_ws) != 1 else ''}"
        )

    summary = " and ".join(parts)

    st.markdown(
        f'<div class="card" style="border-left-color:{brand.ORANGE}; background:#FFF8F0;">'
        f'<h3 style="font-size:1rem; margin-bottom:0.3rem;">What\'s New</h3>'
        f'<p class="meta-text">Since your last visit: {summary}</p>'
        f"</div>",
        unsafe_allow_html=True,
    )

    if total_new_notes:
        recent_notes = db.load_workstream_notes(limit=5)
        new_notes = [
            n
            for n in recent_notes
            if n.get("created_at", "") > previous_visit
        ]
        for note in new_notes[:3]:
            ws = note.get("workstream", "")
            chip = brand.workstream_chip(ws)
            time_str = brand.relative_time(note.get("created_at", ""))
            st.markdown(
                f'{chip} <strong>{note["author"]}</strong> '
                f'<span class="meta-text">{time_str}</span>'
                f"<br><span style='font-size:0.9rem;'>{note['content']}</span>",
                unsafe_allow_html=True,
            )
        st.markdown('<hr class="divider">', unsafe_allow_html=True)


def render_overview() -> None:
    st.markdown("# Merck V&I Program Dashboard")
    st.markdown(
        '<p class="meta-text">Collaborative workspace for workstream status, '
        "action items, stakeholders, and milestones.</p>",
        unsafe_allow_html=True,
    )
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    _render_whats_new()

    previous_visit = st.session_state.get("previous_visit")
    new_note_counts = (
        db.count_new_notes_since(previous_visit) if previous_visit else {}
    )

    statuses = utils.load_all_statuses()

    cols = st.columns(2)
    for i, (ws_name, ws_data) in enumerate(statuses.items()):
        col = cols[i % 2]
        color = brand.WORKSTREAM_COLORS.get(ws_name, brand.TEAL)

        action_items = ws_data.get("action_items", [])
        pending = sum(1 for a in action_items if a.get("status") != "Done")
        done = sum(1 for a in action_items if a.get("status") == "Done")

        description = ws_data.get("description", "")
        modified = ws_data.get("modified", "")
        rel_time = brand.relative_time(modified) if modified else ""

        top_people = utils.get_stakeholders_for_workstream(ws_name, limit=3)
        people_html = ", ".join(top_people) if top_people else ""

        doc_count = utils.get_workstream_doc_count(ws_name)

        new_notes = new_note_counts.get(ws_name, 0)
        ws_updated = (
            previous_visit and modified and modified > previous_visit
        )

        body_parts = []
        if description:
            body_parts.append(f"<p>{description}</p>")

        badge_parts = []
        if new_notes:
            badge_parts.append(
                f"{new_notes} note{'s' if new_notes > 1 else ''}"
            )
        if ws_updated:
            badge_parts.append("status updated")
        if badge_parts:
            body_parts.append(
                f'<p><span class="new-badge">{", ".join(badge_parts)}</span></p>'
            )

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
            if st.button(
                f"View {ws_name} details",
                key=f"view_{ws_name}",
                icon=":material/arrow_forward:",
            ):
                st.session_state["selected_workstream"] = ws_name
                st.switch_page("pages/1_Workstreams.py")

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
        chip = brand.workstream_chip(ws_name)
        with st.expander(f"{title}", expanded=False, icon=":material/update:"):
            st.markdown(chip, unsafe_allow_html=True)
            st.markdown(content)


render_overview()
