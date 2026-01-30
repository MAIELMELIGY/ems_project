# users/permissions.py
from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """Full access for Admin role."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsManagerUser(permissions.BasePermission):
    """Access for Managers."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'manager'

class IsEmployeeUser(permissions.BasePermission):
    """Restricted access for Employees."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'employee'