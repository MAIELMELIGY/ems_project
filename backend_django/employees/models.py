from django.db import models
from django_fsm import FSMField, transition
from datetime import date
from django.core.exceptions import ValidationError
class Employee(models.Model):
    STATUS_CHOICES = (
        ('application_received', 'Application Received'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('hired', 'Hired'),
        ('not_accepted', 'Not Accepted'),
    )

    company = models.ForeignKey('organizations.Company', on_delete=models.CASCADE, related_name='employees')
    department = models.ForeignKey('organizations.Department', on_delete=models.CASCADE, related_name='employees')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=20)
    address = models.TextField()
    designation = models.CharField(max_length=100)
    hired_on = models.DateField(null=True, blank=True)
    status = FSMField(default='application_received', choices=STATUS_CHOICES)

    @property
    def days_employed(self):
        if self.hired_on:
            return (date.today() - self.hired_on).days
        return 0

    @transition(field=status, source='application_received', target='interview_scheduled')
    def schedule_interview(self):
        pass

    @transition(field=status, source='interview_scheduled', target='hired')
    def hire(self):
        self.hired_on = date.today()

    def clean(self):
        if self.department.company != self.company:
            raise ValidationError({"department": "Selected department must belong to the selected company."})
