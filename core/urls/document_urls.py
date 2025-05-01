# In core/urls/document_urls.py
from django.urls import path
from core.views.document_views import (
    upload_document,
    list_documents,
    documents_for_application,
    update_document_status,
    delete_document
)

urlpatterns = [
    path('upload/', upload_document),
    path('list/', list_documents),
    path('application/<int:application_id>/', documents_for_application),
    path('update/<int:document_id>/', update_document_status),
    path('delete/<int:document_id>/', delete_document),
]
