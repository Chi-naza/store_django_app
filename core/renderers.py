from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response') if renderer_context else None
        status_code = response.status_code if response else 200

        # Already shaped by the exception handler — pass through untouched
        if isinstance(data, dict) and set(data.keys()) == {"message", "status", "data"}:
            wrapped = data
        elif isinstance(data, dict) and 'detail' in data and len(data) == 1:
            wrapped = {
                "message": str(data['detail']),
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