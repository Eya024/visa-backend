from core.models import Notification
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from core.models import PageVisit, User
import json


@csrf_exempt
def create_notification(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.get(id=data['user_id'])

            notification = Notification.objects.create(
                user=user,
                title=data['title'],
                message=data['message'],
                seen=False,
                created_at=timezone.now()
            )
            return JsonResponse({'id': notification.id, 'title': notification.title})
        except Exception as e:
            return HttpResponseBadRequest(str(e))


@csrf_exempt
def list_notifications(request):
    if request.method == 'GET':
        notifications = Notification.objects.all()
        result = [{
            'id': n.id,
            'user': n.user.username,
            'title': n.title,
            'message': n.message,
            'seen': n.seen,
            'created_at': n.created_at.isoformat()
        } for n in notifications]
        return JsonResponse(result, safe=False)


@csrf_exempt
def mark_as_seen(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            notification = Notification.objects.get(id=data['notification_id'])
            notification.seen = True
            notification.save()
            return JsonResponse({'message': 'Notification marked as seen.'})
        except Exception as e:
            return HttpResponseBadRequest(str(e))

# In core/views/notification_views.py
@csrf_exempt
def notifications_for_user(request, user_id):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=user_id)
            notifications = Notification.objects.filter(user=user)
            result = [{
                'id': n.id,
                'title': n.title,
                'message': n.message,
                'seen': n.seen,
                'created_at': n.created_at.isoformat()
            } for n in notifications]
            return JsonResponse(result, safe=False)
        except Exception as e:
            return HttpResponseBadRequest(str(e))

# In core/views/notification_views.py
@csrf_exempt
def update_notification(request, notification_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            notification = Notification.objects.get(id=notification_id)
            notification.title = data.get('title', notification.title)
            notification.message = data.get('message', notification.message)
            notification.save()

            return JsonResponse({'id': notification.id, 'title': notification.title, 'message': notification.message})
        except Exception as e:
            return HttpResponseBadRequest(str(e))

# In core/views/notification_views.py
@csrf_exempt
def delete_notification(request, notification_id):
    if request.method == 'DELETE':
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.delete()
            return JsonResponse({'message': 'Notification deleted successfully.'})
        except Exception as e:
            return HttpResponseBadRequest(str(e))

# In core/views/notification_views.py

@csrf_exempt
def mark_all_as_seen(request, user_id):
    if request.method == 'POST':
        try:
            user = User.objects.get(id=user_id)
            Notification.objects.filter(user=user, seen=False).update(seen=True)
            return JsonResponse({'message': 'All notifications marked as seen.'})
        except Exception as e:
            return HttpResponseBadRequest(str(e))




@csrf_exempt
def record_visit(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.get(id=data['user_id'])
            page_name = data.get('page_name', 'Unknown Page')

            visit = PageVisit.objects.create(user=user, page_name=page_name)
            return JsonResponse({'message': 'Visit recorded', 'visited_at': visit.visited_at.isoformat()})
        except Exception as e:
            return HttpResponseBadRequest(str(e))

@csrf_exempt
def get_last_visit(request, user_id, page_name):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=user_id)
            last_visit = PageVisit.objects.filter(user=user, page_name=page_name).order_by('-visited_at').first()
            if last_visit:
                return JsonResponse({'last_visited_at': last_visit.visited_at.isoformat()})
            else:
                return JsonResponse({'last_visited_at': None})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)