import pytest
from pydantic import ValidationError
from src.schema import Measurement


def test_valid_measurement_is_accepted():
    m = Measurement(strain="strain_a", replicate=1, time_h=2.0, od600=0.5)
    assert m.od600 == 0.5


def test_negative_od_is_rejected():
    with pytest.raises(ValidationError):
        Measurement(strain="strain_a", replicate=1, time_h=2.0, od600=-3)