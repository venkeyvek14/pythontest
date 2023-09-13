from functools import wraps
from django.http import JsonResponse
from django.conf import settings
import jwt

def verify_token(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            if not token:
                return JsonResponse({"message": "Token is missing", "status":401}, status=401)

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']

            request.user_id = user_id
            return view_func(request, *args, **kwargs)
        except jwt.ExpiredSignatureError as ExpiredSignatureError:
            return JsonResponse({"message": "Token has expired", "status":401}, status=401)
        except jwt.DecodeError as DecodeError:
            return JsonResponse({"message": "Invalid token", "status":401}, status=401)

    return wrapper
