"""Run the complete synthetic Human-AI personalized learning laboratory.

This command uses only fictional students and learning activity. It evaluates
adaptive feedback, learning gains, trust, dependence risk, fairness, and next-step
recommendations without using real student data.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from learninglab.adaptation import evaluate_adaptation_quality, next_activity_recommendations, summarize_mode_outcomes
from learninglab.audit import append_record, verify_log
from learninglab.config import ensure_output_dirs, set_seed
from learninglab.metrics import dependence_summary, fairness_audit, fairness_gaps, student_outcomes
from learninglab.reporting import write_learning_report
from learninglab.synthetic import SyntheticLearningConfig, generate_synthetic_learning_data
from learninglab.visualization import plot_dependence_trust, plot_fairness_gaps, plot_learning_gains, plot_mastery_curves, plot_recommendation_mix


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a synthetic Human-AI personalized learning lab.")
    parser.add_argument("--students", type=int, default=240)
    parser.add_argument("--sessions", type=int, default=8)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()

    set_seed(args.seed)
    data = generate_synthetic_learning_data(SyntheticLearningConfig(students=args.students, sessions=args.sessions, seed=args.seed))
    students = data["students"]
    tasks = data["tasks"]
    activity = evaluate_adaptation_quality(data["activity"])
    outcomes = student_outcomes(activity)
    fairness = fairness_audit(outcomes)
    gaps = fairness_gaps(outcomes)
    dependence = dependence_summary(outcomes)
    recommendations = next_activity_recommendations(activity)
    mode_summary = summarize_mode_outcomes(activity)

    outputs = ensure_output_dirs(args.output_dir)
    students.to_csv(outputs["results"] / "synthetic_students.csv", index=False)
    tasks.to_csv(outputs["results"] / "synthetic_tasks.csv", index=False)
    activity.to_csv(outputs["results"] / "synthetic_learning_activity.csv", index=False)
    outcomes.to_csv(outputs["results"] / "synthetic_student_outcomes.csv", index=False)
    mode_summary.to_csv(outputs["results"] / "synthetic_feedback_mode_summary.csv", index=False)
    fairness.to_csv(outputs["results"] / "synthetic_fairness_audit.csv", index=False)
    dependence.to_csv(outputs["results"] / "synthetic_dependence_trust_summary.csv", index=False)
    recommendations.to_csv(outputs["results"] / "synthetic_next_activity_recommendations.csv", index=False)

    plot_learning_gains(outcomes, outputs["figures"] / "synthetic_learning_gains.png")
    plot_dependence_trust(outcomes, outputs["figures"] / "synthetic_trust_dependence.png")
    plot_fairness_gaps(fairness, outputs["figures"] / "synthetic_fairness_gaps.png")
    plot_mastery_curves(activity, outputs["figures"] / "synthetic_mastery_curves.png")
    plot_recommendation_mix(recommendations, outputs["figures"] / "synthetic_recommendation_mix.png")

    audit_path = outputs["audit"] / "learning_audit_log.jsonl"
    append_record(audit_path, {
        "experiment": "synthetic_human_ai_learning_lab",
        "seed": args.seed,
        "students": args.students,
        "sessions": args.sessions,
        "feedback_modes": sorted(activity["feedback_mode"].unique().tolist()),
        "fairness_gaps": gaps,
        "boundary": "Synthetic research only; no real student data or educational decisions.",
    })
    summary = {
        "data_origin": "synthetic fictional learning experiment",
        "seed": args.seed,
        "students": args.students,
        "sessions": args.sessions,
        "feedback_modes": sorted(activity["feedback_mode"].unique().tolist()),
        "fairness_gaps": gaps,
        "audit_log": verify_log(audit_path),
        "human_review_boundary": "Recommendations are research artifacts only; teacher/researcher review required before use with real learners.",
    }
    (outputs["results"] / "synthetic_learning_summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    write_learning_report(outputs["reports"] / "synthetic_learning_report.md", summary, mode_summary, fairness)
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
