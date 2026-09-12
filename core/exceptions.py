from rest_framework.views import exception_handler as drf_exception_handler


def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is not None:
        original = response.data
        response.data = {
            "message": extract_message(original),
            "status": response.status_code,
            "data": None if is_simple_detail(original) else original,
        }

    return response


def is_simple_detail(data):
    return isinstance(data, dict) and 'detail' in data and len(data) == 1


def extract_message(data):
    if isinstance(data, dict):
        if 'detail' in data and len(data) == 1:
            return str(data['detail'])
        parts = []
        for field, errors in data.items():
            if isinstance(errors, list):
                parts.append(f"{field}: {' '.join(str(e) for e in errors)}")
            else:
                parts.append(f"{field}: {errors}")
        return " ".join(parts)
    if isinstance(data, list):
        return " ".join(str(item) for item in data)
    return str(data)