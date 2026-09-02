import streamlit as st

import auth
import brand
import nav
import workstream_page

st.set_page_config(page_title="Asset Reporting", layout="wide", initial_sidebar_state="collapsed")
if not auth.check_password():
    st.stop()
brand.inject_brand_css()
nav.render_nav("Asset Reporting")
workstream_page.render("Asset Reporting")
