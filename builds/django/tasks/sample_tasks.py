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
        output_path = input_path.replace("original", "processed")

        logger.debug(input_path)
        # try:
        #     output_path = output_path.strip()

        #     sep = '/' if '/' in output_path else '\\'
        #     path, file_name = os.path.split(output_path)
        #     if not path:
        #         path = sep

        #     file_name_parts = file_name.split('.')
        #     interpolate_output_path = os.path.join(path, f"{file_name_parts[0]}-interpolated.{file_name_parts[1]}")
        #     interpolate_output_path = interpolate_output_path.replace('processed', 'interpolated')
        # except Exception as e:
        #     video.status = 'failed'
        #     print(f"Error during processing: {e}")

        # Формируем JSON-запрос для Flask-сервера
        payload_interpolation = {
            "input_path": input_path,
            "output_path": output_path,
        }
        response_interpolation = requests.post(
            "http://practical-rife:5000/interpolate", json=payload_interpolation
        )

        if response_interpolation.status_code == 200:
            video.processed_video = output_path.replace("/media", "")
            video.status = "done"
        else:
            video.status = "failed"
            logger.info(response_interpolation.json())

        # if response_interpolation.status_code == 200:
        #     payload_upscale = {
        #         "input_path": interpolate_output_path,
        #         "output_path": output_path,
        #     }
        #     response_upscale = requests.post("http://upscale:5001/upscale", json=payload_upscale)

        #     if response_upscale.status_code == 200:
        #         video.processed_video = output_path
        #         video.status = 'done'
        #     else:
        #         video.status = 'failed'
        #         print(response_upscale.json())  # Для дебага
        # else:
        #     video.status = 'failed'
        #     print(response_interpolation.json())  # Для дебага
    except Exception as e:
        video.status = "failed"
        print(f"Error during processing: {e}")
    finally:
        video.save()
