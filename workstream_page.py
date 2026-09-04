from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

import brand
import db
import parsers
import utils


def _normalize_items(items: list[dict]) -> list[dict]:
    out = []
    for it in items:
        out.append(
            {
                "owner": it.get("owner", ""),
                "description": it.get("description", ""),
                "status": it.get("status", "Pending"),
                "due_date": it.get("due_date", ""),
                "completed_on": it.get("completed_on", ""),
                "notes": it.get("notes", ""),
            }
        )
    return out


_PENDING_COLS = {
    "done": st.column_config.CheckboxColumn("", width=50, default=False),
    "owner": st.column_config.TextColumn("Owner", width=120),
    "description": st.column_config.TextColumn("Description", width="large"),
    "due_date": st.column_config.DateColumn("Due", width=110, format="MMM D"),
    "notes": st.column_config.TextColumn("Notes", width="medium"),
}

_DONE_COLS = {
    "owner": st.column_config.TextColumn("Owner", width=120),
    "description": st.column_config.TextColumn("Description", width="large"),
    "notes": st.column_config.TextColumn("Notes", width="medium"),
    "completed_on": st.column_config.TextColumn("Completed", width=100),
}


def _render_action_items(workstream: str, ws: dict) -> None:
    items = _normalize_items(ws.get("action_items", []))
    base_hash = ws.get("action_items_base_hash", "")
    has_overlay = db.is_connected() and items != _normalize_items(
        ws.get("base_action_items", items)
    )

    if not items:
        st.info("No structured action items found. Check the raw status below.")
        with st.expander("Raw status content"):
            st.markdown(ws.get("raw_body", ""))
        return

    df = pd.DataFrame(items)
    pending = df[df["status"] == "Pending"].reset_index(drop=True)
    done = df[df["status"] == "Done"].reset_index(drop=True)

    if not pending.empty:
        st.markdown(f"### Pending ({len(pending)})")

        pending_display = pending[
            ["owner", "description", "due_date", "notes"]
        ].copy()
        pending_display.insert(0, "done", False)
        pending_display["due_date"] = pd.to_datetime(
            pending_display["due_date"], errors="coerce"
        ).dt.date

        edited = st.data_editor(
            pending_display,
            use_container_width=True,
            hide_index=True,
            num_rows="fixed",
            key=f"pending_{workstream}",
            column_config=_PENDING_COLS,
        )

        has_changes = not edited.equals(pending_display)
        if has_changes:
            if st.button(
                "Save changes", key=f"save_{workstream}", type="primary"
            ):
                updated = list(items)
                p_idx = 0
                today = date.today().isoformat()
                for j, item in enumerate(updated):
                    if item["status"] == "Pending" and p_idx < len(edited):
                        row = edited.iloc[p_idx]
                        marking_done = bool(row["done"])
                        due = row.get("due_date")
                        due_str = str(due) if pd.notna(due) else ""
                        updated[j] = {
                            **item,
                            "owner": str(row["owner"]),
                            "description": str(row["description"]),
                            "due_date": due_str,
                            "notes": str(
                                row["notes"] if pd.notna(row["notes"]) else ""
                            ),
                            "status": "Done" if marking_done else "Pending",
                            "completed_on": today if marking_done else "",
                        }
                        p_idx += 1
                if utils.save_action_items(workstream, updated, base_hash):
                    st.success("Changes saved.")
                    utils.load_workstream_status.clear()
                    utils.load_all_statuses.clear()
                    st.rerun()
                else:
                    st.error("Failed to save changes.")

    if not done.empty:
        st.markdown(f"### Completed ({len(done)})")
        st.dataframe(
            done[["owner", "description", "notes", "completed_on"]],
            use_container_width=True,
            hide_index=True,
            column_config=_DONE_COLS,
        )

    if has_overlay:
        if st.button(
            "Reset to source",
            key=f"reset_{workstream}",
            help="Discard cloud edits and reload from memory files",
        ):
            db.clear_action_overlay(workstream)
            utils.load_workstream_status.clear()
            utils.load_all_statuses.clear()
            st.rerun()


def _render_team_notes(workstream: str) -> None:
    user = st.session_state.get("current_user", "")

    if user and db.is_connected():
        with st.form(key=f"note_form_{workstream}", clear_on_submit=True):
            cols = st.columns([5, 1])
            with cols[0]:
                note_text = st.text_input(
                    "Quick update",
                    placeholder="Decision, observation, or update...",
                    label_visibility="collapsed",
                )
            with cols[1]:
                submitted = st.form_submit_button("Post")
            if submitted and note_text.strip():
                db.save_workstream_note(workstream, user, note_text.strip())
                st.rerun()

    notes = db.load_workstream_notes(workstream, limit=5)
    previous_visit = st.session_state.get("previous_visit")

    if notes:
        for note in notes:
            is_new = previous_visit and note.get("created_at", "") > previous_visit
            badge = ' <span class="new-badge">NEW</span>' if is_new else ""
            created = note.get("created_at", "")
            time_str = brand.relative_time(created) if created else ""

            st.markdown(
                f'<div style="padding:0.5rem 0; border-bottom:1px solid #EDE8C4;">'
                f'<span class="meta-text"><strong>{note["author"]}</strong>'
                f" &middot; {time_str}{badge}</span>"
                f"<br><span style='font-size:0.9rem;'>{note['content']}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
    elif not db.is_connected():
        st.caption("Connect Supabase to enable team notes.")


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

    if ws["description"]:
        st.markdown(f"*{ws['description']}*")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    tab_status, tab_actions, tab_people = st.tabs(
        ["Status", "Action Items", "Stakeholders"]
    )

    with tab_status:
        st.markdown("### Team Notes")
        _render_team_notes(workstream)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        if ws["current_state"]:
            st.markdown("## Current State")
            st.markdown(ws["current_state"])

        devs = ws.get("key_developments", [])
        if devs:
            st.markdown("## Key Developments")
            dated = []
            for title, content in devs:
                dt = parsers._extract_date_from_title(title)
                dated.append((dt, title, content))
            dated.sort(
                key=lambda x: (x[0] is not None, x[0] or date.min),
                reverse=True,
            )
            for dt, title, content in dated:
                date_str = dt.strftime("%b %d") if dt else ""
                label = f"{date_str} — {title}" if date_str else title
                with st.expander(label):
                    st.markdown(content)

        questions = ws.get("open_questions", [])
        if questions:
            st.markdown("## Open Questions")
            for q in questions:
                st.markdown(f"- {q}")

    with tab_actions:
        _render_action_items(workstream, ws)

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
