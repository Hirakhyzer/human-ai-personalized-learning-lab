from learninglab.adaptation import evaluate_adaptation_quality, next_activity_recommendations
from learninglab.metrics import fairness_audit, student_outcomes
from learninglab.synthetic import SyntheticLearningConfig, generate_synthetic_learning_data


def test_end_to_end_synthetic_pipeline_runs_without_real_data():
    data = generate_synthetic_learning_data(SyntheticLearningConfig(students=48, sessions=4, seed=21))
    activity = evaluate_adaptation_quality(data["activity"])
    outcomes = student_outcomes(activity)
    fairness = fairness_audit(outcomes)
    recommendations = next_activity_recommendations(activity)
    assert len(activity) == 48 * 4
    assert not outcomes.empty
    assert not fairness.empty
    assert not recommendations.empty
    assert outcomes["learning_gain"].notna().all()
