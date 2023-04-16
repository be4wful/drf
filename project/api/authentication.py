from rest_framework.authentication import TokenAuthentication


class AuthBearer(TokenAuthentication):
    keyword = 'Bearer'
