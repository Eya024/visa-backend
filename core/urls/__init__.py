from django.urls import path, include

urlpatterns = [
    path('auth/', include('core.urls.auth_urls')),
    path('applications/', include('core.urls.application_urls')),
    path('documents/', include('core.urls.document_urls')),
    path('notifications/', include('core.urls.notification_urls')),
    path('appointments/', include('core.urls.appointment_urls')),
    path('notes/', include('core.urls.note_urls')),
]
