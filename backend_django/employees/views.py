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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
logger = logging.getLogger(__name__)

from users.permissions import IsManagerOrAdmin
User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "email": request.user.email,
            "role": request.user.role,
            "username": request.user.username
        })
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['company', 'department', 'status']
    search_fields = ['name', 'email']
    permission_classes = [IsManagerOrAdmin]

    @action(detail=True, methods=['post'])
    def onboard(self, request, pk=None):
        employee = self.get_object()
        target_status = request.data.get('status') 
        
        try:
            if target_status == 'interview_scheduled':
                employee.schedule_interview() 
            elif target_status == 'hired':
                employee.hire() 
            elif target_status == 'not_accepted':
                employee.status = 'not_accepted' 
            else:
                return Response({'error': 'Invalid status requested'}, status=status.HTTP_400_BAD_REQUEST)

            employee.save()
            return Response({'status': f'Employee moved to {employee.status}', 'current_status': employee.status})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def hired_report(self, request):
        """
        Returns a list of all employees with 'hired' status for reporting.
        """
        hired_employees = Employee.objects.filter(status='hired')
        
        serializer = self.get_serializer(hired_employees, many=True)
        return Response(serializer.data)