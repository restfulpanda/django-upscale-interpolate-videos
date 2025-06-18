import os
import requests
import logging

from celery import shared_task
from logic.models import Video

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def _call_interpolation_server(
    video: Video,
    input_path: str,
    output_path: str
) -> str:
    payload = {
        "input_path": input_path,
        "output_path": output_path,
    }
    response = requests.post(
        "http://practical-rife:5000/interpolate", json=payload
    )

    if response.status_code != 200:
        logger.error(f"Interpolation failed: {response.text}")
        video.status = "Failed"
        raise Exception(f"Interpolation step failed with error {response.text}")
    
    data = response.json()
    file_path = data.get("output")
    if not file_path:
        raise KeyError("Key 'output' is not in response")
    
    return file_path

def _call_upscale_server(
    video: Video,
    input_path: str,
    output_path: str
) -> str:
    payload = {
        "input_path": input_path,
        "output_path": output_path,
    }
    response = requests.post(
        "http://upscale:5001/upscale", json=payload
    )

    if response.status_code != 200:
        logger.error(f"Upscale failed: {response.text}")
        video.status = "Failed"
        raise Exception(f"Upscale step failed with error {response.text}")

    data = response.json()
    file_path = data.get("output")
    if not file_path:
        raise KeyError("Key 'output' is not in response")
    
    return file_path

@shared_task
def process_video(video_id):
    video = Video.objects.get(id=video_id)
    video.status = "Processing"
    video.save()

    try:
        input_path = video.original_video.path
        interpolation_output_path = input_path.replace("original", "interpolated")
        os.makedirs("/media/interpolated", exist_ok=True)

        upscale_output_path = input_path.replace("original", "processed")
        os.makedirs("/media/processed", exist_ok=True)

        interpolated_file_path = _call_interpolation_server(video, input_path, interpolation_output_path)
        interpolated_upscaled_file_path = _call_upscale_server(video, interpolated_file_path, upscale_output_path)
            
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
