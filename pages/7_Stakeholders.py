from __future__ import annotations

import streamlit as st

import brand
import nav
import utils

import auth

st.set_page_config(page_title="Stakeholders", layout="wide", initial_sidebar_state="collapsed")
if not auth.check_password():
    st.stop()
brand.inject_brand_css()
nav.render_nav("Stakeholders")

st.markdown("# Stakeholder Directory")

df = utils.load_stakeholders()

if df.empty:
    st.warning("No stakeholder data found. Check that the memory file exists.")
    st.stop()

total = len(df)
orgs = df["Organization"].nunique()
st.markdown(
    f'<p class="meta-text">{total} stakeholders across {orgs} organizations</p>',
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    search = st.text_input("Search", placeholder="Name, role, or keyword...")

with col2:
    org_options = sorted(df["Organization"].unique().tolist())
    org_filter = st.multiselect("Organization", org_options)

with col3:
    ws_options = sorted(
        {ws for ws_list in df["Workstreams"].dropna() for ws in ws_list.split(",") if ws.strip()}
    )
    ws_filter = st.multiselect("Workstream", ws_options)

filtered = df.copy()

if search:
    mask = (
        filtered["Person"].str.contains(search, case=False, na=False)
        | filtered["Role"].str.contains(search, case=False, na=False)
        | filtered["Notes"].str.contains(search, case=False, na=False)
    )
    filtered = filtered[mask]

if org_filter:
    filtered = filtered[filtered["Organization"].isin(org_filter)]

if ws_filter:
    mask = filtered["Workstreams"].apply(
        lambda x: any(ws in str(x) for ws in ws_filter)
    )
    filtered = filtered[mask]

st.markdown(f"**Showing {len(filtered)} of {total} stakeholders**")

st.dataframe(
    filtered[["Person", "Role", "Workstreams", "Notes", "Organization"]],
    use_container_width=True,
    hide_index=True,
    column_config={
        "Person": st.column_config.TextColumn("Person", width="medium"),
        "Role": st.column_config.TextColumn("Role", width="large"),
        "Workstreams": st.column_config.TextColumn("Workstreams", width="medium"),
        "Notes": st.column_config.TextColumn("Notes", width="large"),
        "Organization": st.column_config.TextColumn("Organization", width="medium"),
    },
)
