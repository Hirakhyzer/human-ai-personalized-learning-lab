from pathlib import Path

from learninglab.audit import append_record, verify_log


def test_audit_log_verifies(tmp_path: Path):
    path = tmp_path / "audit.jsonl"
    append_record(path, {"experiment": "unit", "seed": 1})
    append_record(path, {"experiment": "unit", "seed": 2})
    status = verify_log(path)
    assert status["valid"]
    assert status["records"] == 2
