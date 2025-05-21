import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from core.models import Appointment, User, Availability
from django.utils import timezone

@csrf_exempt
def create_appointment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student = User.objects.get(id=data['student_id'])

            appointment = Appointment.objects.create(
                student=student,
                reason=data['reason'],
                status='scheduled'
            )

            # Create availability entries
            for slot in data['availabilities']:
                Availability.objects.create(
                    appointment=appointment,
                    day=slot['day'],
                    time=slot['time']
                )

            return JsonResponse({'id': appointment.id, 'status': appointment.status})
        except Exception as e:
            return HttpResponseBadRequest(str(e))



from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
import json

@csrf_exempt
def list_appointments(request):
    if request.method == 'GET':
        appointments = Appointment.objects.all()
        result = []
        for app in appointments:
            availabilities = list(app.availabilities.values('day', 'time'))  # get availabilities as list of dicts
            result.append({
                'id': app.id,
                'student': app.student.username if app.student else None,
                'admin': app.admin.username if app.admin else None,
                'reason': app.reason,
                'status': app.status,
                'created_at': app.created_at.isoformat(),
                'availabilities': availabilities,
            })
        return JsonResponse(result, safe=False)



# In core/views/appointment_views.py
@csrf_exempt
def update_appointment_status(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return HttpResponseBadRequest("Appointment not found")

    if request.method == 'POST':
        data = json.loads(request.body)
        status = data.get('status')
        if status not in dict(Appointment._meta.get_field('status').choices):
            return HttpResponseBadRequest("Invalid status value.")
        appointment.status = status
        appointment.save()
        return JsonResponse({'id': appointment.id, 'status': appointment.status})

    elif request.method == 'PUT':
        data = json.loads(request.body)
        reason = data.get('reason')
        availabilities = data.get('availabilities')

        if reason:
            appointment.reason = reason
            appointment.save()

        if availabilities is not None:
            # Clear old availabilities
            appointment.availabilities.all().delete()
            # Add new ones
            for slot in availabilities:
                Availability.objects.create(
                    appointment=appointment,
                    day=slot['day'],
                    time=slot['time']
                )

        return JsonResponse({'id': appointment.id, 'reason': appointment.reason, 'availabilities': availabilities})

    elif request.method == 'DELETE':
        appointment.delete()
        return JsonResponse({'message': 'Appointment deleted'})

    else:
        return HttpResponseBadRequest("Unsupported HTTP method")


# In core/views/appointment_views.py
@csrf_exempt
def appointments_for_student(request, student_id):
    if request.method == 'GET':
        try:
            student = User.objects.get(id=student_id)
            appointments = Appointment.objects.filter(student=student)
            result = []
            for app in appointments:
                availabilities = list(app.availabilities.values('day', 'time'))
                result.append({
                    'id': app.id,
                    'admin': app.admin.username if app.admin else None,
                    'reason': app.reason,
                    'status': app.status,
                    'created_at': app.created_at.isoformat(),
                    'availabilities': availabilities,
                })
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
            result = []
            for app in appointments:
                availabilities = list(app.availabilities.values('day', 'time'))
                result.append({
                    'id': app.id,
                    'student': app.student.username if app.student else None,
                    'reason': app.reason,
                    'status': app.status,
                    'created_at': app.created_at.isoformat(),
                    'availabilities': availabilities,
                })
            return JsonResponse(result, safe=False)
        except Exception as e:
            return HttpResponseBadRequest(str(e))



def get_status_choices(request):
    choices = [status[0] for status in Appointment._meta.get_field('status').choices]
    return JsonResponse({'status_choices': choices})