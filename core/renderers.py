from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    GENERIC_DETAIL_MESSAGES = {
        "ok": "Request successful.",
        # add more here as you discover other terse `detail` strings from library views
    }

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response') if renderer_context else None
        status_code = response.status_code if response else 200

        if isinstance(data, dict) and set(data.keys()) == {"message", "status", "data"}:
            wrapped = data
        elif isinstance(data, dict) and 'detail' in data and len(data) == 1:
            detail_value = str(data['detail'])
            wrapped = {
                "message": self.GENERIC_DETAIL_MESSAGES.get(detail_value, detail_value),
                "status": status_code,
                "data": None,
            }
        else:
            wrapped = {
                "message": "Success",
                "status": status_code,
                "data": data,
            }

        return super().render(wrapped, accepted_media_type, renderer_context)