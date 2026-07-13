"""Local report generation for synthetic Human-AI learning experiments."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def write_learning_report(path: str | Path, summary: dict[str, Any], mode_summary: pd.DataFrame, fairness: pd.DataFrame) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Human-AI Personalized Learning Lab — Synthetic Report",
        "",
        "> **Synthetic-data warning:** all students, outcomes, groups, tasks, and feedback effects are fictional. This is not evidence about real learners or an educational product.",
        "",
        "## Run summary",
        "",
        f"- Seed: `{summary['seed']}`",
        f"- Synthetic students: `{summary['students']}`",
        f"- Sessions: `{summary['sessions']}`",
        f"- Audit valid: `{summary['audit_log']['valid']}`",
        f"- Max learning-gain gap: `{summary['fairness_gaps']['max_learning_gain_gap']:.3f}`",
        f"- Max over-reliance gap: `{summary['fairness_gaps']['max_over_reliance_gap']:.3f}`",
        "",
        "## Feedback-mode outcomes",
        "",
        "| Mode | Students | Mean gain | Final mastery | Trust | Dependence | Hint rate |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in mode_summary.itertuples(index=False):
        lines.append(f"| {row.feedback_mode} | {row.students} | {row.mean_learning_gain:.3f} | {row.mean_final_mastery:.3f} | {row.mean_trust:.3f} | {row.mean_dependence:.3f} | {row.mean_hint_rate:.3f} |")
    lines.extend(["", "## Fairness audit", "", "| Mode | Group | Students | Mean gain | Success rate | Over-reliance | Trust miscalibration |", "| --- | --- | ---: | ---: | ---: | ---: | ---: |"])
    for row in fairness.itertuples(index=False):
        lines.append(f"| {row.feedback_mode} | {row.group} | {row.students} | {row.mean_gain:.3f} | {row.success_rate:.3f} | {row.over_reliance_rate:.3f} | {row.trust_miscalibration:.3f} |")
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "The synthetic lab helps compare study designs and metrics. Real student studies require consent, ethics review, privacy controls, accessibility review, teacher oversight, and careful statistical analysis.",
    ])
    destination.write_text("\n".join(lines), encoding="utf-8")
