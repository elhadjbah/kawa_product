from decouple import config
import requests
from ninja.security import APIKeyHeader
from schemas.types import AuthResponse

API_BASE_URL = config('CUSTOMER_API_URL')

class ApiKey(APIKeyHeader):
    param_name = "x-access-token"

    def verify_token(self, auth_token: str):
        result = requests.get(
            f"{API_BASE_URL}/api/auth/verify-token",
            headers={
                "x-access-token": auth_token
            }
        ).json()
        return AuthResponse(**result)

    def authenticate(self, request, key):
        print(f"x-access-token : {key}")
        auth_response = self.verify_token(key)
        print(f"auth response : {auth_response}")
        if auth_response.error is None and auth_response.message == "Token valide":
            return True
