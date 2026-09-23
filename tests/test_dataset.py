from csfb.cli import FILES
from csfb.dataset import validate


def test_checked_in_dataset_schema_and_indices():
    result=validate(FILES)
    assert result["cases"]>=5000
    assert result["events"]>=30000
