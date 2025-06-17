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
        read_only_fields = [
            "id",
            "status",
            "processed_video",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        request = self.context.get("request")
        if request and instance.processed_video:
            data["processed_video"] = request.build_absolute_uri(
                instance.processed_video.url
            )
        else:
            data["processed_video"] = None

        return data
