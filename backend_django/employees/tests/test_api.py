from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from employees.models import Employee
from organizations.models import Company, Department

User = get_user_model()

class EmployeeAPITest(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(name="BrainWise")
        self.department = Department.objects.create(name="HR", company=self.company)
        self.employee = Employee.objects.create(
            name="Jane Smith",
            company=self.company,
            department=self.department,
            status='application_received'
        )
        
        # Create users with different roles
        self.admin = User.objects.create_superuser(username='admin', password='password123', email='admin@test.com')
        self.manager = User.objects.create_user(username='manager', password='password123', role='manager')
        self.staff = User.objects.create_user(username='staff', password='password123', role='employee')

    def test_onboard_action_manager_access(self):
        """Verify a Manager can trigger the onboard transition."""
        self.client.force_authenticate(user=self.manager) [cite: 65]
        url = f'/api/employees/{self.employee.id}/onboard/'
        response = self.client.post(url, {'status': 'interview_scheduled'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_onboard_action_unauthorized_access(self):
        """Verify a standard Employee cannot trigger the onboard transition."""
        self.client.force_authenticate(user=self.staff) [cite: 64]
        url = f'/api/employees/{self.employee.id}/onboard/'
        response = self.client.post(url, {'status': 'interview_scheduled'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_business_logic_cross_company_validation(self):
        """Verify API prevents selecting a department from a different company."""
        other_company = Company.objects.create(name="Other Corp")
        other_dept = Department.objects.create(name="Sales", company=other_company)
        
        self.client.force_authenticate(user=self.admin)
        data = {
            "name": "Validation Test",
            "company": self.company.id,
            "department": other_dept.id # Mismatch
        }
        response = self.client.post('/api/employees/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("The selected department does not belong to this company.", str(response.data)) [cite: 51]