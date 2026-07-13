"""Figures for synthetic Human-AI learning experiments."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def _path(path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    return destination


def plot_learning_gains(outcomes: pd.DataFrame, path: str | Path) -> None:
    summary = outcomes.groupby("feedback_mode")["learning_gain"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.bar(summary.index, summary.values)
    ax.set(title="Synthetic learning gain by feedback mode", xlabel="Feedback mode", ylabel="Mean mastery gain")
    ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout(); fig.savefig(_path(path), dpi=250); plt.close(fig)


def plot_dependence_trust(outcomes: pd.DataFrame, path: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    for mode, group in outcomes.groupby("feedback_mode"):
        ax.scatter(group["trust"], group["dependence"], s=18, alpha=0.55, label=mode)
    ax.set(title="Trust vs dependence risk", xlabel="Final trust", ylabel="Final dependence")
    ax.grid(True, alpha=0.25); ax.legend()
    fig.tight_layout(); fig.savefig(_path(path), dpi=250); plt.close(fig)


def plot_fairness_gaps(fairness: pd.DataFrame, path: str | Path) -> None:
    pivot = fairness.pivot(index="feedback_mode", columns="group", values="mean_gain")
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    pivot.plot(kind="bar", ax=ax)
    ax.set(title="Synthetic learning gains by group and feedback mode", xlabel="Feedback mode", ylabel="Mean gain")
    ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout(); fig.savefig(_path(path), dpi=250); plt.close(fig)


def plot_mastery_curves(activity: pd.DataFrame, path: str | Path) -> None:
    curves = activity.groupby(["feedback_mode", "session"])["mastery_estimate"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8.5, 5.0))
    for mode, group in curves.groupby("feedback_mode"):
        ax.plot(group["session"], group["mastery_estimate"], marker="o", label=mode)
    ax.set(title="Synthetic mastery trajectory", xlabel="Session", ylabel="Mean mastery estimate")
    ax.grid(True, alpha=0.25); ax.legend()
    fig.tight_layout(); fig.savefig(_path(path), dpi=250); plt.close(fig)


def plot_recommendation_mix(recommendations: pd.DataFrame, path: str | Path) -> None:
    counts = recommendations["recommendation"].value_counts().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.barh(counts.index, counts.values)
    ax.set(title="Recommended next-step interventions", xlabel="Student count", ylabel="Recommendation")
    ax.grid(True, axis="x", alpha=0.25)
    fig.tight_layout(); fig.savefig(_path(path), dpi=250); plt.close(fig)
