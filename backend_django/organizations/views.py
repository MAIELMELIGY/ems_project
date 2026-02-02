from rest_framework import viewsets

from users.permissions import IsEmployeeReadOnly
from .models import Company, Department
from .serializers import CompanySerializer, DepartmentSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsEmployeeReadOnly]
    

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filterset_fields = ['company']
    permission_classes = [IsEmployeeReadOnly]