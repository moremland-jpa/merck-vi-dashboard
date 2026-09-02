from __future__ import annotations

import hmac

import streamlit as st


def check_password() -> bool:
    """Gate the app behind a password. Returns True if authenticated."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    if "password" not in st.secrets:
        return True

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Open+Sans:wght@400;600&display=swap');
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
        <div class="login-box">
            <h2>Merck V&I Dashboard</h2>
            <p>Enter the team password to continue.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Sign in", type="primary"):
        if hmac.compare_digest(password, st.secrets["password"]):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")

    return False
