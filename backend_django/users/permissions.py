from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """Full access for Admin role only."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsManagerOrAdmin(permissions.BasePermission):
    """Access for Managers and Admins."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'manager']

class IsEmployeeReadOnly(permissions.BasePermission):
    """
    Employees can view data (GET, HEAD, OPTIONS).
    Admins and Managers can perform any action.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Allow read-only access for anyone authenticated
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Only allow write access for admin and manager
        return request.user.role in ['admin', 'manager']