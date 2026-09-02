from __future__ import annotations

import streamlit as st

import auth
import brand
import nav
import utils
import transcript_processor as tp

st.set_page_config(
    page_title="Process Transcript", layout="wide", initial_sidebar_state="collapsed"
)
if not auth.check_password():
    st.stop()
brand.inject_brand_css()
nav.render_nav("Process")

st.markdown("# Process Transcript")
st.markdown(
    '<p class="meta-text">'
    "Upload meeting transcripts or screenshots to extract updates for workstream "
    "status files. Changes are proposed first — you review and approve before "
    "anything is written."
    "</p>",
    unsafe_allow_html=True,
)

if "anthropic_api_key" not in st.secrets:
    st.warning(
        "Anthropic API key not configured. "
        "Add `anthropic_api_key` to `.streamlit/secrets.toml` or Streamlit Cloud secrets."
    )
    st.stop()

# ── Upload ──

uploaded = st.file_uploader(
    "Drop files here",
    type=["txt", "docx", "png", "jpg", "jpeg", "gif", "webp"],
    accept_multiple_files=True,
    help="Supports .txt, .docx transcripts and image screenshots (PNG, JPG, etc.)",
)

if uploaded and "transcript_result" not in st.session_state:
    images = [f for f in uploaded if tp.is_image(f.name)]
    docs = [f for f in uploaded if not tp.is_image(f.name)]

    file_summary_parts: list[str] = []
    if docs:
        file_summary_parts.append(f"{len(docs)} transcript{'s' if len(docs) != 1 else ''}")
    if images:
        file_summary_parts.append(f"{len(images)} screenshot{'s' if len(images) != 1 else ''}")
    st.markdown(f"**{', '.join(file_summary_parts)}** ready to process.")

    if st.button("Process", type="primary"):
        text = None
        if docs:
            with st.spinner("Extracting text..."):
                text_parts = []
                for doc in docs:
                    text_parts.append(tp.extract_text(doc))
                text = "\n\n---\n\n".join(text_parts)

            if text and text.strip():
                st.info(f"Extracted {len(text):,} characters from transcript(s).")

        if not text and not images:
            st.error("No usable content found in the uploaded files.")
            st.stop()

        with st.spinner("Analyzing with Claude (this may take 30-60 seconds)..."):
            try:
                result = tp.process_transcript(text=text, images=images or None)
            except Exception as e:
                st.error(f"Processing failed: {e}")
                result = None

        if result:
            st.session_state["transcript_result"] = result
            st.session_state["change_approvals"] = {
                i: True for i in range(len(result.get("changes", [])))
            }
            st.rerun()
        elif result is None:
            st.error("No results returned. Check your API key and try again.")

# ── Review ──

if "transcript_result" not in st.session_state:
    st.stop()

result = st.session_state["transcript_result"]

st.markdown("---")
st.markdown("### Meeting Summary")
st.markdown(result.get("transcript_summary", ""))

meta_parts: list[str] = []
if result.get("meeting_date"):
    meta_parts.append(f"**Date:** {result['meeting_date']}")
if result.get("workstreams_touched"):
    meta_parts.append(f"**Workstreams:** {', '.join(result['workstreams_touched'])}")
if meta_parts:
    st.markdown(" &nbsp;|&nbsp; ".join(meta_parts))

changes = result.get("changes", [])

if not changes:
    st.info("No actionable changes extracted from this transcript.")
    if st.button("Clear"):
        del st.session_state["transcript_result"]
        st.rerun()
    st.stop()

st.markdown(f"### Proposed Changes ({len(changes)})")
st.markdown(
    '<p class="meta-text">Uncheck any change you want to skip.</p>',
    unsafe_allow_html=True,
)

_TYPE_LABELS = {
    "update_current_state": "Update Status",
    "add_action_items": "New Action Items",
    "complete_action_items": "Complete Items",
    "add_key_development": "Key Development",
    "add_stakeholder": "New Stakeholder",
    "general_note": "Note",
}

approvals = st.session_state.get("change_approvals", {})

for i, change in enumerate(changes):
    label = _TYPE_LABELS.get(change.get("type", ""), change.get("type", ""))
    ws = change.get("workstream", change.get("file", ""))

    col_check, col_content = st.columns([0.05, 0.95])

    with col_check:
        approvals[i] = st.checkbox(
            "approve",
            value=approvals.get(i, True),
            key=f"approve_{i}",
            label_visibility="collapsed",
        )

    with col_content:
        with st.expander(f"**{label}** — {ws}", expanded=True):
            st.caption(change.get("reason", ""))

            ctype = change.get("type", "")

            if ctype == "update_current_state":
                st.markdown(change.get("new_content", ""))

            elif ctype == "add_action_items":
                for item in change.get("items", []):
                    owner = item.get("owner", "")
                    desc = item.get("description", "")
                    prefix = f"**{owner}:** " if owner else ""
                    st.markdown(f"- {prefix}{desc}")

            elif ctype == "complete_action_items":
                for desc in change.get("descriptions", []):
                    st.markdown(f"- ~~{desc}~~")

            elif ctype == "add_key_development":
                st.markdown(f"**{change.get('title', '')}**")
                st.markdown(change.get("content", ""))

            elif ctype == "add_stakeholder":
                p = change.get("person", {})
                st.markdown(
                    f"**{p.get('name', '')}** — {p.get('role', '')} "
                    f"({p.get('organization', '')})"
                )
                if p.get("notes"):
                    st.caption(p["notes"])

            elif ctype == "general_note":
                st.info(change.get("note", ""))

st.session_state["change_approvals"] = approvals

# ── Actions ──

st.markdown("---")
col_apply, col_discard = st.columns(2)

approved_count = sum(1 for v in approvals.values() if v)

with col_apply:
    if st.button(
        f"Apply {approved_count} change{'s' if approved_count != 1 else ''}",
        type="primary",
        disabled=approved_count == 0,
    ):
        applied = 0
        failed = 0
        for idx, change in enumerate(changes):
            if not approvals.get(idx, False):
                continue
            if change.get("type") == "general_note":
                applied += 1
                continue
            if tp.apply_change(change):
                applied += 1
            else:
                failed += 1

        utils.load_workstream_status.clear()
        utils.load_all_statuses.clear()
        utils.load_stakeholders.clear()

        if failed:
            st.warning(f"Applied {applied} changes, {failed} failed.")
        else:
            st.success(f"Applied {applied} changes.")

        del st.session_state["transcript_result"]
        del st.session_state["change_approvals"]
        st.rerun()

with col_discard:
    if st.button("Discard all"):
        del st.session_state["transcript_result"]
        del st.session_state["change_approvals"]
        st.rerun()
