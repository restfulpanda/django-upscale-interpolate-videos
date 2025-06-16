import json

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Переопределяет стандартный метод render для оборачивания данных в ключ "user"
        """
        token = data.get("token", None)

        if token is not None and isinstance(token, bytes):
            data["token"] = token.decode("utf-8")

        return json.dumps({"user": data})
