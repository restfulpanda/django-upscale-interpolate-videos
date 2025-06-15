from tasks.sample_tasks import process_video
from unittest.mock import patch


def test_task():
    assert process_video.run(1)
    assert process_video.run(2)
    assert process_video.run(3)


@patch("tasks.sample_tasks.create_task.run")
def test_mock_task(mock_run):
    assert process_video.run(1)
    process_video.run.assert_called_once_with(1)

    assert process_video.run(2)
    assert process_video.run.call_count == 2

    assert process_video.run(3)
    assert process_video.run.call_count == 3
