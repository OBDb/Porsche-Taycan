import glob
import os
import pytest
from pathlib import Path
from typing import Dict, Any

# These will be imported from the schemas repository
from schemas.python.json_formatter import format_file
from schemas.python.signals_testing import obd_yaml_testrunner, find_yaml_test_cases

REPO_ROOT = Path(__file__).parent.parent.absolute()
TEST_CASES_DIR = os.path.join(Path(__file__).parent, 'test_cases')

@pytest.mark.parametrize(
    "yaml_path",
    [v for v in find_yaml_test_cases(TEST_CASES_DIR).values()],
    ids=lambda p: f"MY{os.path.splitext(os.path.basename(p))[0]}"
)
def test_signals(yaml_path: str):
    """Test signal decoding against known responses."""
    try:
        obd_yaml_testrunner(yaml_path)
    except Exception as e:
        pytest.fail(f"Failed to run tests from {yaml_path}: {e}")

def get_json_files():
    """Get all JSON files from the signalsets/v3 directory."""
    signalsets_path = os.path.join(REPO_ROOT, 'signalsets', 'v3')
    json_files = glob.glob(os.path.join(signalsets_path, '*.json'))
    # Convert full paths to relative filenames
    return [os.path.basename(f) for f in json_files]

@pytest.mark.parametrize("test_file",
    get_json_files(),
    ids=lambda x: x.split('.')[0].replace('-', '_')  # Create readable test IDs
)
def test_formatting(test_file):
    """Test signal set formatting for all vehicle models in signalsets/v3/."""
    signalset_path = os.path.join(REPO_ROOT, 'signalsets', 'v3', test_file)

    formatted = format_file(signalset_path)

    with open(signalset_path) as f:
        assert f.read() == formatted

if __name__ == '__main__':
    pytest.main([__file__])