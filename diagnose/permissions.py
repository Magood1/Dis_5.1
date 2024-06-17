from rest_framework import permissions

class IsDoctor(permissions.BasePermission):   
    """
    Custom permission to only allow doctors to edit their own data.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.doctor == request.user
