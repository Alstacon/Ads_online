from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):
    message = "Only owners and staff can update/delete this"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author or request.user.role == 'admin'

