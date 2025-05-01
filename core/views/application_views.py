import json
from django.http import JsonResponse, HttpResponseBadRequest
from core.models import Application, User, Notification, Appointment
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

@csrf_exempt
def create_application(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.get(id=data['user_id'])
            app = Application.objects.create(user=user, status='draft', created_at=timezone.now(), updated_at=timezone.now())
            return JsonResponse({'id': app.id, 'status': app.status})
        except Exception as e:
            return HttpResponseBadRequest(str(e))

@csrf_exempt
def list_applications(request):
    if request.method == 'GET':
        apps = Application.objects.all()
        result = [{'id': app.id, 'user': app.user.username, 'status': app.status} for app in apps]
        return JsonResponse(result, safe=False)


# In core/views/application_views.py

@csrf_exempt
def update_application_status(request, app_id):
    """
    Admin endpoint to update the status of a specific application.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            status = data.get('status')

            # Fetch the application
            app = Application.objects.get(id=app_id)

            # Update the status and timestamp
            app.status = status
            app.updated_at = timezone.now()
            app.save()

            return JsonResponse({'id': app.id, 'status': app.status})
        except Exception as e:
            return HttpResponseBadRequest(str(e))


def student_dashboard(request, user_id):
    """
    Fetch the dashboard data for a student — application status, notifications, appointments.
    """
    if request.method == 'GET':
        try:
            # Fetch student user
            user = User.objects.get(id=user_id)

            # Fetch student application data
            app = Application.objects.filter(user=user).first()

            # Fetch notifications
            notifications = Notification.objects.filter(user=user).order_by('-created_at')[:5]

            # Fetch upcoming appointments
            appointments = Appointment.objects.filter(student=user).order_by('-date')[:3]

            return JsonResponse({
                'application': {
                    'id': app.id if app else None,
                    'status': app.status if app else None,
                    'last_updated': app.updated_at if app else None,
                },
                'notifications': [
                    {'title': n.title, 'message': n.message, 'seen': n.seen, 'created_at': n.created_at}
                    for n in notifications
                ],
                'appointments': [
                    {'date': a.date, 'status': a.status, 'link': a.meeting_link} for a in appointments
                ]
            })
        except Exception as e:
            return HttpResponseBadRequest(str(e))