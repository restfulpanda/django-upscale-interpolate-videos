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
        interpolate_output_path = input_path.replace('processed', 'interpolated')
        output_path = input_path.replace("original", "processed")

        payload_interpolation = {
            "input_path": input_path,
            "output_path": interpolate_output_path,
        }
        response_interpolation = requests.post(
            "http://practical-rife:5000/interpolate", json=payload_interpolation
        )

        if response_interpolation.status_code == 200:
            payload_upscale = {
                "input_path": interpolate_output_path,
                "output_path": output_path,
            }
            response_upscale = requests.post("http://upscale:5001/upscale", json=payload_upscale)

            if response_upscale.status_code == 200:
                video.processed_video = output_path
                video.status = 'done'
            else:
                video.status = 'failed'
                logger.debug(response_upscale.json())
        else:
            video.status = 'failed'
            logger.debug(response_interpolation.json())
    except Exception as e:
        video.status = "failed"
        print(f"Error during processing: {e}")
    finally:
        video.save()
