from pathlib import Path

import pandas as pd
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output" / "pdf"
OUT_PATH = OUT_DIR / "hinglish_mbert_muril_research_paper_draft.pdf"


def pct(value):
    if pd.isna(value):
        return ""
    if abs(value) <= 1:
        value = value * 100
    return f"{value:.1f}%"


def clean_label(value):
    aliases = {
        "kaggle_hinglish_hate": "Kaggle Hinglish",
        "cm_splits_codemixed": "CM code-mixed",
        "thar_religion": "THAR religion",
        "existing_79_row_benchmark": "79-row probe",
    }
    return aliases.get(str(value), str(value).replace("_", " "))


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TitleCenter",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            alignment=TA_CENTER,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="AuthorCenter",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#333333"),
            spaceAfter=18,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=17,
            spaceBefore=14,
            spaceAfter=7,
            textColor=colors.HexColor("#111827"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="Subsection",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11.5,
            leading=14,
            spaceBefore=10,
            spaceAfter=5,
            textColor=colors.HexColor("#1f2937"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Small",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8.2,
            leading=10.5,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Caption",
            parent=styles["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#374151"),
            spaceBefore=3,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableCell",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=7.4,
            leading=9,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableHead",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=7.3,
            leading=8.8,
            alignment=TA_LEFT,
            textColor=colors.white,
        )
    )
    return styles


STYLES = make_styles()


def P(text, style="Body"):
    return Paragraph(text, STYLES[style])


def bullets(items):
    return ListFlowable(
        [ListItem(P(item, "Body"), leftIndent=12) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=16,
        bulletFontSize=5,
    )


def table_from_rows(headers, rows, widths=None):
    data = [[P(str(h), "TableHead") for h in headers]]
    data += [[P(str(cell), "TableCell") for cell in row] for row in rows]
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d1d5db")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f9fafb")]),
            ]
        )
    )
    return table


def add_figure(story, rel_path, caption, max_width=6.3 * inch, max_height=3.6 * inch):
    path = ROOT / rel_path
    if not path.exists():
        story.append(P(f"Missing figure: {rel_path}", "Small"))
        return
    with PILImage.open(path) as im:
        width_px, height_px = im.size
    scale = min(max_width / width_px, max_height / height_px)
    story.append(Spacer(1, 6))
    story.append(Image(str(path), width=width_px * scale, height=height_px * scale, hAlign="CENTER"))
    story.append(P(caption, "Caption"))


def matched_rows():
    df = pd.read_csv(ROOT / "results" / "result_analysis" / "primary_matched_transformer_results.csv")
    rows = []
    for _, r in df.iterrows():
        rows.append(
            [
                clean_label(r["test_dataset"]),
                str(r["model"]).upper() if r["model"] == "muril" else "mBERT",
                pct(r["accuracy"]),
                pct(r["recall_positive"]),
                pct(r["f1_positive"]),
                pct(r["f1_macro"]),
                f'{int(r["tn"])}/{int(r["fp"])}/{int(r["fn"])}/{int(r["tp"])}',
            ]
        )
    return rows


def pairwise_rows():
    df = pd.read_csv(ROOT / "results" / "result_analysis" / "mbert_vs_muril_pairwise_gaps.csv")
    selected = [
        ("kaggle_hinglish_hate", "kaggle_hinglish_hate"),
        ("cm_splits_codemixed", "cm_splits_codemixed"),
        ("thar_religion", "thar_religion"),
        ("cm_splits_codemixed", "thar_religion"),
        ("thar_religion", "cm_splits_codemixed"),
        ("kaggle_hinglish_hate", "thar_religion"),
        ("thar_religion", "kaggle_hinglish_hate"),
    ]
    rows = []
    for train, test in selected:
        r = df[(df["train_dataset"] == train) & (df["test_dataset"] == test)].iloc[0]
        rows.append(
            [
                clean_label(train),
                clean_label(test),
                str(r["winner_by_macro_f1"]).upper() if r["winner_by_macro_f1"] == "muril" else "mBERT",
                pct(r["macro_f1_gap"]),
                str(r["winner_by_positive_recall"]).upper() if r["winner_by_positive_recall"] == "muril" else "mBERT",
                pct(r["positive_recall_gap"]),
            ]
        )
    return rows


