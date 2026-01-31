from rest_framework import viewsets, filters, status, permissions
from rest_framework.permissions import IsAdminUser, BasePermission
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from .models import Employee
from .serializers import EmployeeSerializer
class IsManagerUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'manager')
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['company', 'department', 'status']
    search_fields = ['name', 'email']

    @action(detail=True, methods=['post'])
    def onboard(self, request, pk=None):
        """
        Custom action to transition an employee's status.
        Accessible at: /api/employees/{id}/onboard/
        """
        employee = self.get_object()
        target_status = request.data.get('status')

        try:
            if target_status == 'interview_scheduled':
                employee.schedule_interview()
            elif target_status == 'hired':
                employee.hire()
            
            employee.save()
            return Response({'status': f'Employee moved to {employee.status}'})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get_permissions(self):
        """
        Dynamically assign permissions based on the API action.
        """
        if self.action == 'destroy':
            permission_classes = [IsAdminUser]
        elif self.action in ['create', 'update', 'partial_update', 'onboard']:
            permission_classes = [IsAdminUser | IsManagerUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
            
        return [permission() for permission in permission_classes]