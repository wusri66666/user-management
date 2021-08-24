from django.contrib.auth.hashers import check_password
from rest_framework import generics
from rest_framework_expiring_authtoken.models import ExpiringToken as Token
from rest_framework.views import APIView
from utils.encryption import get_encode_user
from utils.pagination_tools import StandardPagination
from utils.user_tools import get_request_user
from system.models import Role, Department, User, FirstMenuPermission, RolePermission
from system.serializers import RoleSerializer, DepartmentSerializer, UserCreateSerializer, UserLoginSerializer, \
    UserListSerializer, SimpleUserSerializer, FirstMenuPermissionSerializer, RolePermissionSerializer
from utils.exceptions import *
from utils.search_tools import search_decorator
from rest_framework.views import Response
from django.utils.translation import ugettext_lazy as _


class HealthCheckAPI(APIView):
    """
    GET -> 健康检查
    """
    authentication_classes = []

    def get(self, request):
        return Response({"code": 0, "msg": "success"})


class UserCreateAPI(generics.CreateAPIView):
    """
    POST -> 创建用户
    """
    authentication_classes = []
    serializer_class = UserCreateSerializer


class UserLoginAPI(APIView):
    """
    POST -> 用户登录
    """
    serializer_class = UserLoginSerializer
    authentication_classes = []

    def post(self, request, format=None):
        phone = request.data.get('phone')
        password = request.data.get('password')
        users = User.objects.filter(phone=phone)
        user = users.first()
        if user and check_password(password, user.password):
            data = UserListSerializer(user).data
            token, _ = Token.objects.get_or_create(
                user=user
            )
            if token.expired():
                token.delete()
                token = Token.objects.create(user=user)
            user.token = token.key
            if user and user.status:
                key = 'system_token ' + token.key
                data["token"] = get_encode_user(key)
                # 用户模块睿畜科技顶级组织id
                return Response({"code": 0, "msg": "登录成功", "data": {"user": data}})
            else:
                raise LoginFail
        raise LoginError


class UserResetAPI(APIView):
    """
    GET -> 重置密码
    """

    def get(self, request, format=None):
        id = self.request.query_params.get("id")
        user = User.objects.filter(id=id).first()
        password = "1234567"
        try:
            user.set_password(password)
            user.save()
            token, _ = Token.objects.get_or_create(
                user=user
            )
            if token:
                token.delete()
                token = Token.objects.create(user=user)

            user.token = token.key
            return Response({"code": 0, "msg": "重置密码成功", "data": {}})
        except Exception as e:
            raise ErrorException


class UserChangePass(APIView):
    """
    POST -> 修改密码
    """

    def post(self, request):
        user = get_request_user(request.data)
        password = request.data.get('password')
        user.set_password(password)
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            token.delete()
            token = Token.objects.create(user=user)
        user.token = token.key
        return Response(
            {"code": 0, "msg": "修改密码成功", "data": {"user": UserListSerializer(user).data, "token": user.token}})


class UserListAPI(generics.ListAPIView):
    """
    GET -> 获取用户列表-未删除用户
    """
    queryset = User.objects.filter(is_active=1)
    serializer_class = UserListSerializer
    pagination_class = StandardPagination

    @search_decorator
    def get_queryset(self):
        department_id = self.request.query_params.get("department")
        # print(self.request.user.id,'==============user_id==============')
        # 查询组织及其子组织下用户
        if department_id:
            departments = Department.objects.filter(id=department_id).get_descendants(include_self=True)
            self.queryset = self.queryset.filter(department_id__in=departments, status=True)
        return self.queryset.order_by("-create_time")


class UserListAllAPI(generics.ListAPIView):
    """
    GET -> 获取所有用户列表-包含删除用户
    """
    queryset = User.objects.all()
    serializer_class = SimpleUserSerializer

    @search_decorator
    def get_queryset(self):
        return self.queryset.all()


class SimpleUserListAPI(generics.ListAPIView):
    """
    GET -> 获取简易用户列表
    """
    queryset = User.objects.filter(is_active=1).order_by("-create_time")
    serializer_class = SimpleUserSerializer

    @search_decorator
    def get_queryset(self):
        return self.queryset.all()


class UserDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    GET -> 获取用户详细信息
    PATCH -> 编辑用户信息
    """
    serializer_class = UserListSerializer
    queryset = User.objects.all()

    def perform_update(self, serializer):
        id = self.request.data.get("id")
        department_id = self.request.data.get("department")
        role_id = self.request.data.get("role")
        phone = self.request.data.get("phone")
        user = User.objects.exclude(id=id).filter(phone=phone)
        if user:
            raise PhoneException
        department = Department.objects.filter(id=department_id).first()
        role = Role.objects.filter(id=role_id).first()
        res = serializer.save(department=department, role=role)
        return UserListSerializer(res).data

    def delete(self, request, *args, **kwargs):
        User.objects.filter(id=kwargs.get("pk")).update(is_active=False)
        return Response({"code": 0, "msg": "删除成功", "data": ""})


class UserActivateAPI(generics.UpdateAPIView):
    """
    启用用户
    """
    serializer_class = UserListSerializer
    queryset = User.objects.all()

    def perform_update(self, serializer):
        user_id = self.kwargs.get("pk")
        user = User.objects.get(id=user_id)
        if user:
            department_id = user.department.id
            departments = Department.objects.filter(id=department_id).get_ancestors(include_self=True).filter(
                status=False)
            if departments:
                raise ActivateUserException
            serializer.save(status=True)


class UserDeactivateAPI(generics.UpdateAPIView):
    """
    禁用用户
    """
    serializer_class = UserListSerializer
    queryset = User.objects.all()

    def perform_update(self, serializer):
        user_id = self.kwargs.get("pk")
        department_id = self.request.data.get("department")
        if department_id:
            department_id_list = Department.objects.filter(id=department_id).get_descendants(
                include_self=True).values_list(
                "id")
            department_id_list = [i[0] for i in department_id_list]
            User.objects.filter(department_id__in=department_id_list).update(status=False)
            Department.objects.filter(id__in=department_id_list).update(status=False)
        else:
            User.objects.filter(id=user_id).update(status=False)
        return Response({"code": 0, "msg": "禁用用户成功", "data": {}})


class UserBulkDeactivateAPI(APIView):
    """
    批量禁用机构下的用户
    """
    serializer_class = UserListSerializer
    queryset = User.objects.all()

    def get(self, request):
        department_id = self.request.query_params.get("department")
        department_id_list = Department.objects.filter(id=department_id).get_descendants(include_self=True).values_list(
            "id")
        department_id_list = [i[0] for i in department_id_list]
        User.objects.filter(department__in=department_id_list).update(status=False)
        Department.objects.filter(id__in=department_id_list).update(status=False)
        return Response({"code": 0, "msg": "批量禁用用户成功", "data": {}})


class RoleAPI(generics.ListCreateAPIView):
    """
    GET -> 获取角色列表
    POST -> 创建角色
    """
    serializer_class = RoleSerializer
    queryset = Role.objects.filter(is_active=True).order_by("-create_time")
    pagination_class = StandardPagination

    @search_decorator
    def get_queryset(self):
        return self.queryset.all()


class RoleDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    PATCH -> 编辑角色信息
    DELETE -> 删除被停用的角色
    """
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

    def delete(self, request, *args, **kwargs):
        role_id = kwargs.get("pk")
        objs = Role.objects.filter(id=role_id)
        User.objects.filter(role__in=objs).update(is_active=False)
        return Response({"code": 0, "msg": "删除成功", "data": ""})


class RoleActivateAPI(generics.UpdateAPIView):
    """
    启用角色
    """
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

    def perform_update(self, serializer):
        serializer.save(status=True)


class RoleDeactivateAPI(generics.UpdateAPIView):
    """
    禁用角色
    """
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

    def perform_update(self, serializer):
        # objs = Role.objects.filter(id=self.kwargs.get("pk"))
        # users = User.objects.filter(role__in=objs)
        # if users:
        #     raise RoleException
        # else:
        #     serializer.save(status=False)
        # 与用户进行关联
        role_id = self.kwargs.get("pk")
        role = Role.objects.get(id=role_id)
        users = User.objects.filter(role=role, status=True, is_active=True)
        if users:
            raise DeactivateRoleException
        serializer.save(status=0)


