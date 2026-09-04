from __future__ import annotations

from datetime import datetime, timedelta

import plotly.express as px
import streamlit as st

import brand
import nav
import utils

import auth

st.set_page_config(page_title="Calendar & Timeline", layout="wide", initial_sidebar_state="collapsed")
if not auth.check_password():
    st.stop()
brand.inject_brand_css()
nav.render_nav("Calendar")

st.markdown("# Calendar & Timeline")

milestones = utils.load_milestones()
meetings = utils.load_meeting_cadence()
today = datetime.now().date()

# ── Gantt Timeline (top of page) ──

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("## Timeline")

if milestones:
    ws_options = sorted({m.get("workstream", "") for m in milestones})
    selected_ws = st.multiselect("Filter by workstream", ws_options, default=ws_options)

    timeline_data = []
    for m in milestones:
        ws = m.get("workstream", "")
        if ws not in selected_ws:
            continue
        try:
            start = datetime.strptime(m["date"], "%Y-%m-%d")
            end_str = m.get("end_date", m["date"])
            end = datetime.strptime(end_str, "%Y-%m-%d")
            if end <= start:
                end = start + timedelta(days=1)
            timeline_data.append(
                {
                    "Task": m["label"],
                    "Start": start,
                    "Finish": end,
                    "Workstream": ws,
                    "Type": m.get("type", "milestone"),
                }
            )
        except Exception:
            continue

    if timeline_data:
        color_map = {ws: brand.WORKSTREAM_COLORS.get(ws, brand.TEAL) for ws in ws_options}

        fig = px.timeline(
            timeline_data,
            x_start="Start",
            x_end="Finish",
            y="Task",
            color="Workstream",
            color_discrete_map=color_map,
        )

        fig.add_vline(
            x=datetime.combine(today, datetime.min.time()),
            line_dash="dash",
            line_color=brand.ORANGE,
            annotation_text="Today",
            annotation_position="top",
        )

        fig.update_layout(
            height=max(300, len(timeline_data) * 40 + 100),
            showlegend=True,
            xaxis_title="",
            yaxis_title="",
            font=dict(family="Open Sans, Arial, sans-serif"),
        )
        fig.update_yaxes(autorange="reversed")

        tasks = [d["Task"] for d in timeline_data]
        for i in range(len(tasks)):
            if i % 2 == 0:
                fig.add_hrect(
                    y0=i - 0.5,
                    y1=i + 0.5,
                    fillcolor="#F5F7F8",
                    layer="below",
                    line_width=0,
                )
            fig.add_hline(
                y=i + 0.5,
                line_color="#E0E0E0",
                line_width=0.5,
                layer="below",
            )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No timeline data matches the selected filters.")
else:
    st.info("No milestones configured.")

# ── Upcoming Deadlines & Milestones (equal-height cards via HTML flex) ──

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("## Upcoming Deadlines & Milestones")

if milestones:
    upcoming = []
    for m in milestones:
        try:
            d = datetime.strptime(m["date"], "%Y-%m-%d").date()
            if d >= today:
                m["_date"] = d
                m["_days_until"] = (d - today).days
                upcoming.append(m)
        except Exception:
            continue

    upcoming.sort(key=lambda x: x["_date"])

    if upcoming:
        cards_html = '<div style="display:flex; gap:1rem; flex-wrap:wrap;">'
        for m in upcoming[:6]:
            ws = m.get("workstream", "")
            color = brand.WORKSTREAM_COLORS.get(ws, brand.TEAL)
            days = m["_days_until"]
            days_label = "Today" if days == 0 else f"in {days} days"
            chip = brand.workstream_chip(ws)

            cards_html += (
                f'<div class="card" style="border-left-color:{color}; '
                f'flex:1 1 calc(33.33% - 1rem); min-width:220px;">'
                f'<p class="meta-text">{m["_date"].strftime("%b %d, %Y")} &middot; {days_label}</p>'
                f'<h3 style="font-size:1rem; margin-bottom:0.5rem;">{m["label"]}</h3>'
                f"{chip}"
                f"</div>"
            )
        cards_html += "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)
    else:
        st.info("No upcoming milestones.")
else:
    st.info("No milestones configured. Edit `data/milestones.json` to add deadlines.")

# ── Meeting Cadence (equal-height cards via HTML flex) ──

st.markdown('<hr class="divider">', unsafe_allow_html=True)

with st.expander("Meeting Cadence", expanded=False):
    if not meetings:
        st.info("No meeting cadence data found.")
    else:
        cards_html = '<div style="display:flex; gap:1rem; flex-wrap:wrap;">'
        for m in meetings:
            cadence = m.get("cadence", "")
            attendees = m.get("attendees", "")
            covers = m.get("covers", "")
            concluded = m.get("concluded", False)

            body = ""
            if cadence:
                body += f'<p class="meta-text"><strong>Cadence:</strong> {cadence}</p>'
            if covers:
                body += f"<p>{covers}</p>"
            if attendees:
                body += f'<p class="meta-text"><strong>Attendees:</strong> {attendees}</p>'

            if concluded:
                border_color = "#B0B0B0"
                extra_style = "background:#F0F0F0; opacity:0.7;"
            else:
                border_color = brand.CYAN
                extra_style = ""

            cards_html += (
                f'<div class="card" style="border-left-color:{border_color}; '
                f'{extra_style}'
                f'flex:1 1 calc(33.33% - 1rem); min-width:220px;">'
                f"<h3>{m.get('name', 'Meeting')}</h3>"
                f"{body}"
                f"</div>"
            )
        cards_html += "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)
