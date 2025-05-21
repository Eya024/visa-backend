# In core/urls/appointment_urls.py
from django.urls import path
from core.views.appointment_views import (
    create_appointment,
    list_appointments,
    update_appointment_status,
    appointments_for_student,
    appointments_for_admin, get_status_choices
)

urlpatterns = [
    path('create/', create_appointment),
    path('list/', list_appointments),
    path('update/<int:appointment_id>/', update_appointment_status),
    path('student/<int:student_id>/', appointments_for_student),
    path('admin/<int:admin_id>/', appointments_for_admin),
    path('statuses/', get_status_choices),

]
