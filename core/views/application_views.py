import json
from django.http import JsonResponse, HttpResponseBadRequest
from core.models import Application, User, Notification, Appointment
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from datetime import datetime


@csrf_exempt
def create_application(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(id=request.POST['user_id'])

            dob_raw = request.POST.get('date_of_birth')
            date_of_birth = datetime.strptime(dob_raw, '%Y-%m-%d').date() if dob_raw else None

            app = Application.objects.create(
                user=user,
                full_name=request.POST.get('full_name'),
                email=request.POST.get('email'),
                phone_number=request.POST.get('phone_number'),
                date_of_birth=date_of_birth,
                passport_number=request.POST.get('passport_number'),
                nationality=request.POST.get('nationality'),
                destination_country=request.POST.get('destination_country'),
                visa_type=request.POST.get('visa_type'),
                purpose_of_travel=request.POST.get('purpose_of_travel'),
                duration_of_stay=request.POST.get('duration_of_stay'),
                occupation=request.POST.get('occupation'),
                education_level=request.POST.get('education_level'),
                marital_status=request.POST.get('marital_status'),
                supporting_documents=request.POST.get('supporting_documents'),
                additional_notes_file=request.FILES.get('additional_notes_file'),
                status='draft',
                created_at=timezone.now(),
                updated_at=timezone.now()
            )

            # Create notification for application created
            Notification.objects.create(
                user=user,
                title="Application Created",
                message=f"Your application has been successfully created.",
                seen=False,
                created_at=timezone.now()
            )

            return JsonResponse({'id': app.id, 'status': app.status})
        except Exception as e:
            return HttpResponseBadRequest(str(e))


@csrf_exempt
def list_applications(request):
    if request.method == 'GET':
        apps = Application.objects.all()
        result = []
        for app in apps:
            result.append({
                'id': app.id,
                'user_id': app.user.id,
                'user': app.user.username,
                'full_name': app.full_name,
                'email': app.email,
                'phone_number': app.phone_number,
                'date_of_birth': app.date_of_birth,
                'passport_number': app.passport_number,
                'nationality': app.nationality,
                'destination_country': app.destination_country,
                'visa_type': app.visa_type,
                'purpose_of_travel': app.purpose_of_travel,
                'duration_of_stay': app.duration_of_stay,
                'occupation': app.occupation,
                'education_level': app.education_level,
                'marital_status': app.marital_status,
                'supporting_documents': app.supporting_documents,
                'additional_notes_file': app.additional_notes_file.url if app.additional_notes_file else None,
                'status': app.status,
                'created_at': app.created_at,
                'updated_at': app.updated_at,
            })
        return JsonResponse(result, safe=False)


@csrf_exempt
def update_application_status(request, app_id):
    """
    Admin endpoint to update the status of a specific application.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            status = data.get('status')

            app = Application.objects.get(id=app_id)
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
            user = User.objects.get(id=user_id)
            app = Application.objects.filter(user=user).first()
            notifications = Notification.objects.filter(user=user).order_by('-created_at')[:5]
            appointments = Appointment.objects.filter(student=user).order_by('-date')[:3]

            return JsonResponse({
                'application': {
                    'id': app.id if app else None,
                    'status': app.status if app else None,
                    'last_updated': app.updated_at if app else None,
                    'destination_country': app.destination_country if app else None,
                    'visa_type': app.visa_type if app else None,
                    'full_name': app.full_name if app else None
                },
                'notifications': [
                    {'title': n.title, 'message': n.message, 'seen': n.seen, 'created_at': n.created_at}
                    for n in notifications
                ],
                'appointments': [
                    {'date': a.date, 'status': a.status, 'link': a.meeting_link}
                    for a in appointments
                ]
            })
        except Exception as e:
            return HttpResponseBadRequest(str(e))


@csrf_exempt
def get_user_application(request, user_id):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=user_id)
            app = Application.objects.filter(user=user).first()
            if not app:
                return JsonResponse({'exists': False})

            return JsonResponse({
                'exists': True,
                'data': {
                    'id': app.id,
                    'user_id': user.id,
                    'full_name': app.full_name,
                    'email': app.email,
                    'phone_number': app.phone_number,
                    'date_of_birth': app.date_of_birth,
                    'passport_number': app.passport_number,
                    'nationality': app.nationality,
                    'destination_country': app.destination_country,
                    'visa_type': app.visa_type,
                    'purpose_of_travel': app.purpose_of_travel,
                    'duration_of_stay': app.duration_of_stay,
                    'occupation': app.occupation,
                    'education_level': app.education_level,
                    'marital_status': app.marital_status,
                    'supporting_documents': app.supporting_documents,
                }
            })
        except Exception as e:
            return HttpResponseBadRequest(str(e))


@csrf_exempt
def update_application(request, app_id):
    if request.method == 'POST':
        try:
            app = Application.objects.get(id=app_id)
            data = request.POST

            app.full_name = data.get('full_name')
            app.email = data.get('email')
            app.phone_number = data.get('phone_number')
            app.date_of_birth = datetime.strptime(data.get('date_of_birth'), '%Y-%m-%d').date()
            app.passport_number = data.get('passport_number')
            app.nationality = data.get('nationality')
            app.destination_country = data.get('destination_country')
            app.visa_type = data.get('visa_type')
            app.purpose_of_travel = data.get('purpose_of_travel')
            app.duration_of_stay = data.get('duration_of_stay')
            app.occupation = data.get('occupation')
            app.education_level = data.get('education_level')
            app.marital_status = data.get('marital_status')
            app.supporting_documents = data.get('supporting_documents')
            if 'additional_notes_file' in request.FILES:
                app.additional_notes_file = request.FILES['additional_notes_file']
            app.updated_at = timezone.now()
            app.save()

            # Create notification for application updated
            Notification.objects.create(
                user=app.user,
                title="Application Updated",
                message=f"Your application has been successfully updated.",
                seen=False,
                created_at=timezone.now()
            )

            return JsonResponse({'message': 'Application updated successfully'})
        except Exception as e:
            return HttpResponseBadRequest(str(e))


