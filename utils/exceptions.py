from rest_framework import status
from rest_framework.exceptions import APIException


class LoginError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "用户名或密码错误"


class LoginFail(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "用户被停用,无法登录"


class ErrorException(APIException):
    status_code = 500
    default_detail = "发生错误"


class PhoneException(APIException):
    status_code = 400
    default_detail = "手机号不能重复"


class DeactivateRoleException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '该角色被使用，无法被停用！'


class ActivateDepartmentException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '该部门被停用，无法启用！'


class DeactivateDepartmentException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '该组织下有农场、场景，无法被停用！'


class ActivateUserException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '该用户所属父级组织被停用，无法启用！'


class DirectReturnException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Bad Request.'

    def __init__(self, error_code=None, detail=None, desire_status_code=status_code):
        self.detail = {
            'desire_status_code': desire_status_code,
            'error_code': error_code,
            'detail': detail
        }


class DecodeException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "token错误"
