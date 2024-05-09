import pytest

from retrochatbot.framework.domain.usecases import calculate_participant_buffer_size


@pytest.mark.parametrize(
    argnames=["input_participant_count", "expected_buffer_size"],
    argvalues=[
        [1, 1440],
        [2, 640],
        [3, 320],
        [4, 240],
        [5, 160],
        [6, 80],
    ],
)
def test_calculate_participant_buffer_sise(
    input_participant_count: int,
    expected_buffer_size: int,
):
    actual_buffer_size = calculate_participant_buffer_size(
        participant_count=input_participant_count
    )
    assert actual_buffer_size == expected_buffer_size
