from django.test import TestCase
from django.core.exceptions import ValidationError
from django_fsm import TransitionNotAllowed
from employees.models import Employee
from organizations.models import Company, Department

class EmployeeWorkflowTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="BrainWise")
        self.department = Department.objects.create(name="Engineering", company=self.company)
        self.employee = Employee.objects.create(
            name="John Doe",
            email="john@example.com",
            company=self.company,
            department=self.department
        )

    def test_initial_status(self):
        """Verify new employees start with 'Application Received' status."""
        self.assertEqual(self.employee.status, 'application_received') [cite: 56]

    def test_valid_transition_to_interview(self):
        """Verify transition: Application Received -> Interview Scheduled."""
        self.employee.schedule_interview() [cite: 57]
        self.employee.save()
        self.assertEqual(self.employee.status, 'interview_scheduled')

    def test_valid_transition_to_hired(self):
        """Verify transition: Interview Scheduled -> Hired sets the hired_on date."""
        self.employee.status = 'interview_scheduled'
        self.employee.hire() [cite: 60]
        self.employee.save()
        self.assertEqual(self.employee.status, 'hired')
        self.assertIsNotNone(self.employee.hired_on) [cite: 41]

    def test_invalid_transition_fails(self):
        """Verify that skipping the interview stage raises a TransitionNotAllowed error."""
        with self.assertRaises(TransitionNotAllowed):
            self.employee.hire() 