# Synthetic Human-AI learning lab

## Command

```bash
python scripts/run_synthetic_learning_lab.py
```

Optional controls:

```bash
python scripts/run_synthetic_learning_lab.py --students 360 --sessions 10 --seed 42
```

## Outputs

```text
outputs/results/synthetic_students.csv
outputs/results/synthetic_tasks.csv
outputs/results/synthetic_learning_activity.csv
outputs/results/synthetic_student_outcomes.csv
outputs/results/synthetic_feedback_mode_summary.csv
outputs/results/synthetic_fairness_audit.csv
outputs/results/synthetic_dependence_trust_summary.csv
outputs/results/synthetic_next_activity_recommendations.csv
outputs/results/synthetic_learning_summary.json
outputs/reports/synthetic_learning_report.md
outputs/audit/learning_audit_log.jsonl

outputs/figures/synthetic_learning_gains.png
outputs/figures/synthetic_trust_dependence.png
outputs/figures/synthetic_fairness_gaps.png
outputs/figures/synthetic_mastery_curves.png
outputs/figures/synthetic_recommendation_mix.png
```

## Interpretation rules

- Keep the word **synthetic** in generated files and figure captions.
- Do not claim evidence about real students from this demo.
- Treat all recommendations as research artifacts requiring teacher/researcher review.
- Use synthetic outputs to test methodology, metrics, reporting, and reproducibility only.
