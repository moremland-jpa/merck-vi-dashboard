import streamlit as st

import auth
import brand
import nav
import workstream_page

st.set_page_config(page_title="MRL Debrief", layout="wide", initial_sidebar_state="collapsed")
if not auth.check_password():
    st.stop()
brand.inject_brand_css()
nav.render_nav("MRL Debrief")
workstream_page.render("MRL Debrief")
