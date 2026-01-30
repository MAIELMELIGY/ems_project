
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from organizations.views import CompanyViewSet, DepartmentViewSet
from employees.views import EmployeeViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]