"""
App.py

Entry point for the Air Quality Intelligence Dashboard.

Author: Ashish Kumar Mishra
"""

import streamlit as st

from dashboard import run_dashboard


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Air Quality Intelligence Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==========================================================
# APPLICATION
# ==========================================================

def main() -> None:
    """Launch the Streamlit application."""

    try:
        run_dashboard()

    except KeyboardInterrupt:
        st.warning("Application interrupted.")

    except Exception as error:
        st.error("⚠️ An unexpected error occurred.")
        with st.expander("Show technical details"):
            st.exception(error)


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":
    main()