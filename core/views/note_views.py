import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from core.models import Note, Application, User
from django.utils import timezone

@csrf_exempt
def create_note(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            application = Application.objects.get(id=data['application_id'])
            admin = User.objects.get(id=data['admin_id'], role='admin')

            note = Note.objects.create(
                application=application,
                admin=admin,
                content=data['content'],
                created_at=timezone.now()
            )
            return JsonResponse({'id': note.id, 'content': note.content})
        except Exception as e:
            return HttpResponseBadRequest(str(e))


@csrf_exempt
def list_notes(request):
    if request.method == 'GET':
        notes = Note.objects.all()
        result = [{
            'id': note.id,
            'application_id': note.application.id,
            'admin': note.admin.username,
            'content': note.content,
            'created_at': note.created_at.isoformat()
        } for note in notes]
        return JsonResponse(result, safe=False)

@csrf_exempt
def notes_for_application(request, application_id):
    if request.method == 'GET':
        try:
            application = Application.objects.get(id=application_id)
            notes = Note.objects.filter(application=application)
            result = [{
                'id': note.id,
                'admin': note.admin.username,
                'content': note.content,
                'created_at': note.created_at.isoformat()
            } for note in notes]
            return JsonResponse(result, safe=False)
        except Exception as e:
            return HttpResponseBadRequest(str(e))

# In core/views/note_views.py
@csrf_exempt
def update_note(request, note_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            note = Note.objects.get(id=note_id)
            note.content = data.get('content', note.content)
            note.save()

            return JsonResponse({'id': note.id, 'content': note.content})
        except Exception as e:
            return HttpResponseBadRequest(str(e))

# In core/views/note_views.py
@csrf_exempt
def delete_note(request, note_id):
    if request.method == 'DELETE':
        try:
            note = Note.objects.get(id=note_id)
            note.delete()
            return JsonResponse({'message': 'Note deleted successfully.'})
        except Exception as e:
            return HttpResponseBadRequest(str(e))
