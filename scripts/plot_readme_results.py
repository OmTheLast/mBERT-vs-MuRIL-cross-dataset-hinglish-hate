"""Plot committed matched-run means and sample standard deviations without checkpoints."""
import csv
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    path = ROOT / "results/multiseed/matched_multiseed_summary.csv"
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    order = ["kaggle_hinglish_hate", "cm_splits_codemixed", "thar_religion"]
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="940" height="420" viewBox="0 0 940 420" role="img" aria-labelledby="title desc">',
           '<title id="title">mBERT and MuRIL matched Macro F1 across three datasets</title>',
           '<desc id="desc">Points are three-seed means; ranges are mean plus or minus one sample standard deviation, not confidence intervals.</desc>',
           '<rect width="940" height="420" fill="#fafaf8"/>',
           '<g font-family="Arial, sans-serif" fill="#20252b">',
           '<text x="28" y="35" font-size="23">The model ranking changes with the dataset</text>',
           '<text x="28" y="63" font-size="14">Macro F1 (%) • mean ± sample SD • seeds 7, 13, 42 • evaluation reused for selection</text>']
    for tick in range(0, 101, 20):
        x = 260 + tick * 5.6
        svg += [f'<line x1="{x}" y1="85" x2="{x}" y2="335" stroke="#d9dde0"/>',
                f'<text x="{x}" y="361" text-anchor="middle" font-size="13">{tick}</text>']
    for i, dataset in enumerate(order):
        subset = [r for r in rows if r["train_dataset"] == dataset]
        assert len(subset) == 2
        label = escape(subset[0]["train_dataset_label"])
        y = 115 + i * 83
        svg.append(f'<text x="28" y="{y+14}" font-size="17">{label}</text>')
        for j, model in enumerate(["mbert", "muril"]):
            row = next(r for r in subset if r["model"] == model)
            assert int(row["n_seeds"]) == 3
            mean, std = float(row["f1_macro_mean"]) * 100, float(row["f1_macro_std"]) * 100
            x, lo, hi = 260 + mean*5.6, 260 + (mean-std)*5.6, 260 + (mean+std)*5.6
            yy = y + j * 26
            color = "#176b75" if model == "mbert" else "#9a572e"
            svg += [f'<line x1="{lo:.2f}" y1="{yy}" x2="{hi:.2f}" y2="{yy}" stroke="{color}" stroke-width="3"/>',
                    f'<circle cx="{x:.2f}" cy="{yy}" r="6" fill="{color}"/>',
                    f'<text x="{hi+12:.2f}" y="{yy+5}" font-size="14">{mean:.1f} ± {std:.1f}</text>']
    svg += ['<text x="28" y="394" font-size="14">Teal: mBERT   Brown: MuRIL   |   Ranges are sample spread, not confidence intervals.</text>', '</g></svg>']
    output = ROOT / "results/result_analysis/readme-matched-results.svg"
    output.write_text("\n".join(svg) + "\n")
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
