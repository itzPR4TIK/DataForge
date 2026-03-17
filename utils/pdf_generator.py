import io
from datetime import datetime

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
)
DARK_BLUE  = colors.HexColor("#1E3A5F")
MID_BLUE   = colors.HexColor("#2563EB")
LIGHT_BLUE = colors.HexColor("#DBEAFE")
GREY_BG    = colors.HexColor("#F8F9FA")
WHITE      = colors.white
DARK_TEXT  = colors.HexColor("#1F2937")
def _build_styles():
    base = getSampleStyleSheet()
    
    styles = {
        "title": ParagraphStyle(
            "ReportTitle",
            parent=base["Title"],
            fontSize=26,
            textColor=DARK_BLUE,
            spaceAfter=4,
            alignment=1,
            fontName="Helvetica-Bold",
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["Normal"],
            fontSize=11,
            textColor=colors.grey,
            spaceAfter=20,
            alignment=1,
        ),
        "section_heading": ParagraphStyle(
            "SectionHeading",
            parent=base["Heading2"],
            fontSize=14,
            textColor=DARK_BLUE,
            spaceBefore=16,
            spaceAfter=8,
            fontName="Helvetica-Bold",
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontSize=10,
            textColor=DARK_TEXT,
            spaceAfter=6,
        ),
    }
    return styles
def _image_from_bytes(img_bytes, width_cm=15):
    buf = io.BytesIO(img_bytes)
    img = Image(buf)
    aspect = img.imageHeight / img.imageWidth
    img.drawWidth = width_cm * cm
    img.drawHeight = img.drawWidth * aspect
    return img

def _df_to_table(df):
    header = [str(col) for col in df.columns]
    data = [header] + [
        [str(round(v, 2)) if isinstance(v, float) else str(v) for v in row]
        for row in df.values
    ]
    col_width = 15 * cm / len(df.columns)
    table = Table(data, colWidths=[col_width] * len(df.columns), repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  DARK_BLUE),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, GREY_BG]),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 1), (-1, -1), 9),
        ("GRID",          (0, 0), (-1, -1), 0.3, colors.HexColor("#D1D5DB")),
        ("BOX",           (0, 0), (-1, -1), 0.8, DARK_BLUE),
    ]))
    return table
def generate_pdf(df, stats_df, chart_bytes_list, report_title="Data Report"):
    buf = io.BytesIO()
    styles = _build_styles()

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title=report_title,
    )

    story = []
    # Title
    story.append(Paragraph(report_title, styles["title"]))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}",
        styles["subtitle"]
    ))
    story.append(Spacer(1, 0.4*cm))

    # Data preview
    story.append(Paragraph("Data Preview (first 10 rows)", styles["section_heading"]))
    story.append(_df_to_table(df.head(10)))
    story.append(Spacer(1, 0.5*cm))

    # Statistics
    if not stats_df.empty:
        story.append(Paragraph("Descriptive Statistics", styles["section_heading"]))
        stats_display = stats_df.reset_index()
        stats_display.columns = ["Column"] + list(stats_display.columns[1:])
        story.append(_df_to_table(stats_display))
        story.append(Spacer(1, 0.5*cm))

    # Charts
    if chart_bytes_list:
        story.append(Paragraph("Charts", styles["section_heading"]))
        for chart_title, chart_bytes in chart_bytes_list:
            story.append(Paragraph(chart_title, styles["body"]))
            story.append(_image_from_bytes(chart_bytes))
            story.append(Spacer(1, 0.4*cm))

    doc.build(story)
    buf.seek(0)
    return buf.getvalue()