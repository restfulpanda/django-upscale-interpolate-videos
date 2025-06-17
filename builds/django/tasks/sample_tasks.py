import os
import requests
import logging

from celery import shared_task
from logic.models import Video

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@shared_task
def process_video(video_id):
    video = Video.objects.get(id=video_id)
    video.status = "Processing"
    video.save()

    try:
        input_path = video.original_video.path
        interpolate_output_path = input_path.replace("original", "interpolated")
        os.makedirs("/media/interpolated", exist_ok=True)

        # output_path = input_path.replace("original", "processed")
        os.makedirs("/media/processed", exist_ok=True)

        # INTERPOLATION
        payload_interpolation = {
            "input_path": input_path,
            "output_path": interpolate_output_path,
        }
        response_interpolation = requests.post(
            "http://practical-rife:5000/interpolate", json=payload_interpolation
        )

        if response_interpolation.status_code != 200:
            logger.error(f"Interpolation failed: {response_interpolation.text}")
            video.status = "Failed"
            raise Exception("Interpolation step failed")

        # UPSCALING

        # payload_upscale = {
        #     "input_path": interpolate_output_path,
        #     "output_path": output_path,
        # }
        # response_upscale = requests.post(
        #     "http://upscale:5001/upscale", json=payload_upscale
        # )

        # if response_upscale.status_code != 200:
        #     logger.error(f"Upscale failed: {response_upscale.text}")
        #     video.status = "Failed"
        #     raise Exception("Upscale step failed")

        video.status = "Done"
        video.processed_video = interpolate_output_path
        # video.processed_video = output_path
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
