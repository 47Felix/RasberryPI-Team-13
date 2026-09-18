import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from calibration import raw_to_celsius


def test_raw_to_celsius_interpolates_linearly():
    temp_c = raw_to_celsius(raw=300, raw_low=200, temp_low_c=10.0, raw_high=400, temp_high_c=30.0)
    assert temp_c == 20.0


def test_raw_to_celsius_at_reference_points():
    assert raw_to_celsius(raw=200, raw_low=200, temp_low_c=10.0, raw_high=400, temp_high_c=30.0) == 10.0
    assert raw_to_celsius(raw=400, raw_low=200, temp_low_c=10.0, raw_high=400, temp_high_c=30.0) == 30.0
