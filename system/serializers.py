from system.models import Role, Department, User, FirstMenuPermission, SecondMenuPermission, RolePermission
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from utils.exceptions import PhoneException
from utils.request_tools import server_requests
from utils.response_tools import jsonify_response_content
from django.conf import settings


# 获取睿畜科技机构id
def get_smartahc_institute():
    response_institute = server_requests(method='GET', url='/user/org/smartahc-institute/', root_path=settings.USER)
    response_institute = jsonify_response_content(response_institute)
    smartahc_institute = response_institute.get("data").get("institute")
    return smartahc_institute


class UserCreateSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=64, required=False)
    password = serializers.CharField(max_length=64, required=False)
    first_name = serializers.CharField(max_length=32, required=False)
    department = serializers.CharField(max_length=64, required=False)
    status = serializers.BooleanField(required=False)
    role = serializers.CharField(max_length=64, required=False)

    def create(self, validated_data):
        obj = User.objects.filter(phone=validated_data.get('phone'))
        if obj:
            raise PhoneException
        user = User.objects.create(
            phone=validated_data.get("phone"),
            username=validated_data.get("phone"),
            first_name=validated_data.get("first_name"),
            department_id=validated_data.get("department"),
            role_id=validated_data.get("role"),
            status=validated_data.get("status"),
            is_active=True)
        password = "1234567"
        if password:
            user.set_password(password)
            user.save()
            token = Token.objects.create(user=user)
            user.token = token.key
        else:
            user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    password = serializers.CharField(max_length=128)


class UserListSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField(read_only=True)
    role = serializers.SerializerMethodField(read_only=True)
    institute = serializers.IntegerField(default=get_smartahc_institute, read_only=True)

    def get_department(self, obj):
        department = obj.department
        return DepartmentSerializer(department).data

    def get_role(self, obj):
        role = obj.role
        return RoleSerializer(role).data

    class Meta:
        model = User
        fields = ["id", "first_name", "phone", "email", "department", "role", "status", "is_active", "create_time",
                  "update_time", "institute"]


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name"]


class RoleSerializer(serializers.ModelSerializer):
    permission = serializers.SerializerMethodField(required=False, read_only=True)

    def get_permission(self, obj):
        res = RolePermission.objects.filter(role_id=obj.id)
        if res:
            return RolePermissionSerializer(res.first()).data
        return None

    class Meta:
        model = Role
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        exclude = ["lft", "rght"]


class FirstMenuPermissionSerializer(serializers.ModelSerializer):
    second_menu = serializers.SerializerMethodField(required=False, read_only=True)

    def get_second_menu(self, obj):
        res = SecondMenuPermission.objects.filter(parent=obj.id)
        return SecondMenuPermissionSerializer(res, many=True).data

    class Meta:
        model = FirstMenuPermission
        fields = "__all__"


class SecondMenuPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondMenuPermission
        fields = "__all__"


class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = "__all__"
