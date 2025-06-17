from rest_framework import serializers
from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "id",
            "status",
            "original_video",
            "processed_video",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "status": {"read_only": True},
            "processed_video": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)

        request = self.context.get("request")
        if request and instance.processed_video and instance.processed_video.name:
            try:
                data["processed_video"] = request.build_absolute_uri(instance.processed_video.url)
            except ValueError:
                data["processed_video"] = None
        else:
            data["processed_video"] = None

        return data
