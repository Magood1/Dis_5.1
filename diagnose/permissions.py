from rest_framework import permissions

class IsDoctor(permissions.BasePermission):   
    """
    Custom permission to only allow doctors to edit their own data.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return obj.doctor == request.user
