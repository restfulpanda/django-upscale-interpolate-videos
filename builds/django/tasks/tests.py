# import pytest
# from unittest.mock import patch, MagicMock
# from logic.models import Video
# from tasks.sample_tasks import process_video

# @pytest.mark.django_db
# def test_process_video_success(client, tmp_path):
#     original_path = tmp_path / "original" / "video.mp4"
#     original_path.parent.mkdir(parents=True, exist_ok=True)
#     original_path.write_text("fake data")

#     video = Video.objects.create(
#         original_video=str(original_path),
#         status='pending'
#     )

#     mock_response = MagicMock()
#     mock_response.status_code = 200

#     with patch("logic.tasks.requests.post", return_value=mock_response):
#         process_video(video.id)

#     video.refresh_from_db()
#     assert video.status == "done"
#     assert "processed" in video.processed_video


# @pytest.mark.django_db
# def test_process_video_fail_response(client, tmp_path):
#     original_path = tmp_path / "original" / "video.mp4"
#     original_path.parent.mkdir(parents=True, exist_ok=True)
#     original_path.write_text("fake data")

#     video = Video.objects.create(
#         original_video=str(original_path),
#         status='pending'
#     )

#     mock_response = MagicMock()
#     mock_response.status_code = 500
#     mock_response.json.return_value = {"error": "Internal Server Error"}

#     with patch("logic.tasks.requests.post", return_value=mock_response):
#         process_video(video.id)

#     video.refresh_from_db()
#     assert video.status == "failed"


# @pytest.mark.django_db
# def test_process_video_exception(client, tmp_path):
#     original_path = tmp_path / "original" / "video.mp4"
#     original_path.parent.mkdir(parents=True, exist_ok=True)
#     original_path.write_text("fake data")

#     video = Video.objects.create(
#         original_video=str(original_path),
#         status='pending'
#     )

#     with patch("logic.tasks.requests.post", side_effect=Exception("Network error")):
#         process_video(video.id)

#     video.refresh_from_db()
#     assert video.status == "failed"
