# In core/urls/note_urls.py
from django.urls import path
from core.views.note_views import (
    create_note,
    list_notes,
    notes_for_application,
    update_note,
    delete_note
)

urlpatterns = [
    path('create/', create_note),
    path('list/', list_notes),
    path('application/<int:application_id>/', notes_for_application),
    path('update/<int:note_id>/', update_note),
    path('delete/<int:note_id>/', delete_note),
]
