"""
charts.py

Professional Plotly charts for the Air Quality Dashboard.

Author: Ashish Kumar Mishra
"""

from typing import Dict

import plotly.graph_objects as go

from utils.helpers import get_aqi_status

# ==========================================================
# COMMON CHART STYLE
# ==========================================================


def style_chart(fig: go.Figure, height: int = 350) -> go.Figure:
    """
    Apply a common theme to all Plotly charts.
    """

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(color="white", size=14),
        height=height,
    )

    return fig


# ==========================================================
# AQI GAUGE
# ==========================================================


def create_gauge(aqi: float) -> go.Figure:
    """
    Create an AQI speedometer gauge.
    """

    status, color = get_aqi_status(aqi)

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=aqi,
            number={"font": {"size": 58}},
            title={
                "text": f"<b>{status}</b>",
                "font": {"size": 24, "color": color},
            },
            gauge={
                "axis": {
                    "range": [0, 500],
                    "tickwidth": 2,
                    "tickcolor": "white",
                },
                "bar": {
                    "color": color,
                    "thickness": 0.35,
                },
                "borderwidth": 2,
                "bordercolor": "#777",
                "threshold": {
                    "line": {
                        "color": "white",
                        "width": 5,
                    },
                    "value": aqi,
                },
                "steps": [
                    {"range": [0, 50], "color": "#00E400"},
                    {"range": [50, 100], "color": "#FFFF00"},
                    {"range": [100, 150], "color": "#FF7E00"},
                    {"range": [150, 200], "color": "#FF0000"},
                    {"range": [200, 300], "color": "#8F3F97"},
                    {"range": [300, 500], "color": "#7E0023"},
                ],
            },
        )
    )

    return style_chart(fig)


# ==========================================================
# POLLUTANT CHART
# ==========================================================


def create_pollutant_chart(data: Dict[str, float]) -> go.Figure:
    """
    Create a horizontal bar chart for pollutants.
    """

    pollutants = {
        "PM2.5": data["pm2_5"],
        "PM10": data["pm10"],
        "NO₂": data["nitrogen_dioxide"],
        "SO₂": data["sulphur_dioxide"],
        "O₃": data["ozone"],
    }

    sorted_pollutants = sorted(
        pollutants.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    labels = [i[0] for i in sorted_pollutants]
    values = [i[1] for i in sorted_pollutants]

    colors = [
        "#EF553B",
        "#FECB52",
        "#19D3F3",
        "#AB63FA",
        "#00CC96",
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker=dict(
                color=colors[: len(values)],
                line=dict(color="white", width=1),
            ),
            text=[f"{v:.1f}" for v in values],
            textposition="outside",
            hovertemplate="%{y}: %{x} μg/m³<extra></extra>",
        )
    )

    fig.update_layout(
        title="🌫 Major Pollutants",
        xaxis_title="Concentration (μg/m³)",
        yaxis_title="",
        showlegend=False,
    )

    fig.update_xaxes(showgrid=True)

    fig.update_yaxes(showgrid=False)

    return style_chart(fig)


# ==========================================================
# HEALTH SCORE
# ==========================================================


def create_health_score(score: int) -> go.Figure:
    """
    Create a donut chart representing the health score.
    """

    fig = go.Figure(
        go.Pie(
            values=[score, 100 - score],
            labels=["Healthy Air", "Poor Air"],
            hole=0.72,
            textinfo="none",
            marker=dict(
                colors=[
                    "#00CC96",
                    "#2A2A2A",
                ]
            ),
        )
    )

    fig.update_layout(
        annotations=[
            dict(
                text=f"<b>{score}</b><br>Score",
                showarrow=False,
                font=dict(size=28),
            )
        ]
    )

    return style_chart(fig)


# ==========================================================
# PUBLIC EXPORTS
# ==========================================================

__all__ = [
    "create_gauge",
    "create_pollutant_chart",
    "create_health_score",
]