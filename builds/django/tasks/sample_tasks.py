import os
import requests
import logging

from celery import shared_task
from logic.models import Video

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def _call_interpolation_server(video: Video, input_path: str, output_path: str) -> str:
    """
    Calls the video interpolation server and returns the path to the processed file.

    Args:
        video: Video object to update the status of
        input_path: Path to the input video file
        output_path: Path to save the result

    Returns:
        Path to the processed video file

    Raises:
        Exception: If the request to the server failed
        KeyError: If the 'output' key is missing from the response
    """
    payload = {
        "input_path": input_path,
        "output_path": output_path,
    }
    try:
        response = requests.post(
            "http://practical-rife:5000/interpolate", json=payload, timeout=60
        )
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        error_msg = f"Interpolation request failed: {str(e)}"
        logger.error(error_msg)
        video.status = "Failed"
        raise Exception(error_msg) from e

    try:
        data = response.json()
        file_path = data["output"]
        return file_path

    except (KeyError, ValueError) as e:
        error_msg = f"Invalid server response: {str(e)}"
        logger.error(error_msg)
        video.status = "Failed"
        raise Exception(error_msg) from e


def _call_upscale_server(video: Video, input_path: str, output_path: str) -> str:
    """
    Calls the video upscale server and returns the path to the processed file.

    Args:
        video: Video object to update the status of
        input_path: Path to the input video file
        output_path: Path to save the result

    Returns:
        Path to the processed video file

    Raises:
        Exception: If the request to the server failed
        KeyError: If the 'output' key is missing from the response
    """
    payload = {
        "input_path": input_path,
        "output_path": output_path,
    }
    try:
        response = requests.post("http://esrgan:5001/upscale", json=payload, timeout=60)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        error_msg = f"Interpolation request failed: {str(e)}"
        logger.error(error_msg)
        video.status = "Failed"
        raise Exception(error_msg) from e

    try:
        data = response.json()
        file_path = data["output"]
        return file_path

    except (KeyError, ValueError) as e:
        error_msg = f"Invalid server response: {str(e)}"
        logger.error(error_msg)
        video.status = "Failed"
        raise Exception(error_msg) from e


@shared_task
def process_video(video_id) -> dict:
    """
    Processes video interpolation and upscale using video_id to get original video path.
    Calls interpolation and upscale servers in same docker network.

    Args:
        video_id (int): ID of video to enhance FPS and resolution.

    Returns:
        dict: Contains video ID and status.
    """
    video = Video.objects.get(id=video_id)
    video.status = "Processing"
    video.save()

    try:
        input_path = video.original_video.path
        interpolation_output_path = input_path.replace("original", "interpolated")
        os.makedirs("/media/interpolated", exist_ok=True)

        upscale_output_path = input_path.replace("original", "processed")
        os.makedirs("/media/processed", exist_ok=True)

        interpolated_file_path = _call_interpolation_server(
            video, input_path, interpolation_output_path
        )
        interpolated_upscaled_file_path = _call_upscale_server(
            video, interpolated_file_path, upscale_output_path
        )

        video.status = "Done"
        video.processed_video = interpolated_upscaled_file_path

        result = {
            "video_id": video_id,
            "video_status": video.status,
            "note": "To download video try /videos/download/{video_id}",
        }
    except Exception as e:
        video.status = "Failed"
        result = {
            "video_id": video_id,
            "video_status": video.status,
            "error": str(e),
        }
        logger.error(f"Error processing video {video_id}: {e}")
    finally:
        video.save()

    return result
