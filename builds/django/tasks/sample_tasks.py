import requests
import logging

from celery import shared_task
from logic.models import Video

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@shared_task
def process_video(video_id):
    video = Video.objects.get(id=video_id)
    video.status = "processing"
    video.save()

    try:
        input_path = video.original_video.path
        interpolate_output_path = input_path.replace("processed", "interpolated")
        # output_path = input_path.replace("original", "processed")

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
