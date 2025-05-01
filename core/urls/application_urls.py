# In core/urls/application_urls.py
from django.urls import path
from core.views.application_views import create_application, list_applications, update_application_status, student_dashboard

urlpatterns = [
    path('create/', create_application),
    path('list/', list_applications),
    path('update/<int:app_id>/', update_application_status),
    path('dashboard/<int:user_id>/', student_dashboard),
]
