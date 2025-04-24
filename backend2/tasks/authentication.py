import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from django.conf import settings

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        
        try:
            prefix, token = auth_header.split(' ')
            if prefix != 'Bearer':
                raise AuthenticationFailed('Invalid token prefix')
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        except (jwt.DecodeError, ValueError):
            raise AuthenticationFailed('Invalid token')

        try:
            user, _ = User.objects.get_or_create(
                username=payload['email'],  # assuming token contains 'email'
                defaults={"password": "admin"}  # dummy password; not used
            )
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')

        return (user, None)
