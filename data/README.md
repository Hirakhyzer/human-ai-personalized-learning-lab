# Student data boundary

This repository runs without real student data. The default pipeline uses fictional synthetic learners and tasks.

## Synthetic default

Run:

```bash
python scripts/run_synthetic_learning_lab.py
```

## Future approved data

Real student data must not be committed to Git. Place approved local datasets only under:

```text
data/raw/
```

That folder is ignored by Git.

Minimum fields for an approved adapter:

| Field | Purpose |
| --- | --- |
| learner_id | Pseudonymous identifier |
| session | Learning time/order |
| task_id/domain | Activity context |
| feedback_condition | Experimental condition |
| score/correctness | Performance outcome |
| hint_use | Dependence proxy |
| trust survey item | Trust calibration analysis |
| consent/approval metadata | Governance record |

Do not use real data without authorization, privacy review, and educator/research governance.
