from rest_framework.authentication import BaseAuthentication
from rest_framework_expiring_authtoken.models import ExpiringToken as Token

from utils.encryption import get_decode_user
from utils.exceptions import DirectReturnException


class UserServerAuthentication(BaseAuthentication):
    def authenticate(self, request):
        full_path = request.get_full_path()
        # 从中间服务请求或别的模块请求
        if request.META.get("HTTP_SERVICE") or full_path == "/system/auth/":
            return
        original_token = request.META.get("HTTP_AUTHORIZATION", None)
        original_token = get_decode_user(original_token)
        if original_token:
            original_token = original_token.split()[1]
            obj = Token.objects.filter(key=original_token).first()
            if not obj:
                raise DirectReturnException(detail='用户认证失败', desire_status_code=401)
            if not obj.user.is_active or not obj.user.status:
                print('User inactive or deleted')
                raise DirectReturnException(detail='用户账号被禁用或被删除', desire_status_code=401)
            return (obj.user, obj)
        else:
            raise DirectReturnException(detail='未提供认证信息', desire_status_code=401)
