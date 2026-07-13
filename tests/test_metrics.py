from learninglab.adaptation import evaluate_adaptation_quality, next_activity_recommendations, summarize_mode_outcomes
from learninglab.metrics import fairness_audit, fairness_gaps, student_outcomes
from learninglab.synthetic import SyntheticLearningConfig, generate_synthetic_learning_data


def test_metrics_pipeline_outputs_expected_columns():
    data = generate_synthetic_learning_data(SyntheticLearningConfig(students=60, sessions=5, seed=11))
    activity = evaluate_adaptation_quality(data["activity"])
    outcomes = student_outcomes(activity)
    fairness = fairness_audit(outcomes)
    gaps = fairness_gaps(outcomes)
    recommendations = next_activity_recommendations(activity)
    mode_summary = summarize_mode_outcomes(activity)
    assert {"learning_gain", "independence_score", "over_reliance_risk", "trust_miscalibration"}.issubset(outcomes.columns)
    assert not fairness.empty
    assert "max_learning_gain_gap" in gaps
    assert len(recommendations) == outcomes["student_id"].nunique()
    assert set(mode_summary["feedback_mode"]) == {"none", "generic", "adaptive", "overhelpful"}
