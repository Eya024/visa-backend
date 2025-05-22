from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import PageVisit
from django.contrib.auth.models import User

@csrf_exempt
def record_page_visit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        page = data.get('page')
        visited_at = data.get('visited_at')
        user = User.objects.get(id=user_id)
        PageVisit.objects.create(user=user, page=page, visited_at=visited_at)
        return JsonResponse({'message': 'Visit recorded'})
