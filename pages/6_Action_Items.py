from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

import auth
import brand
import db
import nav
import utils
from workstream_page import _normalize_items

st.set_page_config(
    page_title="Action Items", layout="wide", initial_sidebar_state="collapsed"
)
if not auth.check_password():
    st.stop()
brand.inject_brand_css()
nav.render_nav("Action Items")

st.markdown("# Action Items")
st.markdown(
    '<p class="meta-text">All action items across workstreams in one view. '
    "Edits sync back to individual workstream tabs.</p>",
    unsafe_allow_html=True,
)
st.markdown('<hr class="divider">', unsafe_allow_html=True)


def _load_all_items() -> tuple[list[dict], dict[str, str]]:
    statuses = utils.load_all_statuses()
    all_items: list[dict] = []
    base_hashes: dict[str, str] = {}
    for ws_name, ws_data in statuses.items():
        base_hashes[ws_name] = ws_data.get("action_items_base_hash", "")
        for item in _normalize_items(ws_data.get("action_items", [])):
            all_items.append({**item, "initiative": ws_name})
    return all_items, base_hashes


all_items, base_hashes = _load_all_items()

if not all_items:
    st.info("No action items found across workstreams.")
    st.stop()

df = pd.DataFrame(all_items)
pending = df[df["status"] == "Pending"].reset_index(drop=True)
done = df[df["status"] == "Done"].reset_index(drop=True)

if not pending.empty:
    st.markdown(f"### Pending ({len(pending)})")

    pending_display = pending[
        ["initiative", "owner", "description", "due_date", "notes"]
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
        key="master_pending",
        column_config={
            "done": st.column_config.CheckboxColumn("", width=50, default=False),
            "initiative": st.column_config.TextColumn(
                "Initiative", width=130, disabled=True
            ),
            "owner": st.column_config.TextColumn("Owner", width=120),
            "description": st.column_config.TextColumn(
                "Description", width="large"
            ),
            "due_date": st.column_config.DateColumn(
                "Due", width=110, format="MMM D"
            ),
            "notes": st.column_config.TextColumn("Notes", width="medium"),
        },
    )

    has_changes = not edited.equals(pending_display)
    if has_changes:
        if st.button("Save changes", key="master_save", type="primary"):
            ws_items: dict[str, list[dict]] = {
                ws: _normalize_items(data.get("action_items", []))
                for ws, data in utils.load_all_statuses().items()
            }
            ws_pending_idx: dict[str, int] = {ws: 0 for ws in ws_items}

            today = date.today().isoformat()
            orig_pending = pending.to_dict("records")

            for i, orig in enumerate(orig_pending):
                ws = orig["initiative"]
                row = edited.iloc[i]

                items = ws_items[ws]
                p_count = 0
                for j, item in enumerate(items):
                    if item["status"] != "Pending":
                        continue
                    if p_count == ws_pending_idx[ws]:
                        marking_done = bool(row["done"])
                        due = row.get("due_date")
                        due_str = str(due) if pd.notna(due) else ""
                        items[j] = {
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
                        ws_pending_idx[ws] += 1
                        break
                    p_count += 1

            ok = True
            for ws, items in ws_items.items():
                if not utils.save_action_items(
                    ws, items, base_hashes.get(ws, "")
                ):
                    ok = False

            if ok:
                st.success("Changes saved.")
                utils.load_workstream_status.clear()
                utils.load_all_statuses.clear()
                st.rerun()
            else:
                st.error("Failed to save some changes.")

if not done.empty:
    st.markdown(f"### Completed ({len(done)})")
    st.dataframe(
        done[["initiative", "owner", "description", "notes", "completed_on"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "initiative": st.column_config.TextColumn("Initiative", width=130),
            "owner": st.column_config.TextColumn("Owner", width=120),
            "description": st.column_config.TextColumn(
                "Description", width="large"
            ),
            "notes": st.column_config.TextColumn("Notes", width="medium"),
            "completed_on": st.column_config.TextColumn("Completed", width=100),
        },
    )
