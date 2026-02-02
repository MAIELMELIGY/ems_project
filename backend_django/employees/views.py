from rest_framework import viewsets, filters, status, permissions
from rest_framework.permissions import IsAdminUser, BasePermission
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
import logging
logger = logging.getLogger(__name__)

from .permissions import IsManagerUser
User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['company', 'department', 'status']
    search_fields = ['name', 'email']
    permission_classes = [IsAdminUser | IsManagerUser]

    @action(detail=True, methods=['post'])
    def onboard(self, request, pk=None):
        """
        Custom action to transition an employee's status.
        Accessible at: /api/employees/{id}/onboard/
        """
        employee = self.get_object()
        target_status = request.data.get('status')
        user = request.user

        try:
            logger.info(f"User {user.username} (Role: {user.role}) attempting transition to {target_status} for employee ID {pk}")

            if target_status == 'interview_scheduled':
                employee.schedule_interview()
            elif target_status == 'hired':
                employee.hire()

            employee.save()
            logger.info(f"Successfully transitioned employee {pk} to {employee.status}")
            return Response({'status': f'Employee moved to {employee.status}'})

        except Exception as e:
            logger.error(f"Failed transition for employee {pk} by user {user.username}: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)