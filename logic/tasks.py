import ffmpeg
from celery import shared_task
from .models import Video

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