from ninja_extra.exceptions import APIException
from ninja_extra import status


class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Bad Request : Veuillez vérifier le corps de votre requête'