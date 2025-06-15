import json

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data):
        token = data.get("token", None)

        if token is not None and isinstance(token, bytes):
            data["token"] = token.decode("utf-8")

        return json.dumps({"user": data})
