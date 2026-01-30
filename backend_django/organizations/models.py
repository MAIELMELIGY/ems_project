# organizations/models.py
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    
    @property
    def department_count(self):
        return self.departments.count()

    @property
    def employee_count(self):
        return self.employees.count()

class Department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=255)

    @property
    def employee_count(self):
        return self.employees.count()