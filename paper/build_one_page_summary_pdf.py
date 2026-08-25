from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "one_page_research_summary.pdf"


def paragraph(text, style):
    return Paragraph(text, style)


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#1f2937"))
    canvas.setLineWidth(0.5)
    canvas.line(16 * mm, 288 * mm, 194 * mm, 288 * mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.drawRightString(
        194 * mm,
        11 * mm,
        "Application research summary - Working Paper Draft v0.2 - August 25, 2026",
    )
    canvas.restoreState()


def build_pdf():
    OUT.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#111827"),
        spaceAfter=4,
    )
    subtitle = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#374151"),
        spaceAfter=7,
    )
    heading = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=10,
        textColor=colors.HexColor("#111827"),
        spaceBefore=3,
        spaceAfter=2,
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=7.8,
        leading=9.4,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=3,
    )
    small = ParagraphStyle(
        "Small",
        parent=body,
        fontSize=7.2,
        leading=8.4,
        spaceAfter=2,
    )
    bullet = ParagraphStyle(
        "Bullet",
        parent=small,
        leftIndent=8,
        firstLineIndent=-5,
    )

    doc = BaseDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=13 * mm,
        bottomMargin=12 * mm,
        title="One-page research summary: mBERT vs MuRIL Hinglish harmful speech detection",
        author="Om Patnaik",
    )
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    doc.addPageTemplates([PageTemplate(id="OnePage", frames=[frame], onPage=on_page)])

    story = []
    story.append(paragraph("mBERT vs MuRIL for Hinglish / Hindi-English Harmful Speech Detection", title))
    story.append(paragraph("One-page research summary for review and project defense", subtitle))

    story.append(paragraph("Research Question", heading))
    story.append(
        paragraph(
            "Does Indian-language-specific pretraining in MuRIL improve hate/offensive speech detection for "
            "Hinglish and Hindi-English code-mixed text compared with general multilingual pretraining in mBERT? "
            "Current evidence says the answer is conditional: the better model changes with dataset situation.",
            body,
        )
    )

    story.append(paragraph("Datasets", heading))
    data = [
        ["Dataset", "Rows", "Positive label", "Situation"],
        ["Kaggle Hinglish Hate", "4,780", "hate", "controlled Hinglish subset from Kaggle"],
        ["CM Code-mixed", "3,900", "offensive", "Indian politics / Twitter/X, hate-adjacent"],
        ["THAR Religion", "11,549", "AntiReligion", "YouTube targeted religious hate"],
    ]
    table = Table(data, colWidths=[37 * mm, 17 * mm, 31 * mm, 81 * mm], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5e7eb")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 6.9),
                ("LEADING", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d1d5db")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    story.append(table)

    story.append(Spacer(1, 4))
    story.append(paragraph("Methods", heading))
    story.append(paragraph("- Models: mBERT and MuRIL fine-tuned as binary classifiers.", bullet))
    story.append(paragraph("- Matched setting: train and evaluate on the same dataset situation.", bullet))
    story.append(paragraph("- Robustness setting: evaluate trained checkpoints across other datasets and mixed-training conditions.", bullet))
    story.append(paragraph("- Primary metric: Macro F1; positive recall is tracked because false negatives are missed harmful examples.", bullet))

    story.append(paragraph("Main Matched Multi-Seed Result", heading))
    result_data = [
        ["Dataset", "Better model", "mBERT Macro F1", "MuRIL Macro F1", "Meaning"],
        ["Kaggle", "mBERT", "67.5 +/- 2.1", "58.1 +/- 5.7", "mBERT clear win; MuRIL misses more positives"],
        ["CM", "mBERT narrow", "77.7 +/- 1.9", "76.1 +/- 2.3", "both competitive; labels are offense-like"],
        ["THAR", "MuRIL", "74.7 +/- 0.1", "76.5 +/- 1.3", "MuRIL wins targeted religious hate"],
    ]
    result_table = Table(result_data, colWidths=[24 * mm, 29 * mm, 29 * mm, 29 * mm, 55 * mm], repeatRows=1)
    result_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 6.6),
                ("LEADING", (0, 0), (-1, -1), 7.8),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    story.append(result_table)

    story.append(Spacer(1, 4))
    story.append(paragraph("Current Interpretation", heading))
    story.append(
        paragraph(
            "The central evidence is that model ranking changes by dataset: mBERT wins Kaggle, mBERT narrowly wins CM, "
            "and MuRIL wins THAR. Cross-dataset robustness is weak, so hate, offensive, and AntiReligion labels must "
            "not be treated as interchangeable. The 79-row benchmark remains excluded from primary claims because its "
            "provenance is uncertain.",
            body,
        )
    )

    story.append(paragraph("Limitations", heading))
    story.append(paragraph("- Mixed-training and cross-dataset transformer results are mostly single-seed evidence.", bullet))
    story.append(paragraph("- Label definitions differ across datasets, which limits universal model-superiority claims.", bullet))
    story.append(paragraph("- Dataset licenses/citation details need final verification before public final release.", bullet))
    story.append(paragraph("- More manual error examples are needed to explain failure modes in the final draft.", bullet))

    story.append(paragraph("Feedback Requested", heading))
    story.append(
        paragraph(
            "Is the conditional claim clear enough? Are the dataset caveats acceptable? Which result should be prioritized "
            "for the next multi-seed run: mixed all-three training, Kaggle+THAR, CM+THAR, or cross-dataset transfer?",
            body,
        )
    )

    doc.build(story)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    build_pdf()
