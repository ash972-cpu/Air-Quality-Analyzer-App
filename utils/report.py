"""
report.py

Professional PDF Report Generator
for the Air Quality Intelligence Dashboard.

Author: Ashish Kumar Mishra
"""

from io import BytesIO
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    SimpleDocTemplate,
)

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# ==========================================================
# FONT
# ==========================================================

try:
    pdfmetrics.registerFont(
        TTFont(
            "DejaVu",
            "DejaVuSans.ttf"
        )
    )
    FONT = "DejaVu"

except Exception:
    FONT = "Helvetica"


# ==========================================================
# STYLES
# ==========================================================

styles = getSampleStyleSheet()

title_style = styles["Title"]
title_style.fontName = FONT
title_style.fontSize = 24
title_style.alignment = TA_CENTER
title_style.textColor = colors.HexColor("#00897B")

heading_style = styles["Heading2"]
heading_style.fontName = FONT
heading_style.textColor = colors.HexColor("#1565C0")

normal_style = styles["BodyText"]
normal_style.fontName = FONT
normal_style.fontSize = 11
normal_style.leading = 18

small_style = styles["BodyText"]
small_style.fontName = FONT
small_style.fontSize = 9
small_style.leading = 12


# ==========================================================
# TABLE STYLE
# ==========================================================

TABLE_STYLE = TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1565C0")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, -1), FONT),
    ("FONTSIZE", (0, 0), (-1, -1), 10),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
])


# ==========================================================
# FORMAT AI TEXT
# ==========================================================

def format_ai_text(text: str) -> list[str]:
    """
    Converts Groq Markdown into clean printable lines.
    """

    lines = []

    for raw in text.splitlines():

        line = raw.strip()

        if not line:
            continue

        if line.startswith("##"):
            line = line.replace("##", "").strip()
            lines.append(f"HEADING::{line}")
            continue

        if line.startswith("- "):
            line = "• " + line[2:]

        line = line.replace("*", "")

        lines.append(line)

    return lines


# ==========================================================
# PDF REPORT
# ==========================================================

def generate_pdf_report(
    city,
    location,
    weather,
    air_quality,
    status,
    health_score,
    ai_advice,
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.6 * inch,
        leftMargin=0.6 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
    )

    story = []

    # ======================================================
    # TITLE
    # ======================================================

    story.append(
        Paragraph(
            "🌍 Air Quality Intelligence Report",
            title_style,
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            f"Generated on {datetime.now().strftime('%d %B %Y %I:%M %p')}",
            small_style,
        )
    )

    story.append(Spacer(1, 0.3 * inch))

    # ======================================================
    # LOCATION
    # ======================================================

    story.append(
        Paragraph(
            "Location Information",
            heading_style,
        )
    )

    location_table = [
        ["Field", "Value"],
        ["City", location["city"]],
        ["State", location["state"] or "-"],
        ["Country", location["country"]],
        [
            "Coordinates",
            f"{location['latitude']:.4f}, {location['longitude']:.4f}",
        ],
    ]

    table = Table(
        location_table,
        colWidths=[2.3 * inch, 3.7 * inch],
    )

    table.setStyle(TABLE_STYLE)

    story.append(table)

    story.append(Spacer(1, 0.30 * inch))

        # ====================================================
    # AQI SUMMARY
    # ====================================================

    story.append(
        Paragraph(
            "Air Quality Summary",
            heading_style,
        )
    )

    aqi_table = [

        ["Metric", "Value"],

        ["European AQI", str(air_quality["european_aqi"])],

        ["Status", status],

        ["Health Score", f"{health_score}/100"],

    ]

    table = Table(
        aqi_table,
        colWidths=[3 * inch, 3 * inch],
    )

    table.setStyle(TABLE_STYLE)

    story.append(table)

    story.append(Spacer(1, 0.30 * inch))

    # ====================================================
    # WEATHER
    # ====================================================

    story.append(
        Paragraph(
            "Current Weather",
            heading_style,
        )
    )

    weather_table = [

        ["Parameter", "Value"],

        [
            "Temperature",
            f"{weather['temperature_2m']} °C",
        ],

        [
            "Humidity",
            f"{weather['relative_humidity_2m']} %",
        ],

        [
            "Wind Speed",
            f"{weather['wind_speed_10m']} km/h",
        ],

    ]

    table = Table(
        weather_table,
        colWidths=[3 * inch, 3 * inch],
    )

    table.setStyle(TABLE_STYLE)

    story.append(table)

    story.append(Spacer(1, 0.30 * inch))

    # ====================================================
    # POLLUTANTS
    # ====================================================

    story.append(
        Paragraph(
            "Major Pollutants",
            heading_style,
        )
    )

    pollutant_table = [

        ["Pollutant", "Value"],

        [
            "PM2.5",
            f"{air_quality['pm2_5']} μg/m³",
        ],

        [
            "PM10",
            f"{air_quality['pm10']} μg/m³",
        ],

        [
            "Nitrogen Dioxide (NO₂)",
            f"{air_quality['nitrogen_dioxide']} μg/m³",
        ],

        [
            "Sulphur Dioxide (SO₂)",
            f"{air_quality['sulphur_dioxide']} μg/m³",
        ],

        [
            "Ozone (O₃)",
            f"{air_quality['ozone']} μg/m³",
        ],

        [
            "Carbon Monoxide (CO)",
            f"{air_quality['carbon_monoxide']} μg/m³",
        ],

    ]

    table = Table(
        pollutant_table,
        colWidths=[3 * inch, 3 * inch],
    )

    table.setStyle(TABLE_STYLE)

    story.append(table)

    story.append(Spacer(1, 0.30 * inch))

    # ====================================================
    # AI HEALTH ADVISOR
    # ====================================================

    story.append(
        Paragraph(
            "AI Health Advisor",
            heading_style,
        )
    )

    ai_lines = format_ai_text(ai_advice)

    for line in ai_lines:

        if line.startswith("\n"):

            heading = line.strip().upper()

            story.append(
                Spacer(1, 0.10 * inch)
            )

            story.append(
                Paragraph(
                    f"<b>{escape(heading)}</b>",
                    normal_style,
                )
            )

            continue

        safe_line = escape(line)

        story.append(
            Paragraph(
                safe_line,
                normal_style,
            )
        )

    story.append(
        Spacer(1, 0.30 * inch)
    )

        # ====================================================
    # FOOTER
    # ====================================================

    story.append(Spacer(1, 0.40 * inch))

    footer_table = Table(
        [[
            "Generated using Streamlit • Groq AI • Open-Meteo API\n"
            f"Report generated on {datetime.now().strftime('%d %B %Y %I:%M %p')}\n\n"
            "© Ashish Kumar Mishra"
        ]],
        colWidths=[6.2 * inch],
    )

    footer_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F3F4F6")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.grey),
                ("FONTNAME", (0, 0), (-1, -1), FONT),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    story.append(footer_table)

    # ====================================================
    # BUILD PDF
    # ====================================================

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf