"""Deterministic synthetic Human-AI learning experiment generator.

All students, tasks, groups, and outcomes are fictional. The generator is for
privacy-preserving research demonstrations and must not be interpreted as real
student evidence or educational advice.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


DOMAINS = ["math", "programming", "reading", "science"]
FEEDBACK_MODES = ["none", "generic", "adaptive", "overhelpful"]
GROUPS = ["A", "B", "C"]


@dataclass(frozen=True)
class SyntheticLearningConfig:
    students: int = 240
    sessions: int = 8
    seed: int = 42

    def __post_init__(self) -> None:
        if self.students < 40:
            raise ValueError("Use at least 40 synthetic students for subgroup analysis.")
        if self.sessions < 3:
            raise ValueError("Use at least 3 learning sessions.")


def generate_synthetic_learning_data(config: SyntheticLearningConfig | None = None) -> dict[str, pd.DataFrame]:
    """Generate students, tasks, session activity, and synthetic outcome labels."""
    cfg = config or SyntheticLearningConfig()
    rng = np.random.default_rng(cfg.seed)
    students = _students(cfg, rng)
    tasks = _tasks(rng)
    activity = _activity(cfg, students, tasks, rng)
    return {"students": students, "tasks": tasks, "activity": activity}


def _students(cfg: SyntheticLearningConfig, rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    for index in range(cfg.students):
        group = GROUPS[index % len(GROUPS)]
        prior = float(np.clip(rng.beta(2.5, 2.8) + {"A": 0.04, "B": -0.03, "C": 0.0}[group], 0.05, 0.95))
        learning_speed = float(np.clip(rng.normal(0.12 + 0.06 * prior, 0.035), 0.03, 0.28))
        confidence = float(np.clip(rng.normal(0.52 + 0.25 * prior, 0.12), 0.05, 0.98))
        engagement = float(np.clip(rng.normal(0.62, 0.15), 0.1, 1.0))
        support_need = float(np.clip(1.0 - prior + rng.normal(0, 0.10), 0.05, 0.95))
        rows.append({
            "student_index": index,
            "student_id": f"S-{index+1:04d}",
            "group": group,
            "prior_knowledge": round(prior, 3),
            "learning_speed": round(learning_speed, 3),
            "confidence": round(confidence, 3),
            "engagement": round(engagement, 3),
            "support_need": round(support_need, 3),
        })
    return pd.DataFrame(rows)


def _tasks(rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    for domain in DOMAINS:
        for level in range(1, 7):
            rows.append({
                "task_id": f"{domain[:3].upper()}-{level:02d}",
                "domain": domain,
                "difficulty": round(0.15 + level * 0.12 + float(rng.normal(0, 0.02)), 3),
                "concept": f"{domain}_concept_{level}",
            })
    return pd.DataFrame(rows)


def _activity(cfg: SyntheticLearningConfig, students: pd.DataFrame, tasks: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    mode_cycle = np.resize(np.array(FEEDBACK_MODES), len(students))
    for student, mode in zip(students.itertuples(index=False), mode_cycle):
        mastery = float(student.prior_knowledge)
        trust = float(np.clip(0.42 + 0.25 * student.confidence, 0.05, 0.95))
        dependence = 0.05
        for session in range(1, cfg.sessions + 1):
            domain = DOMAINS[(session + int(student.student_index)) % len(DOMAINS)]
            available = tasks.loc[tasks["domain"] == domain].copy()
            # Adaptive mode picks closer difficulty; overhelpful tends to keep tasks too easy.
            if mode == "adaptive":
                target = mastery + 0.12
            elif mode == "overhelpful":
                target = mastery - 0.05
            elif mode == "generic":
                target = 0.55
            else:
                target = 0.50
            chosen = available.iloc[(available["difficulty"] - target).abs().argsort().iloc[0]]
            feedback_quality = {
                "none": 0.00,
                "generic": 0.45,
                "adaptive": 0.75 + 0.10 * (1 - abs(chosen["difficulty"] - target)),
                "overhelpful": 0.88,
            }[mode]
            challenge_fit = float(np.clip(1.0 - abs(chosen["difficulty"] - (mastery + 0.10)), 0, 1))
            effort = float(np.clip(student.engagement * (0.75 + 0.25 * challenge_fit) - dependence * 0.18 + rng.normal(0, 0.05), 0.05, 1.0))
            hint_rate = float(np.clip((1 - mastery) * (0.25 + feedback_quality) + (0.18 if mode == "overhelpful" else 0.0) + rng.normal(0, 0.04), 0, 1))
            correctness_prob = float(np.clip(0.18 + 0.62 * mastery + 0.18 * challenge_fit + 0.12 * feedback_quality - 0.06 * dependence, 0.05, 0.98))
            correct = int(rng.random() < correctness_prob)
            gain = student.learning_speed * (0.55 * effort + 0.45 * feedback_quality) * (1.05 if correct else 0.65)
            if mode == "overhelpful":
                gain *= 0.78
                dependence += 0.055 + 0.04 * hint_rate
                trust += 0.055
            elif mode == "adaptive":
                dependence += 0.018 * hint_rate
                trust += 0.020 * correct - 0.010 * (1 - correct)
            elif mode == "generic":
                dependence += 0.012 * hint_rate
                trust += 0.008 * correct
            else:
                dependence += 0.002
                trust -= 0.003
            mastery = float(np.clip(mastery + gain, 0, 1))
            dependence = float(np.clip(dependence, 0, 1))
            trust = float(np.clip(trust, 0, 1))
            rows.append({
                "student_id": student.student_id,
                "group": student.group,
                "session": session,
                "feedback_mode": mode,
                "task_id": chosen["task_id"],
                "domain": domain,
                "task_difficulty": float(chosen["difficulty"]),
                "mastery_estimate": round(mastery, 3),
                "correct": correct,
                "effort": round(effort, 3),
                "hint_rate": round(hint_rate, 3),
                "feedback_quality": round(feedback_quality, 3),
                "trust": round(trust, 3),
                "dependence": round(dependence, 3),
                "challenge_fit": round(challenge_fit, 3),
            })
    return pd.DataFrame(rows)
