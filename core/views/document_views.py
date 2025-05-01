import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from core.models import Document, Application
from django.utils import timezone

@csrf_exempt
def upload_document(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            application = Application.objects.get(id=data['application_id'])

            doc = Document.objects.create(
                application=application,
                type=data['type'],
                file_url=data['file_url'],
                status='pending',
                uploaded_at=timezone.now()
            )
            return JsonResponse({'id': doc.id, 'type': doc.type, 'status': doc.status})
        except Exception as e:
            return HttpResponseBadRequest(str(e))


@csrf_exempt
def list_documents(request):
    if request.method == 'GET':
        documents = Document.objects.all()
        result = [{
            'id': doc.id,
            'application_id': doc.application.id,
            'type': doc.type,
            'file_url': doc.file_url,
            'status': doc.status,
            'uploaded_at': doc.uploaded_at.isoformat()
        } for doc in documents]
        return JsonResponse(result, safe=False)

@csrf_exempt
def documents_for_application(request, application_id):
    if request.method == 'GET':
        try:
            application = Application.objects.get(id=application_id)
            documents = Document.objects.filter(application=application)
            result = [{
                'id': doc.id,
                'type': doc.type,
                'file_url': doc.file_url,
                'status': doc.status,
                'uploaded_at': doc.uploaded_at.isoformat()
            } for doc in documents]
            return JsonResponse(result, safe=False)
        except Exception as e:
            return HttpResponseBadRequest(str(e))

@csrf_exempt
def update_document_status(request, document_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            status = data.get('status')  # status can be 'pending', 'approved', or 'rejected'

            document = Document.objects.get(id=document_id)
            document.status = status
            document.save()

            return JsonResponse({'id': document.id, 'status': document.status})
        except Exception as e:
            return HttpResponseBadRequest(str(e))

# In core/views/document_views.py
@csrf_exempt
def delete_document(request, document_id):
    if request.method == 'DELETE':
        try:
            document = Document.objects.get(id=document_id)
            document.delete()
            return JsonResponse({'message': 'Document deleted successfully.'})
        except Exception as e:
            return HttpResponseBadRequest(str(e))
