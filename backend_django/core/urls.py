
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from organizations.views import CompanyViewSet, DepartmentViewSet
from employees.views import EmployeeViewSet
from django.contrib import admin
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularSwaggerView, 
    SpectacularRedocView
)
router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Interactive Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Optional: Redoc UI (often preferred for technical documentation)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]