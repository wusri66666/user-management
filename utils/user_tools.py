from django.shortcuts import get_object_or_404

from system.models import User


def get_request_user(request_data):
    pk = request_data['id']
    user = get_object_or_404(User, pk=pk)
    return user
