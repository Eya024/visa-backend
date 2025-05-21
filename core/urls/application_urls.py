from core.views import application_views
from django.urls import path

urlpatterns = [
    path('create/', application_views.create_application),
    path('list/', application_views.list_applications),
    #path('update/<int:app_id>/', application_views.update_application_status),
    path('dashboard/<int:user_id>/', application_views.student_dashboard),
    path('update/<int:app_id>/', application_views.update_application),
    path('user/<int:user_id>/', application_views.get_user_application),
]
