# Methodology

## Scope and ethics boundary

This repository is a synthetic-first Human-AI learning research lab. It studies adaptive AI feedback, learning gains, dependence risk, trust calibration, and fairness using fictional learners and tasks.

It is **not** an educational product, placement system, grading system, or real student intervention tool. Real studies require consent, institutional/ethics review, privacy protection, accessibility review, educator oversight, and careful statistical design.

## Synthetic learner model

The lab simulates learners with prior knowledge, learning speed, confidence, engagement, support need, and subgroup label. These variables are fictional and are used only to exercise evaluation logic.

## Feedback conditions

| Condition | Research purpose |
| --- | --- |
| `none` | Baseline independent practice |
| `generic` | Non-personalized feedback |
| `adaptive` | Personalized task/feedback fit |
| `overhelpful` | Risk condition for dependence and over-trust |

## Outcomes

The system tracks mastery gain, correctness, effort, hint rate, adaptation quality, trust, dependence, trust miscalibration, independence score, and over-reliance risk.

## Fairness audit

Subgroup analysis estimates differences in learning gain, success rate, over-reliance risk, and trust miscalibration. These are synthetic regression-test indicators, not real demographic findings.

## Interpretation limits

Synthetic results can validate code paths and research design, but they cannot prove that AI feedback improves real student outcomes. Any real study must use appropriate experimental design, privacy controls, and educator judgment.
