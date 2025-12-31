from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


METRIC_ORDER = ["recall_1", "prec_1", "f1_1", "bal_acc", "acc", "ap", "roc_auc"]


def parse_report(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")

    # run name = 파일명
    run = path.stem

    # thr 추출
    thr = None
    m_thr = re.search(r"### Final Model.*?\n- thr:\s*([0-9.]+)", text, flags=re.S)
    if m_thr:
        thr = float(m_thr.group(1))

    # Final test metrics 블록에서 metric:value 추출
    metrics = {}
    # 예) "  - recall_1: 1.0000"
    for m in re.finditer(r"^\s*-\s*([a-zA-Z0-9_]+)\s*:\s*([0-9.]+)\s*$", text, flags=re.M):
        k = m.group(1).strip()
        v = float(m.group(2))
        # "test metrics:" 이후 블록만 잡고 싶지만, report 구조상 안전하게 아래 키들만 반영
        if k in set(METRIC_ORDER) or k == "thr":
            metrics[k] = v

    # 위 정규식은 "- thr:"도 잡아버릴 수 있어 thr은 별도 우선
    if thr is not None:
        metrics["thr"] = thr

    # Final test metrics는 "test metrics:" 아래에 있으니, 그 블록만 더 정확히 파싱
    m_block = re.search(r"- test metrics:\n(?P<blk>(?:\s*-\s*[a-zA-Z0-9_]+\s*:\s*[0-9.]+\s*\n)+)", text)
    if m_block:
        blk = m_block.group("blk")
        for m in re.finditer(r"^\s*-\s*([a-zA-Z0-9_]+)\s*:\s*([0-9.]+)\s*$", blk, flags=re.M):
            metrics[m.group(1)] = float(m.group(2))

    return {"run": run, **metrics}


def grouped_bar(df: pd.DataFrame, metric_keys: list[str], out_png: Path, title: str):
    runs = df["run"].tolist()
    n_runs = len(runs)
    x = np.arange(len(metric_keys))
    width = 0.8 / max(1, n_runs)

    plt.figure()
    for i, run in enumerate(runs):
        vals = [df.loc[df["run"] == run, k].iloc[0] if k in df.columns else np.nan for k in metric_keys]
        plt.bar(x + (i - (n_runs - 1) / 2) * width, vals, width, label=run)

    plt.xticks(x, metric_keys, rotation=25, ha="right")
    plt.ylim(0.0, 1.05)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=160)
    plt.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reports", nargs="+", required=True, help="report md paths")
    ap.add_argument("--outdir", default="reports/viz_20251231")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    rows = []
    for rp in args.reports:
        rows.append(parse_report(Path(rp)))

    df = pd.DataFrame(rows)
    df.to_csv(outdir / "final_metrics.csv", index=False, encoding="utf-8-sig")
    print("[OK] saved:", outdir / "final_metrics.csv")
    print(df)

    # 핵심 비교 1장
    core = ["recall_1", "prec_1", "f1_1", "bal_acc"]
    grouped_bar(df, core, outdir / "compare_core_metrics.png", "Final Test Metrics (core)")

    # 전체 비교 1장
    grouped_bar(df, METRIC_ORDER, outdir / "compare_all_metrics.png", "Final Test Metrics (all)")

    # threshold 비교
    if "thr" in df.columns:
        plt.figure()
        plt.bar(df["run"].tolist(), df["thr"].tolist())
        plt.xticks(rotation=25, ha="right")
        plt.title("Threshold (final)")
        plt.tight_layout()
        plt.savefig(outdir / "compare_threshold.png", dpi=160)
        plt.close()

    print("[OK] png saved to:", outdir)


if __name__ == "__main__":
    main()
