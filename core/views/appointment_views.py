import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from core.models import Appointment, User
from django.utils import timezone

@csrf_exempt
def create_appointment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student = User.objects.get(id=data['student_id'])
            admin = User.objects.get(id=data['admin_id'])

            appointment = Appointment.objects.create(
                student=student,
                admin=admin,
                date=data['date'],
                meeting_link=data['meeting_link'],
                status='scheduled'
            )
            return JsonResponse({'id': appointment.id, 'status': appointment.status})
        except Exception as e:
            return HttpResponseBadRequest(str(e))


@csrf_exempt
def list_appointments(request):
    if request.method == 'GET':
        appointments = Appointment.objects.all()
        result = [{
            'id': app.id,
            'student': app.student.username,
            'admin': app.admin.username,
            'date': app.date.isoformat(),
            'meeting_link': app.meeting_link,
            'status': app.status
        } for app in appointments]
        return JsonResponse(result, safe=False)

# In core/views/appointment_views.py
@csrf_exempt
def update_appointment_status(request, appointment_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            status = data.get('status')  # status can be 'scheduled', 'completed', or 'cancelled'

            # Fetch appointment
            appointment = Appointment.objects.get(id=appointment_id)

            # Update status
            appointment.status = status
            appointment.save()

            return JsonResponse({'id': appointment.id, 'status': appointment.status})
        except Exception as e:
            return HttpResponseBadRequest(str(e))

# In core/views/appointment_views.py
@csrf_exempt
def appointments_for_student(request, student_id):
    if request.method == 'GET':
        try:
            student = User.objects.get(id=student_id)
            appointments = Appointment.objects.filter(student=student)
            result = [{
                'id': app.id,
                'admin': app.admin.username,
                'date': app.date.isoformat(),
                'meeting_link': app.meeting_link,
                'status': app.status
            } for app in appointments]
            return JsonResponse(result, safe=False)
        except Exception as e:
            return HttpResponseBadRequest(str(e))

# In core/views/appointment_views.py
@csrf_exempt
def appointments_for_admin(request, admin_id):
    if request.method == 'GET':
        try:
            admin = User.objects.get(id=admin_id)
            appointments = Appointment.objects.filter(admin=admin)
            result = [{
                'id': app.id,
                'student': app.student.username,
                'date': app.date.isoformat(),
                'meeting_link': app.meeting_link,
                'status': app.status
            } for app in appointments]
            return JsonResponse(result, safe=False)
        except Exception as e:
            return HttpResponseBadRequest(str(e))
