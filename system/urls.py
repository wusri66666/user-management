from django.urls import path
from system.apis import *

urlpatterns = [
    path('register/', UserCreateAPI.as_view()),
    path('pass-login/', UserLoginAPI.as_view()),
    path('auth/', Auth.as_view()),
    path('userreset/', UserResetAPI.as_view()),
    path('change-pass/', UserChangePass.as_view()),

    path('simple-user/', SimpleUserListAPI.as_view()),
    path('user/', UserListAPI.as_view()),
    path('user-all/', UserListAllAPI.as_view()),
    path('user/<int:pk>/', UserDetailAPI.as_view()),
    path('user/activate/<int:pk>/', UserActivateAPI.as_view()),
    path('user/deactivate/<int:pk>/', UserDeactivateAPI.as_view()),
    path('user/bulk-deactivate/', UserBulkDeactivateAPI.as_view()),

    path('role/', RoleAPI.as_view()),
    path('role/<int:pk>/', RoleDetailAPI.as_view()),
    path('role/activate/<int:pk>/', RoleActivateAPI.as_view()),
    path('role/deactivate/<int:pk>/', RoleDeactivateAPI.as_view()),

    path('department/', DepartmentAPI.as_view()),
    path('department/<int:pk>/', DepartmentDetailAPI.as_view()),
    path('department/activate/<int:pk>/', DepartmentActivateAPI.as_view()),
    path('department/deactivate/<int:pk>/', DepartmentDeactivateAPI.as_view()),

    path('menu-permission/', FirstMenuPermissionAPI.as_view()),
    path('role-permission/', RolePermissionAPI.as_view()),
    path('role-permission/<int:pk>/', RolePermissionDetailAPI.as_view()),
]
