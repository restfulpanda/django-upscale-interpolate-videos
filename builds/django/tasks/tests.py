from unittest.mock import patch, MagicMock

import pytest
from django.contrib.auth import get_user_model

from logic.models import Video
from tasks.sample_tasks import process_video

pytestmark = pytest.mark.django_db
User = get_user_model()

@pytest.fixture
def test_user(db):
    return User.objects.create_user(email="testuser@test.user", username="testuser", password="testpass")

def create_test_video_file(tmp_path):
    original_path = tmp_path / "original" / "video.mp4"
    original_path.parent.mkdir(parents=True, exist_ok=True)
    original_path.write_text("fake data")
    return original_path


def create_video_instance(original_path, owner):
    return Video.objects.create(
        original_video=str(original_path),
        status="Pending",
        owner=owner,
    )


def test_process_video_fail_response(tmp_path, test_user):
    original_path = create_test_video_file(tmp_path)
    video = create_video_instance(original_path, test_user)

    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.json.return_value = {"error": "Internal Server Error"}

    with patch("tasks.sample_tasks.requests.post", return_value=mock_response):
        process_video(video.id)

    video.refresh_from_db()
    assert video.status == "Failed"


def test_process_video_exception(tmp_path, test_user):
    original_path = create_test_video_file(tmp_path)
    video = create_video_instance(original_path, test_user)

    with patch("tasks.sample_tasks.requests.post", side_effect=Exception("Network error")):
        process_video(video.id)

    video.refresh_from_db()
    assert video.status == "Failed"
