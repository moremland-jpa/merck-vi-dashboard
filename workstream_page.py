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
        out.append({
            "owner": it.get("owner", ""),
            "description": it.get("description", ""),
            "status": it.get("status", "Pending"),
            "completed_on": it.get("completed_on", ""),
            "notes": it.get("notes", ""),
        })
    return out


_PENDING_COLS = {
    "done": st.column_config.CheckboxColumn("", width=50, default=False),
    "owner": st.column_config.TextColumn("Owner", width=120),
    "description": st.column_config.TextColumn("Description", width="large"),
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
    has_overlay = (
        db.is_connected()
        and items != _normalize_items(ws.get("base_action_items", items))
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

        pending_display = pending[["owner", "description", "notes"]].copy()
        pending_display.insert(0, "done", False)

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
            if st.button("Save changes", key=f"save_{workstream}", type="primary"):
                updated = list(items)
                p_idx = 0
                today = date.today().isoformat()
                for j, item in enumerate(updated):
                    if item["status"] == "Pending" and p_idx < len(edited):
                        row = edited.iloc[p_idx]
                        marking_done = bool(row["done"])
                        updated[j] = {
                            **item,
                            "owner": str(row["owner"]),
                            "description": str(row["description"]),
                            "notes": str(row["notes"] if pd.notna(row["notes"]) else ""),
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

_STATUS_COLORS = {
    "Blocked": ("#DC2626", "#FEE2E2"),
    "Waiting": ("#E37222", "#FFF0E5"),
    "Active": ("#00857C", "#E0F7FA"),
    "Done": ("#595959", "#F0F0F0"),
}


def _dev_zone_css() -> str:
    return """
    <style>
    .dev-timeline {
        position: relative;
        padding-left: 2.5rem;
        margin: 0.5rem 0 1.5rem 0;
    }
    .dev-timeline::before {
        content: '';
        position: absolute;
        left: 0.55rem;
        top: 0.5rem;
        bottom: 0.5rem;
        width: 2px;
        background: #EDE8C4;
    }
    .dev-event {
        position: relative;
        padding-bottom: 0.75rem;
    }
    .dev-event:last-child { padding-bottom: 0; }
    .dev-dot {
        position: absolute;
        left: -2.05rem;
        top: 0.2rem;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        box-sizing: border-box;
    }
    .dev-dot.past { background: var(--dot-color); }
    .dev-dot.upcoming {
        background: transparent;
        border: 2.5px solid var(--dot-color);
    }
    .dev-event-header {
        display: flex;
        align-items: baseline;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    .dev-event-date {
        font-family: 'Open Sans', Arial, sans-serif;
        font-size: 0.75rem;
        font-weight: 700;
        color: #595959;
        min-width: 4.5rem;
    }
    .dev-event-title {
        font-family: 'DM Serif Display', Georgia, serif;
        font-size: 0.95rem;
        color: #004153;
    }
    .dev-event-summary {
        font-size: 0.8rem;
        color: #595959;
        line-height: 1.4;
        margin-top: 0.15rem;
    }
    .dev-spawn-badge {
        display: inline-block;
        font-size: 0.65rem;
        color: #595959;
        background: #F5F7F8;
        border: 1px solid #EDE8C4;
        border-radius: 3px;
        padding: 0 5px;
        margin-left: 0.25rem;
        vertical-align: baseline;
    }

    .dev-thread {
        display: flex;
        align-items: flex-start;
        gap: 0.6rem;
        padding: 0.5rem 0.75rem;
        border-left: 3px solid;
        border-radius: 0 6px 6px 0;
        margin-bottom: 0.4rem;
        background: #FAFBFC;
        min-height: 44px;
    }
    .dev-thread-status {
        display: inline-block;
        padding: 1px 8px;
        border-radius: 4px;
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        flex-shrink: 0;
        margin-top: 2px;
    }
    .dev-thread-body { flex: 1; min-width: 0; }
    .dev-thread-title {
        font-weight: 600;
        font-size: 0.88rem;
        color: #004153;
        line-height: 1.3;
    }
    .dev-thread-summary {
        font-size: 0.78rem;
        color: #595959;
        line-height: 1.4;
        margin-top: 0.1rem;
    }
    .dev-provenance {
        display: inline-block;
        padding: 0 6px;
        border-radius: 3px;
        font-size: 0.62rem;
        background: #EDE8C4;
        color: #595959;
        margin-left: 0.35rem;
        vertical-align: middle;
    }
    </style>
    """


def _render_timeline(
    events: list[dict], threads: list[dict], accent: str
) -> None:
    if not events:
        return
    st.markdown("### Events")
    html = f'<div class="dev-timeline" style="--dot-color:{accent};">'
    for ev in events:
        date_str = ev["date"].strftime("%b %d")
        css_class = "past" if ev.get("is_past") else "upcoming"

        spawn_count = ev.get("_spawn_count", 0)
        spawn_html = ""
        if spawn_count > 0:
            spawn_html = (
                f' <span class="dev-spawn-badge">'
                f'{spawn_count} thread{"s" if spawn_count != 1 else ""}'
                f"</span>"
            )

        summary_html = ""
        if ev.get("summary"):
            summary_html = f'<div class="dev-event-summary">{ev["summary"]}</div>'
        html += (
            f'<div class="dev-event">'
            f'<div class="dev-dot {css_class}"></div>'
            f'<div class="dev-event-header">'
            f'<span class="dev-event-date">{date_str}</span>'
            f'<span class="dev-event-title">{ev["title"]}{spawn_html}</span>'
            f"</div>"
            f"{summary_html}"
            f"</div>"
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def _render_threads(threads: list[dict], accent: str) -> None:
    if not threads:
        return

    first_active_idx = next(
        (
            i
            for i, t in enumerate(threads)
            if t["status"] in ("Blocked", "Waiting", "Active")
        ),
        -1,
    )

    # Status filter when many threads
    if len(threads) > 6:
        statuses = sorted({t["status"] for t in threads})
        selected = st.multiselect(
            "Filter threads by status",
            statuses,
            default=[s for s in statuses if s != "Done"],
            key="thread_status_filter",
        )
        visible = [t for t in threads if t["status"] in selected]
    else:
        visible = threads

    st.markdown(
        f"### Open Threads"
        f' <span class="meta-text">({len(visible)} of {len(threads)})</span>',
        unsafe_allow_html=True,
    )

    for idx, t in enumerate(visible):
        status = t["status"]
        fg, bg = _STATUS_COLORS.get(status, ("#595959", "#F0F0F0"))

        prov_html = ""
        if t.get("provenance"):
            prov_html = f'<span class="dev-provenance">From {t["provenance"]}</span>'

        summary_text = t.get("summary", "")
        summary_html = ""
        if summary_text:
            summary_html = f'<div class="dev-thread-summary">{summary_text}</div>'

        html = (
            f'<div class="dev-thread" style="border-left-color:{fg};">'
            f'<span class="dev-thread-status" style="background:{bg}; color:{fg};">{status}</span>'
            f'<div class="dev-thread-body">'
            f'<span class="dev-thread-title">{t["title"]}</span>'
            f"{prov_html}"
            f"{summary_html}"
            f"</div></div>"
        )
        st.markdown(html, unsafe_allow_html=True)

        is_first_active = threads.index(t) == first_active_idx
        with st.expander(
            f"Details",
            expanded=is_first_active,
        ):
            st.markdown(t["content"])


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
        if ws["current_state"]:
            st.markdown("## Current State")
            st.markdown(ws["current_state"])

        devs = ws.get("key_developments", [])
        if devs:
            st.markdown("## Key Developments")
            st.markdown(_dev_zone_css(), unsafe_allow_html=True)

            events, threads = parsers.classify_key_developments(devs)

            # Count how many threads reference each event for spawn badges
            for ev in events:
                ev_words = (
                    ev["title"]
                    .split("/")[0]
                    .split("(")[0]
                    .strip()
                    .lower()
                    .split()
                )
                count = 0
                for t in threads:
                    prov = t.get("provenance", "").lower()
                    if prov and any(w in prov for w in ev_words if len(w) > 3):
                        count += 1
                ev["_spawn_count"] = count

            # Show most recent events (last 8) on timeline
            recent_events = events[-8:] if len(events) > 8 else events
            _render_timeline(recent_events, threads, color)
            _render_threads(threads, color)

            # Older events in a separate expander if many
            older = events[: -8] if len(events) > 8 else []
            if older:
                with st.expander(
                    f"Earlier events ({len(older)} more)", expanded=False
                ):
                    for ev in older:
                        date_str = ev["date"].strftime("%b %d")
                        st.markdown(
                            f"**{date_str}** — {ev['title']}  \n"
                            f"<span class='meta-text'>{ev.get('summary', '')}</span>",
                            unsafe_allow_html=True,
                        )

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
                people["Workstreams"].str.contains(workstream, case=False, na=False)
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
