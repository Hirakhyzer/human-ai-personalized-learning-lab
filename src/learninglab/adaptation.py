"""Adaptation quality and recommendation analysis."""

from __future__ import annotations

import numpy as np
import pandas as pd


def evaluate_adaptation_quality(activity: pd.DataFrame) -> pd.DataFrame:
    """Score whether task difficulty and feedback mode fit the learner state."""
    output = activity.copy()
    output["optimal_difficulty"] = (output["mastery_estimate"].shift(1).fillna(output["mastery_estimate"]) + 0.10).clip(0, 1)
    output["difficulty_gap"] = (output["task_difficulty"] - output["optimal_difficulty"]).abs()
    output["adaptation_quality_score"] = (100 * (0.45 * output["challenge_fit"] + 0.35 * output["feedback_quality"] + 0.20 * (1 - output["difficulty_gap"].clip(0, 1)))).round(2)
    return output


def next_activity_recommendations(activity: pd.DataFrame) -> pd.DataFrame:
    """Generate safe, human-review next-step recommendations by student."""
    latest = activity.sort_values(["student_id", "session"]).groupby("student_id", as_index=False).tail(1)
    rows = []
    for row in latest.itertuples(index=False):
        if row.dependence >= 0.55:
            action = "reduce hint availability and add independent practice"
        elif row.mastery_estimate < 0.45:
            action = "provide scaffolded practice with short formative checks"
        elif row.trust > 0.82 and row.correct == 0:
            action = "add reflection prompt to recalibrate trust in AI feedback"
        elif row.mastery_estimate > 0.78:
            action = "increase challenge and request explanation before feedback"
        else:
            action = "continue adaptive practice with evidence-based feedback"
        rows.append({
            "student_id": row.student_id,
            "group": row.group,
            "feedback_mode": row.feedback_mode,
            "latest_mastery": row.mastery_estimate,
            "latest_trust": row.trust,
            "latest_dependence": row.dependence,
            "recommendation": action,
            "human_review_boundary": "recommendation only; teacher/researcher review required before use with real learners",
        })
    return pd.DataFrame(rows)


def summarize_mode_outcomes(activity: pd.DataFrame) -> pd.DataFrame:
    """Summarize learning, trust, and dependence by feedback condition."""
    first = activity.sort_values("session").groupby("student_id").first().reset_index()
    last = activity.sort_values("session").groupby("student_id").last().reset_index()
    merged = first[["student_id", "feedback_mode", "mastery_estimate"]].merge(
        last[["student_id", "mastery_estimate", "trust", "dependence", "hint_rate"]], on="student_id", suffixes=("_first", "_last")
    )
    merged["learning_gain"] = merged["mastery_estimate_last"] - merged["mastery_estimate_first"]
    return merged.groupby("feedback_mode").agg(
        students=("student_id", "count"),
        mean_learning_gain=("learning_gain", "mean"),
        mean_final_mastery=("mastery_estimate_last", "mean"),
        mean_trust=("trust", "mean"),
        mean_dependence=("dependence", "mean"),
        mean_hint_rate=("hint_rate", "mean"),
    ).reset_index().round(3)
