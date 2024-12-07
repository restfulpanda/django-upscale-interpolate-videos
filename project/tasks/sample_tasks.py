import time

from celery import shared_task
from logic.models import Video
import ffmpeg

@shared_task
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True

@shared_task
def process_video(video_id):
    video = Video.objects.get(id=video_id)
    video.status = 'processing'
    video.save()

    try:
        input_path = video.original_video.path
        output_path = input_path.replace('original', 'processed')
        ffmpeg.input(input_path).output(output_path, vf="scale=1280:720").run()

        video.processed_video = output_path.replace('/media/', '')
        video.status = 'done'
    except Exception as e:
        video.status = 'failed'
    finally:
        video.save()