def baseline_rows():
    df = pd.read_csv(ROOT / "results" / "result_analysis" / "best_transformer_vs_best_tfidf.csv")
    selected = [
        ("cm_splits_codemixed", "cm_splits_codemixed"),
        ("kaggle_hinglish_hate", "kaggle_hinglish_hate"),
        ("thar_religion", "thar_religion"),
        ("kaggle_hinglish_hate", "thar_religion"),
        ("thar_religion", "kaggle_hinglish_hate"),
        ("cm_splits_codemixed", "thar_religion"),
        ("thar_religion", "cm_splits_codemixed"),
    ]
    rows = []
    for train, test in selected:
        r = df[(df["train_dataset"] == train) & (df["test_dataset"] == test)].iloc[0]
        rows.append(
            [
                clean_label(train),
                clean_label(test),
                str(r["best_transformer"]).upper() if r["best_transformer"] == "muril" else "mBERT",
                pct(r["transformer_f1_macro"]),
                str(r["best_baseline"]).replace("tfidf_", "").replace("_", " ").title(),
                pct(r["baseline_f1_macro"]),
                pct(r["transformer_minus_baseline"]),
            ]
        )
    return rows


def error_rows():
    df = pd.read_csv(ROOT / "results" / "error_analysis" / "error_rate_summary.csv")
    selected = [
        ("kaggle_hinglish_hate", "kaggle_hinglish_hate"),
        ("cm_splits_codemixed", "cm_splits_codemixed"),
        ("thar_religion", "thar_religion"),
        ("kaggle_hinglish_hate", "thar_religion"),
        ("thar_religion", "kaggle_hinglish_hate"),
        ("thar_religion", "cm_splits_codemixed"),
    ]
    rows = []
    for train, test in selected:
        r = df[(df["train_dataset"] == train) & (df["test_dataset"] == test)].iloc[0]
        rows.append(
            [
                clean_label(train),
                clean_label(test),
                int(r["rows"]),
                int(r["positive_rows"]),
                pct(r["mbert_false_negative_rate"]),
                pct(r["muril_false_negative_rate"]),
                pct(r["mbert_false_positive_rate"]),
                pct(r["muril_false_positive_rate"]),
            ]
        )
    return rows


def manual_reason_rows():
    df = pd.read_csv(ROOT / "results" / "error_analysis" / "manual_error_annotation_summary.csv")
    rows = []
    for _, r in df.head(9).iterrows():
        rows.append([str(r["manual_reason"]).replace("_", " "), int(r["rows"]), pct(r["share"])])
    return rows


