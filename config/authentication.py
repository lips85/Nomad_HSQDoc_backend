from multiprocessing import AuthenticationError
import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # token = request.headers.get("Jwt")
        try:
            token = request.COOKIES["jwt"]
            decoded = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
            )
            pk = decoded.get("pk")
            if not pk:
                raise AuthenticationFailed("Invalid Token")
            try:
                user = User.objects.get(pk=pk)
                return (user, None)
            except User.DoesNotExist:
                raise AuthenticationError("User Not Found")
        except:
            return None