class DepartmentAPI(generics.ListCreateAPIView):
    """
    GET -> 获取组织列表
    POST -> 创建组织列表
    """
    serializer_class = DepartmentSerializer
    queryset = Department.objects.filter(is_active=True).order_by("-create_time")

    @search_decorator
    def get_queryset(self):
        return self.queryset.all()


class DepartmentDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    PATCH -> 编辑组织信息
    DELETE -> 删除被停用的组织
    """
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    def delete(self, request, *args, **kwargs):
        objs = Department.objects.filter(id=kwargs.get("pk")).get_descendants(include_self=True)
        objs.update(is_active=False)
        User.objects.filter(department__in=objs).update(is_active=False)
        return Response({"code": 0, "msg": "删除成功", "data": ""})


class DepartmentActivateAPI(generics.UpdateAPIView):
    """
    启用组织
    """
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    def perform_update(self, serializer):
        department_id = self.kwargs.get("pk")
        departments = self.queryset.filter(id=department_id).get_ancestors(include_self=False).filter(
            status=False)
        if departments:
            raise ActivateDepartmentException
        serializer.save(status=True)


class DepartmentDeactivateAPI(generics.UpdateAPIView):
    """
    禁用部门
    """
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    def update(self, request, *args, **kwargs):
        department_id = self.kwargs.get("pk")
        department_id_list = Department.objects.filter(id=department_id).get_descendants(include_self=True).values_list(
            "id")
        department_id_list = [i[0] for i in department_id_list]
        users = User.objects.filter(department_id__in=department_id_list, is_active=True, status=True)
        if users:
            return Response({})
        Department.objects.filter(id__in=department_id_list).update(status=False)
        return Response({"code": 0, "msg": "禁用部门及其下用户成功", "data": {}})


class Auth(APIView):
    keyword = 'system_token'
    model = Token

    def authenticate_credentials(self, key):
        """Attempt token authentication using the provided key."""
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            print('Invalid token')
            raise DirectReturnException(error_code=5, detail='token无效', desire_status_code=401)
            # raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active or not token.user.status:
            print('User inactive or deleted')
            raise DirectReturnException(error_code=6, detail='用户账号被禁用或被删除', desire_status_code=401)
            # raise exceptions.AuthenticationFailed('User inactive or deleted')

        if token.expired():
            print('Token has expired')
            raise DirectReturnException(error_code=7, detail='token已过期', desire_status_code=401)
            # raise exceptions.AuthenticationFailed('Token has expired')
        user = UserListSerializer(token.user, context={'request': self.request}).data
        return (user, None)

    def post(self, request):
        request_data = request.data
        user_auth = request_data['original_token']
        auth = user_auth.split()
        if not auth or auth[0].lower() != self.keyword.lower():
            msg = _('请检查请求头是否正确提供')
            raise DirectReturnException(error_code=1, detail=msg, desire_status_code=401)

        if len(auth) == 1:
            msg = _('请提供token')
            raise DirectReturnException(error_code=2, detail=msg, desire_status_code=401)

        elif len(auth) > 2:
            msg = _('token字符串中不允许包含空格字符')
            raise DirectReturnException(error_code=3, detail=msg, desire_status_code=401)

        try:
            token = auth[1]
        except UnicodeError:
            msg = _('token字符串中不允许包含非法字符')
            raise DirectReturnException(error_code=4, detail=msg, desire_status_code=401)
        authenticate_token = self.authenticate_credentials(token)
        result = {"authenticate_token": authenticate_token}
        return Response({"data": result})


class FirstMenuPermissionAPI(generics.ListCreateAPIView):
    """
    GET -> 获取菜单权限列表
    """
    queryset = FirstMenuPermission.objects.all()
    serializer_class = FirstMenuPermissionSerializer

    @search_decorator
    def get_queryset(self):
        return self.queryset.all()


class RolePermissionAPI(generics.ListCreateAPIView):
    """
    GET -> 获取角色的菜单权限列表
    POST -> 创建角色的菜单权限列表
    """
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer

    @search_decorator
    def get_queryset(self):
        return self.queryset.all()


class RolePermissionDetailAPI(generics.RetrieveUpdateAPIView):
    """
    GET -> 获取具体角色的菜单权限列表
    PUT/PATCH -> 修改具体角色的菜单权限列表
    """
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer

