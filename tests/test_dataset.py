from pathlib import Path

from csfb.dataset import validate

ROOT=Path(__file__).resolve().parents[1]


def test_checked_in_dataset_schema_and_indices():
    result=validate([ROOT/"datasets/golden/cases.jsonl",ROOT/"datasets/synthetic/cases.jsonl",ROOT/"datasets/adversarial/cases.jsonl"])
    assert result["cases"]>=5000
    assert result["events"]>=30000
