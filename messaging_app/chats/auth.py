from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

class CustomJWTAuthentication(JWTAuthentication):
    """
    Extend JWT authentication if needed, e.g., add custom claims.
    """
    pass

