from rest_framework import serializers
from .models import Employee
from organizations.models import Department
from django.contrib.auth import get_user_model
import re
User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role') 
        )
        return user
class EmployeeSerializer(serializers.ModelSerializer):
    days_employed = serializers.ReadOnlyField()

    class Meta:
        model = Employee
        fields = [
            'id', 'company', 'department', 'name', 'email', 
            'mobile_number', 'address', 'designation', 
            'hired_on', 'days_employed', 'status'
        ]

    def validate(self, data):

        company = data.get('company')
        department = data.get('department')

        if department and company and department.company != company:
            raise serializers.ValidationError({
                "department": "The selected department does not belong to this company."
            })
        return data

    def validate_mobile_number(self, value):
        """
        Custom validation for mobile numbers.
        """
        egypt_mobile_regex = r"^01[0125][0-9]{8}$"

        if not re.match(egypt_mobile_regex, value):
            raise serializers.ValidationError(
                "Enter a valid Egyptian mobile number (e.g., 01012345678)."
            )
        
        return value
    

class EmployeeStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['status']

    def update(self, instance, validated_data):
        new_status = validated_data.get('status')
        
        if new_status == 'interview_scheduled':
            instance.schedule_interview()
        elif new_status == 'hired':
            instance.hire()
        
        instance.save()
        return instance