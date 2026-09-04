from __future__ import annotations

import streamlit as st

import auth
import brand
import nav
import utils
import workstream_page

st.set_page_config(
    page_title="Workstreams", layout="wide", initial_sidebar_state="collapsed"
)
if not auth.check_password():
    st.stop()
brand.inject_brand_css()
nav.render_nav("Workstreams")

ws_names = list(utils.WORKSTREAMS.keys())
default = st.session_state.get("selected_workstream", ws_names[0])
idx = ws_names.index(default) if default in ws_names else 0

selected = st.selectbox(
    "Select workstream",
    ws_names,
    index=idx,
    key="ws_selector",
    label_visibility="collapsed",
)
st.session_state["selected_workstream"] = selected

workstream_page.render(selected)
