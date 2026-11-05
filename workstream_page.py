from __future__ import annotations

from datetime import date

import streamlit as st

import brand
import db
import parsers
import utils




def _render_open_items(ws: dict) -> None:
    """Read-only list of open and completed items from the status file (no editing or check-off)."""
    items = ws.get("action_items", [])
    if not items:
        st.info("No open items listed in the status file.")
        return

    def line(item: dict) -> str:
        owner = f"**{item['owner']}:** " if item.get("owner") else ""
        return f"- {owner}{item['description']}"

    open_items = [i for i in items if i.get("status") != "Done"]
    done_items = [i for i in items if i.get("status") == "Done"]
    st.caption("From the status file, read-only. Status is tracked weekly in the Merck/JPA status tracker.")
    if open_items:
        st.markdown("\n".join(line(i) for i in open_items))
    else:
        st.caption("Nothing open.")
    if done_items:
        with st.expander(f"Completed ({len(done_items)})"):
            st.markdown("\n".join(line(i) for i in done_items))


def _render_single_update(note: dict, previous_visit: str | None) -> None:
    created = note.get("created_at", "")
    time_str = brand.relative_time(created) if created else ""

    category = brand.normalize_category(note.get("category"))
    cat_badge = brand.category_badge(category)
    cat_class = f"cat-{category.lower().replace(' ', '-')}"
    sync_label = brand.sync_indicator(note.get("synced_at"))

    safe_author = brand.safe(note.get("author"))
    safe_content = brand.safe(note.get("content"))

    st.markdown(
        f'<div class="update-item {cat_class}">'
        f"{cat_badge} "
        f'<span class="meta-text"><strong>{safe_author}</strong>'
        f" &middot; {time_str} &middot; {sync_label}</span>"
        f"<br><span style='font-size:0.9rem; margin-top:0.2rem; "
        f"display:inline-block;'>{safe_content}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )


def _render_team_updates(workstream: str) -> None:
    user = st.session_state.get("current_user", "")

    if user and db.is_connected():
        with st.form(key=f"update_form_{workstream}", clear_on_submit=True):
            note_text = st.text_area(
                "Share an update",
                placeholder="What's happening? Decisions, blockers, progress, things to raise with Merck...",
                label_visibility="collapsed",
                height=80,
            )
            cols = st.columns([5, 1])
            with cols[0]:
                category = st.radio(
                    "Category",
                    list(brand.UPDATE_CATEGORIES.keys()),
                    horizontal=True,
                    index=0,
                    label_visibility="collapsed",
                )
            with cols[1]:
                submitted = st.form_submit_button(
                    "Post", type="primary"
                )
            if submitted and note_text.strip():
                db.save_workstream_note(
                    workstream, user, note_text.strip(), category
                )
                st.rerun()
        st.caption(
            "**Tracker** notes go into the weekly Merck/JPA status tracker, so write them as you'd "
            "want Merck to read them. **Internal Note** stays with the JPA team."
        )

    notes = db.load_workstream_notes(workstream, limit=200)
    previous_visit = st.session_state.get("previous_visit")

    if notes:
        INITIAL_SHOW = 10
        for note in notes[:INITIAL_SHOW]:
            _render_single_update(note, previous_visit)

        remaining = notes[INITIAL_SHOW:]
        if remaining:
            with st.expander(f"Show {len(remaining)} earlier updates"):
                for note in remaining:
                    _render_single_update(note, previous_visit)
    elif not db.is_connected():
        st.caption("Connect Supabase to enable team updates.")


def render(workstream: str) -> None:
    color = brand.WORKSTREAM_COLORS[workstream]

    ws = utils.load_workstream_status(workstream)
    if not ws:
        st.error(f"Could not load {workstream} status data.")
        st.stop()

    st.markdown(f"# {workstream}")

    rel_time = brand.relative_time(ws["modified"]) if ws["modified"] else ""
    if rel_time:
        st.markdown(
            f'{brand.status_badge("Active", color)} '
            f'<span class="meta-text">Updated {rel_time}</span>',
            unsafe_allow_html=True,
        )

    summary = brand.summary_html(parsers.summary_items(ws.get("summary"), ws.get("description", "")))
    if summary:
        st.markdown(summary, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    tab_status, tab_items, tab_people = st.tabs(
        ["Status", "Open Items", "Stakeholders"]
    )

    with tab_status:
        st.markdown("### Team Updates")
        _render_team_updates(workstream)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        if ws["current_state"]:
            st.markdown("## Current State")
            st.markdown(ws["current_state"])

        devs = ws.get("key_developments", [])
        if devs:
            st.markdown("## Key Developments")
            parsed = []
            for title, content in devs:
                dt = parsers.extract_date_from_title(title)
                parsed.append((dt, title, content))
            parsed.sort(
                key=lambda x: (x[0] is not None, x[0] or date.min),
                reverse=True,
            )
            dated_items = [(dt, t, c) for dt, t, c in parsed if dt]
            undated_items = [(dt, t, c) for dt, t, c in parsed if not dt]

            if dated_items:
                with st.container(border=True):
                    for dt, title, content in dated_items:
                        label = f"{dt.strftime('%b %d')} — {title}"
                        with st.expander(label, icon=":material/event:"):
                            st.markdown(content)

            if undated_items:
                if dated_items:
                    st.caption("Other topics")
                for _, title, content in undated_items:
                    with st.expander(title):
                        st.markdown(content)

        questions = ws.get("open_questions", [])
        if questions:
            st.markdown("## Open Questions")
            for q in questions:
                st.markdown(f"- {q}")

    with tab_items:
        _render_open_items(ws)

    with tab_people:
        people = utils.load_stakeholders()
        if not people.empty:
            ws_people = people[
                people["Workstreams"].str.contains(
                    workstream, case=False, na=False
                )
            ]
            if not ws_people.empty:
                st.dataframe(
                    ws_people[["Person", "Role", "Notes", "Organization"]],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info(f"No stakeholders tagged with '{workstream}'.")
        else:
            st.warning("Stakeholder data not available.")