def build_story():
    story = []
    story.append(P("Cross-Dataset Evaluation of mBERT and MuRIL for Hinglish Hate and Offensive Speech Detection", "TitleCenter"))
    story.append(P("Om Patnaik | Working Draft v0.1 - July 1, 2026", "AuthorCenter"))

    story.append(P("Abstract", "Section"))
    story.append(
        P(
            "Hinglish hate speech detection is difficult because online text often mixes Hindi and English, "
            "uses inconsistent Romanization, moves between Latin and Devanagari scripts, and changes sharply "
            "across platform, topic, and annotation policy. This project compares mBERT, a general multilingual "
            "BERT model, with MuRIL, an Indian-language-focused model, for binary hate/offensive speech detection "
            "across multiple Hindi-English code-mixed dataset situations. Current experiments show that neither "
            "model is universally superior. mBERT performs better on matched Latin-script Hinglish and code-mixed "
            "offensive datasets, while MuRIL performs better on targeted religious hate and several THAR-related "
            "transfer settings. Cross-dataset evaluation reveals substantial generalization gaps and shows that "
            "TF-IDF baselines remain competitive in some transfer conditions.",
        )
    )

    story.append(P("1. Research Motivation and Claim", "Section"))
    story.append(
        P(
            "The original research question asked whether MuRIL, because it was designed for Indian languages, "
            "would outperform mBERT for Hinglish hate speech detection. The experiments so far show that the "
            "answer cannot be reduced to one universal winner. The stronger research claim is conditional: "
            "model ranking changes with dataset content, platform, script composition, and positive-label definition."
        )
    )
    story.append(
        bullets(
            [
                "mBERT is stronger on matched Kaggle Hinglish hate and CM code-mixed offensive evaluation.",
                "MuRIL is stronger on matched THAR targeted religious hate and on several THAR-related transfer settings.",
                "Every primary test dataset is best served by an in-domain model, showing that cross-dataset robustness is limited.",
                "TF-IDF baselines are competitive in several settings, so transformer performance must be interpreted against lexical baselines.",
            ]
        )
    )

    story.append(P("2. Related Work", "Section"))
    story.append(
        P(
            "This project sits at the intersection of multilingual language models, Indian-language representation learning, "
            "and code-mixed harmful speech detection. mBERT is a general multilingual BERT model, while MuRIL was introduced "
            "to improve representation learning for Indian languages, including translated and transliterated signals. This "
            "makes MuRIL a natural candidate for Hinglish and Hindi-English code-mixed social media text."
        )
    )
    story.append(
        P(
            "Prior Hindi-English code-mixed hate speech work, including the Bohra et al. dataset, shows that this task cannot "
            "be treated as ordinary English hate speech detection. Code-mixed text contains unstable spelling, transliteration, "
            "language switching, and local social context. THAR adds another important angle by focusing specifically on targeted "
            "religious hate in Hindi-English code-mixed comments. The current project builds on these ideas but places emphasis "
            "on cross-dataset robustness: whether a model trained on one dataset situation still works when the platform, target, "
            "script mix, or positive-label definition changes."
        )
    )

    story.append(P("3. Datasets and Dataset Situations", "Section"))
    story.append(
        P(
            "The project uses three primary source-backed datasets. The 79-row benchmark is excluded from primary "
            "claims because its provenance is uncertain and it may be manually written or AI-generated."
        )
    )
    story.append(
        table_from_rows(
            ["Dataset", "Source/domain", "Rows", "Label 0", "Label 1", "Positive meaning"],
            [
                ["Kaggle Hinglish", "Kaggle Hinglish subset", "4,780", "2,914", "1,866", "Hate"],
                ["CM code-mixed", "Indian politics Twitter/X", "3,900", "2,455", "1,445", "Offensive"],
                ["THAR religion", "YouTube religion comments", "11,549", "6,095", "5,454", "AntiReligion"],
            ],
            widths=[1.35 * inch, 1.45 * inch, 0.55 * inch, 0.55 * inch, 0.55 * inch, 1.25 * inch],
        )
    )
    story.append(Spacer(1, 8))
    story.append(
        P(
            "Kaggle Hinglish is fully Latin-script in the processed subset and is useful for Romanized Hinglish behavior. "
            "CM is mostly Latin-script but contains Indian political content, many mentions, hashtags, and an offensive "
            "rather than strict hate label. THAR is narrower but highly relevant: it focuses on targeted religious hate "
            "in Hindi-English code-mixed YouTube comments and contains more Devanagari and mixed-script text."
        )
    )
    add_figure(story, "results/figures/dataset_size_label_balance.png", "Figure 1. Dataset size and label balance.")
    add_figure(story, "results/data_analysis/script_composition.png", "Figure 2. Script composition by dataset.")
    add_figure(story, "results/data_analysis/word_count_by_label.png", "Figure 3. Text length by label.")

    story.append(P("4. Models and Experimental Setup", "Section"))
    story.append(
        P(
            "The transformer experiments compare bert-base-multilingual-cased for mBERT and google/muril-base-cased "
            "for MuRIL. Each model is fine-tuned as a binary sequence classifier. The controlled checkpoints use seed "
            "42, two training epochs, maximum sequence length 128, learning rate 2e-5, and minimal URL/user normalization. "
            "For datasets without an official split, a stratified 80/20 split is used. For CM, source-provided splits are used."
        )
    )
    story.append(
        P(
            "The project also evaluates TF-IDF with logistic regression and TF-IDF with linear SVM. These baselines are "
            "important because hate and offensive datasets can contain strong repeated lexical cues. A transformer claim "
            "is only meaningful if it is read alongside these simpler models."
        )
    )
    story.append(P("Reproducibility Box", "Subsection"))
    story.append(
        table_from_rows(
            ["Item", "Current setting"],
            [
                ["Models", "bert-base-multilingual-cased; google/muril-base-cased"],
                ["Primary datasets", "Kaggle Hinglish; CM code-mixed; THAR religion"],
                ["Split policy", "Stratified 80/20 where needed; CM source split used"],
                ["Seed", "42 for current controlled transformer runs"],
                ["Epochs", "2"],
                ["Max sequence length", "128"],
                ["Learning rate", "2e-5"],
                ["Baselines", "TF-IDF + logistic regression; TF-IDF + linear SVM"],
                ["Hardware/scripts", "Device-specific wrappers for Mac MPS, CPU/debug, and CUDA/Colab"],
                ["Known rigor gap", "Multi-seed runs and confidence intervals are still pending"],
            ],
            widths=[1.8 * inch, 4.6 * inch],
        )
    )
    story.append(
        P(
            "Two epochs were chosen as a controlled first-pass setting so every model/dataset condition could be compared under "
            "the same budget. This is not a claim that two epochs are optimal. Future versions should use multi-seed runs, validation "
            "curves, and possibly early stopping."
        )
    )

    story.append(P("5. Primary Matched Results", "Section"))
    story.append(
        P(
            "Matched evaluation means that a model is trained and tested within the same dataset situation. This is the "
            "cleanest setting for measuring how well each pretrained model adapts to a specific dataset."
        )
    )
    story.append(
        table_from_rows(
            ["Test dataset", "Model", "Acc.", "Pos. recall", "Pos. F1", "Macro F1", "TN/FP/FN/TP"],
            matched_rows(),
            widths=[1.35 * inch, 0.5 * inch, 0.5 * inch, 0.65 * inch, 0.55 * inch, 0.6 * inch, 1.0 * inch],
        )
    )
    story.append(
        P(
            "Interpretation: mBERT wins the matched Kaggle and CM conditions, while MuRIL wins the matched THAR condition. "
            "This is the first major reason the paper should avoid claiming a universal winner."
        )
    )
    add_figure(story, "results/result_analysis/transformer_primary_macro_f1_matrix.png", "Figure 4. Primary transformer macro F1 matrix.")

    story.append(P("6. Cross-Dataset Transfer", "Section"))
    story.append(
        P(
            "Cross-dataset evaluation asks whether a model trained on one dataset can generalize to another. This is the "
            "main research contribution because it exposes whether a model has learned broadly useful hate/offense signals "
            "or only the local annotation and lexical patterns of one dataset."
        )
    )
    story.append(
        table_from_rows(
            ["Train", "Test", "Macro winner", "Macro gap", "Recall winner", "Recall gap"],
            pairwise_rows(),
            widths=[1.25 * inch, 1.25 * inch, 0.75 * inch, 0.65 * inch, 0.85 * inch, 0.65 * inch],
        )
    )
    story.append(
        P(
            "MuRIL becomes stronger in THAR-related transfer, especially CM-to-THAR and THAR-to-CM. However, both models "
            "transfer poorly between broad Hinglish hate and targeted religious hate. Kaggle-trained models are very "
            "conservative on THAR, while THAR-trained models do not become general Hinglish hate detectors."
        )
    )
    add_figure(story, "results/figures/transformer_cross_dataset_macro_f1.png", "Figure 5. Transformer cross-dataset macro F1.")
    add_figure(story, "results/figures/transformer_cross_dataset_positive_recall.png", "Figure 6. Transformer cross-dataset positive recall.")
    add_figure(story, "results/result_analysis/transformer_generalization_gaps.png", "Figure 7. Generalization gaps from matched to transfer evaluation.")

    story.append(P("7. Baselines and Lexical Effects", "Section"))
    story.append(
        P(
            "TF-IDF baselines are not the focus of the project, but they are essential controls. If TF-IDF performs well, "
            "that suggests strong lexical regularities in the dataset. In several transfer settings, TF-IDF beats the best "
            "transformer, especially Kaggle-to-THAR and THAR-to-Kaggle."
        )
    )
    story.append(
        table_from_rows(
            ["Train", "Test", "Best transformer", "Trans. macro", "Best TF-IDF", "TF-IDF macro", "Delta"],
            baseline_rows(),
            widths=[1.08 * inch, 1.08 * inch, 0.7 * inch, 0.62 * inch, 0.9 * inch, 0.65 * inch, 0.5 * inch],
        )
    )
    add_figure(story, "results/result_analysis/transformer_vs_tfidf_delta.png", "Figure 8. Transformer macro F1 minus best TF-IDF macro F1.")
    add_figure(story, "results/figures/baseline_cross_dataset_macro_f1.png", "Figure 9. Baseline cross-dataset macro F1.")

    story.append(PageBreak())
    story.append(P("8. Error Analysis", "Section"))
    story.append(
        P(
            "False negatives are especially important in this task because they are harmful examples predicted as non-harmful. "
            "The false-negative pattern matches the larger story: mBERT misses fewer positives in matched Kaggle and CM, while "
            "MuRIL misses fewer positives in matched THAR and THAR-to-CM transfer."
        )
    )
    story.append(
        table_from_rows(
            ["Train", "Test", "Rows", "Pos.", "mBERT FN", "MuRIL FN", "mBERT FP", "MuRIL FP"],
            error_rows(),
            widths=[1.0 * inch, 1.0 * inch, 0.45 * inch, 0.45 * inch, 0.62 * inch, 0.62 * inch, 0.62 * inch, 0.62 * inch],
        )
    )
    add_figure(story, "results/error_analysis/false_negative_rates.png", "Figure 10. False-negative rates by train/test condition.")
    add_figure(story, "results/error_analysis/model_disagreement_advantage.png", "Figure 11. Model disagreement advantage analysis.")
    story.append(P("Manual Error Coding", "Subsection"))
    story.append(
        P(
            "A first-pass manual coding of sampled errors was created as a structured reading aid, not final human-ground-truth annotation. "
            "The dominant theme is cross-dataset label mismatch: many errors occur because one dataset's positive class is not the same "
            "as another dataset's positive class."
        )
    )
    story.append(
        table_from_rows(
            ["Manual reason", "Rows", "Share"],
            manual_reason_rows(),
            widths=[3.2 * inch, 0.55 * inch, 0.65 * inch],
        )
    )

    story.append(P("9. Main Inferences", "Section"))
    story.append(
        bullets(
            [
                "The project should claim conditional model behavior, not absolute model superiority.",
                "mBERT's strengths appear in mostly Latin-script Hinglish and offensive/code-mixed settings.",
                "MuRIL's strengths appear in targeted religious hate and some Indian-context transfer settings.",
                "Dataset label meaning is a major confound: hate, offense, and AntiReligion are related but not interchangeable.",
                "Cross-dataset failure is not noise; it is a core research result showing weak robustness across dataset situations.",
                "TF-IDF competitiveness implies that lexical shortcuts and dataset-specific words are part of the story.",
            ]
        )
    )

    story.append(P("10. Limitations", "Section"))
    story.append(
        bullets(
            [
                "The three primary datasets differ in platform, label policy, target domain, and script mix.",
                "CM should be described as offensive/hate-adjacent unless its label definition is verified further.",
                "The 79-row benchmark is excluded from primary conclusions because its provenance is uncertain.",
                "The THAR citation and CM licensing/citation details need final verification before formal submission.",
                "Indo-HateSpeech was reviewed but not added to primary experiments because of short texts, duplicates, source concentration, and label ambiguity.",
                "Mixed-dataset training has not yet been completed in this draft.",
            ]
        )
    )

    story.append(P("11. Next Experimental Step", "Section"))
    story.append(
        P(
            "The next stage is mixed-dataset training. The project should train mBERT and MuRIL on Kaggle+CM, Kaggle+THAR, "
            "CM+THAR, and Kaggle+CM+THAR, then evaluate each checkpoint separately on every primary dataset. This will show "
            "whether broader training improves robustness or simply mixes incompatible label definitions."
        )
    )
    story.append(P("AI-Use Statement", "Section"))
    story.append(
        P(
            "AI tools were used for coding assistance, environment debugging, documentation organization, and draft generation. "
            "The research direction, dataset selection decisions, experiment interpretation, and manual error-analysis decisions "
            "were reviewed and directed by the student."
        )
    )

    story.append(PageBreak())
    story.append(P("References", "Section"))
    references = [
        "Devlin, J., Chang, M.-W., Lee, K., and Toutanova, K. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. NAACL-HLT.",
        "Khanuja, S. et al. (2021). MuRIL: Multilingual Representations for Indian Languages. arXiv:2103.10730.",
        "Bohra, A., Vijay, D., Singh, V., Akhtar, S. S., and Shrivastava, M. (2018). A Dataset of Hindi-English Code-Mixed Social Media Text for Hate Speech Detection. PEOPLES.",
        "Dhekane, S. Code-Mixed Hinglish Hate Speech Detection Dataset. Kaggle. Accessed 2026-07-01.",
        "cm-hate-speech-detection contributors. GitHub repository: https://github.com/shikharras/cm-hate-speech-detection. Accessed 2026-07-01.",
        "Sharma, D. et al. (2024). THAR: Targeted Hate Speech Against Religion. DOI: 10.1145/3653017.",
    ]
    story.append(bullets(references))
    return story


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.drawRightString(A4[0] - 0.65 * inch, 0.42 * inch, f"Page {doc.page}")
    canvas.drawString(0.65 * inch, 0.42 * inch, "mBERT vs MuRIL cross-dataset Hinglish hate/offensive speech draft")
    canvas.restoreState()


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT_PATH),
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
    )
    story = build_story()
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(OUT_PATH)


if __name__ == "__main__":
    main()
