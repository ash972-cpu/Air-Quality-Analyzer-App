"""
components.py

Reusable Streamlit UI Components.

Author: Ashish Kumar Mishra
"""

from typing import Dict

import streamlit as st


# ==========================================================
# WEATHER CARD
# ==========================================================

def weather_card(weather: Dict) -> None:
    """
    Display the current weather metrics.
    """

    st.markdown("### 🌤 Current Weather")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🌡 Temperature",
            f"{weather['temperature_2m']:.1f}°C",
        )

    with col2:
        st.metric(
            "💧 Humidity",
            f"{weather['relative_humidity_2m']}%",
        )

    with col3:
        st.metric(
            "🌬 Wind Speed",
            f"{weather['wind_speed_10m']} km/h",
        )


# ==========================================================
# AQI STATUS BADGE
# ==========================================================

def status_badge(status, color):

    st.markdown(
        f"""
<div style="
background:{color};
padding:18px;
border-radius:18px;
font-size:28px;
font-weight:700;
text-align:center;
color:black;
box-shadow:0 8px 25px rgba(0,0,0,.25);
margin-bottom:20px;
">

🌍 Current Air Quality

<br><br>

{status}

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# HEALTH SCORE CARD
# ==========================================================

def health_card(score: int) -> None:
    """
    Display the health score with a remark.
    """

    if score >= 80:
        remark = "🟢 Excellent"

    elif score >= 60:
        remark = "🟡 Good"

    elif score >= 40:
        remark = "🟠 Moderate"

    else:
        remark = "🔴 Poor"

    st.info(
        f"""
### ❤️ Health Score

**{score}/100**

{remark}
"""
    )


# ==========================================================
# AI RESPONSE PANEL
# ==========================================================

def ai_panel(ai_text: str) -> None:
    """
    Display AI recommendations inside an expandable panel.
    """

    with st.expander(
        "🤖 AI Health Advisor",
        expanded=True,
    ):
        st.markdown(ai_text)


# ==========================================================
# SECTION HEADER
# ==========================================================

def section_header(title: str) -> None:
    """
    Display a section title with a divider.
    """

    st.subheader(title)
    st.divider()


# ==========================================================
# FOOTER
# ==========================================================
def footer():

    st.markdown(
        """
<div class="footer">

<hr>

<h4>🌍 Air Quality Intelligence Dashboard</h4>

<p>
Made with ❤️ by <b>Ashish Kumar Mishra</b>
</p>

<p>
Powered by Streamlit • Groq AI • Open-Meteo API
</p>

</div>
""",
        unsafe_allow_html=True,
    )
# ==========================================================
# PUBLIC EXPORTS
# ==========================================================

__all__ = [
    "weather_card",
    "status_badge",
    "health_card",
    "ai_panel",
    "section_header",
    "footer",
]