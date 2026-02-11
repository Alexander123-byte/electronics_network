from rest_framework import permissions


class IsActiveEmployee(permissions.BasePermission):
    """
    Разрешение, предоставляющее доступ только активным сотрудникам.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_active and
            (request.user.is_staff or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
