from rest_framework import serializers
from .models import Company, Department

class CompanySerializer(serializers.ModelSerializer):
    department_count = serializers.ReadOnlyField()
    employee_count = serializers.ReadOnlyField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'department_count', 'employee_count']

class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.ReadOnlyField()

    class Meta:
        model = Department
        fields = ['id', 'company', 'name', 'employee_count']