from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from django.db import models


class Department(MPTTModel):
    department_name = models.CharField(max_length=32, verbose_name="组织名称")
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children",
                            verbose_name="所属组织")
    status = models.BooleanField(default=1, verbose_name="状态")
    create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_active = models.BooleanField(default=True, verbose_name="假删除")  # False表示删除

    class Meta:
        verbose_name = "部门表"
        verbose_name_plural = "部门表"

    def __str__(self):
        return self.department_name


class Role(models.Model):
    role_name = models.CharField(max_length=32, verbose_name="角色名称")
    role_desc = models.CharField(max_length=256, null=True, blank=True, verbose_name="角色描述")
    status = models.BooleanField(default=1, verbose_name="状态")
    create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_active = models.BooleanField(default=True, verbose_name="假删除")  # False表示删除

    class Meta:
        verbose_name = "角色表"
        verbose_name_plural = "角色表"

    def __str__(self):
        return self.role_name


class User(AbstractUser):
    # 自带is_active用来标识假删除
    phone = models.CharField(max_length=11, verbose_name="手机号")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="department_system_user",
                                   null=True, blank=True, verbose_name="所属部门")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="role_system_user", null=True, blank=True,
                             verbose_name="角色")
    status = models.BooleanField(default=1, verbose_name="状态")
    create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.first_name


class FirstMenuPermission(models.Model):
    menu_key = models.CharField(max_length=32, null=True, blank=True, verbose_name="一级菜单key")
    menu_name = models.CharField(max_length=64, null=True, blank=True, verbose_name="一级菜单名")
    create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "firstmenu_permission"
        verbose_name = "一级菜单权限表"
        verbose_name_plural = "一级菜单权限表"


class SecondMenuPermission(models.Model):
    parent = models.ForeignKey(FirstMenuPermission, on_delete=models.PROTECT, related_name="parent_permission",
                               verbose_name="所属一级菜单id")
    menu_key = models.CharField(max_length=32, null=True, blank=True, verbose_name="二级菜单key")
    menu_name = models.CharField(max_length=64, null=True, blank=True, verbose_name="二级菜单名")
    create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "secondmenu_permission"
        verbose_name = "二级菜单权限表"
        verbose_name_plural = "二级菜单权限表"


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="role_menu", verbose_name="所属角色id")
    menu_permission = ArrayField(models.CharField(max_length=512, null=True, blank=True), verbose_name="角色权限列表")
    create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "role_permission"
        verbose_name = "角色权限表"
        verbose_name_plural = "角色权限表"
