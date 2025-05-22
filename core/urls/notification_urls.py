# In core/urls/notification_urls.py
from django.urls import path
from core.views.notification_views import (
    create_notification,
    list_notifications,
    mark_as_seen,
    notifications_for_user,
    update_notification,
    delete_notification, mark_all_as_seen, record_visit, get_last_visit
)

urlpatterns = [
    path('create/', create_notification),
    path('list/', list_notifications),
    path('mark-as-seen/', mark_as_seen),
    path('user/<int:user_id>/', notifications_for_user),
    path('update/<int:notification_id>/', update_notification),
    path('delete/<int:notification_id>/', delete_notification),
    path('mark-all-as-seen/<int:user_id>/', mark_all_as_seen),
    path('record-visit/', record_visit),
    path('last-visit/<int:user_id>/<str:page_name>/', get_last_visit),

]
