from learninglab.synthetic import SyntheticLearningConfig, generate_synthetic_learning_data


def test_synthetic_learning_data_is_reproducible():
    cfg = SyntheticLearningConfig(students=48, sessions=4, seed=7)
    first = generate_synthetic_learning_data(cfg)
    second = generate_synthetic_learning_data(cfg)
    assert first["students"].equals(second["students"])
    assert first["tasks"].equals(second["tasks"])
    assert first["activity"].equals(second["activity"])


def test_synthetic_activity_has_all_feedback_modes():
    data = generate_synthetic_learning_data(SyntheticLearningConfig(students=48, sessions=4, seed=3))
    assert set(data["activity"]["feedback_mode"]) == {"none", "generic", "adaptive", "overhelpful"}
    assert data["activity"]["mastery_estimate"].between(0, 1).all()
    assert data["activity"]["trust"].between(0, 1).all()
