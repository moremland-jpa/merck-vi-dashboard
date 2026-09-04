from __future__ import annotations

import hashlib
import hmac

import streamlit as st
from streamlit_cookies_controller import CookieController

_COOKIE_NAME = "merck_vi_auth"
_USER_COOKIE = "merck_vi_user"
_COOKIE_MAX_AGE = 30 * 24 * 60 * 60  # 30 days

TEAM_MEMBERS = [
    "Matt Oremland",
    "Grace Abrahams",
    "Cinnamon Walker-Thompson",
    "Talia Baghdoyan",
    "Colin Baughman",
    "Patrick Leyden",
    "Shannon Smith",
]


def _expected_token() -> str:
    pw = st.secrets.get("password", "")
    return hashlib.sha256(f"merck_vi_{pw}".encode()).hexdigest()[:24]


def _record_visit(username: str) -> None:
    if "previous_visit" not in st.session_state:
        import db

        prev = db.load_user_visit(username)
        st.session_state["previous_visit"] = prev
        db.save_user_visit(username)


_LOGIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Open+Sans:wght@400;600&display=swap');
[data-testid="stSidebarNav"] li:first-child {
    display: none !important;
}
[data-testid="stSidebarNav"]::before {
    content: "Merck V&I";
    display: block;
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #004153;
    padding: 0.25rem 0.75rem 0.5rem;
}
.login-box {
    max-width: 400px;
    margin: 4rem auto;
    padding: 2rem;
    text-align: center;
}
.login-box h2 {
    font-family: 'DM Serif Display', Georgia, serif;
    color: #004153;
    margin-bottom: 0.5rem;
}
.login-box p {
    color: #595959;
    font-size: 0.9rem;
}
</style>
"""


def check_password() -> bool:
    if "password" not in st.secrets:
        return True

    controller = CookieController()

    token = controller.get(_COOKIE_NAME)
    if token == _expected_token():
        user = controller.get(_USER_COOKIE)
        if user:
            st.session_state["current_user"] = user
            _record_visit(user)
            return True

        st.markdown(_LOGIN_CSS, unsafe_allow_html=True)
        st.markdown(
            '<div class="login-box">'
            "<h2>Welcome!</h2>"
            "<p>Select your name so we can track what's new for you.</p>"
            "</div>",
            unsafe_allow_html=True,
        )

        name = st.selectbox("Who are you?", TEAM_MEMBERS, key="user_picker")
        if st.button("Continue", type="primary"):
            controller.set(_USER_COOKIE, name, max_age=_COOKIE_MAX_AGE)
            st.session_state["current_user"] = name
            _record_visit(name)
            st.rerun()
        return False

    st.markdown(_LOGIN_CSS, unsafe_allow_html=True)
    st.markdown(
        '<div class="login-box">'
        "<h2>Merck V&I Dashboard</h2>"
        "<p>Enter the team password to continue.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Sign in", type="primary"):
        if hmac.compare_digest(password, st.secrets["password"]):
            controller.set(_COOKIE_NAME, _expected_token(), max_age=_COOKIE_MAX_AGE)
            st.rerun()
        else:
            st.error("Incorrect password.")

    return False
