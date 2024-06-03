from ninja_extra.exceptions import APIException
from ninja_extra import status


class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad Request : Veuillez vérifier le corps de votre requête'


class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not Found : La ressource demandée n\'a pas été retrouvée'
