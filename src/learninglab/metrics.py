"""Learning outcome, dependence, trust, and fairness metrics."""

from __future__ import annotations

import pandas as pd


def student_outcomes(activity: pd.DataFrame) -> pd.DataFrame:
    """Return one row per synthetic student with outcome indicators."""
    ordered = activity.sort_values(["student_id", "session"])
    first = ordered.groupby("student_id").first().reset_index()
    last = ordered.groupby("student_id").last().reset_index()
    outcomes = first[["student_id", "group", "feedback_mode", "mastery_estimate"]].merge(
        last[["student_id", "mastery_estimate", "trust", "dependence", "hint_rate"]], on="student_id", suffixes=("_pre", "_post")
    )
    accuracy = ordered.groupby("student_id")["correct"].mean().rename("mean_accuracy").reset_index()
    effort = ordered.groupby("student_id")["effort"].mean().rename("mean_effort").reset_index()
    outcomes = outcomes.merge(accuracy, on="student_id").merge(effort, on="student_id")
    outcomes["learning_gain"] = outcomes["mastery_estimate_post"] - outcomes["mastery_estimate_pre"]
    outcomes["independence_score"] = (1 - outcomes["dependence"]).clip(0, 1)
    outcomes["over_reliance_risk"] = ((outcomes["dependence"] > 0.55) & (outcomes["hint_rate"] > 0.45)).astype(int)
    outcomes["trust_miscalibration"] = (outcomes["trust"] - outcomes["mean_accuracy"]).abs()
    outcomes["success"] = (outcomes["learning_gain"] >= 0.10).astype(int)
    return outcomes.round(3)


def fairness_audit(outcomes: pd.DataFrame) -> pd.DataFrame:
    """Compute subgroup gaps by feedback mode and learner group."""
    group_metrics = outcomes.groupby(["feedback_mode", "group"]).agg(
        students=("student_id", "count"),
        mean_gain=("learning_gain", "mean"),
        mean_final_mastery=("mastery_estimate_post", "mean"),
        over_reliance_rate=("over_reliance_risk", "mean"),
        trust_miscalibration=("trust_miscalibration", "mean"),
        success_rate=("success", "mean"),
    ).reset_index().round(3)
    return group_metrics


def fairness_gaps(outcomes: pd.DataFrame) -> dict[str, float]:
    """Return maximum subgroup disparities for key outcomes."""
    by_group = outcomes.groupby("group").agg(
        gain=("learning_gain", "mean"),
        success=("success", "mean"),
        reliance=("over_reliance_risk", "mean"),
        trust_gap=("trust_miscalibration", "mean"),
    )
    return {
        "max_learning_gain_gap": float(by_group["gain"].max() - by_group["gain"].min()),
        "max_success_rate_gap": float(by_group["success"].max() - by_group["success"].min()),
        "max_over_reliance_gap": float(by_group["reliance"].max() - by_group["reliance"].min()),
        "max_trust_miscalibration_gap": float(by_group["trust_gap"].max() - by_group["trust_gap"].min()),
    }


def dependence_summary(outcomes: pd.DataFrame) -> pd.DataFrame:
    """Summarize dependence and trust by experimental condition."""
    return outcomes.groupby("feedback_mode").agg(
        mean_gain=("learning_gain", "mean"),
        independence=("independence_score", "mean"),
        over_reliance_rate=("over_reliance_risk", "mean"),
        trust_miscalibration=("trust_miscalibration", "mean"),
    ).reset_index().round(3)
