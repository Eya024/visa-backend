import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from core.models import User


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                role=data.get('role', 'student')
            )
            return JsonResponse({'message': 'User registered successfully.', 'id': user.id})
        except Exception as e:
            return HttpResponseBadRequest(str(e))


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = authenticate(request, username=data['username'], password=data['password'])

            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Logged in successfully', 'id': user.id, 'role': user.role})
            else:
                return HttpResponseBadRequest('Invalid credentials')
        except Exception as e:
            return HttpResponseBadRequest(str(e))


@csrf_exempt
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'})


def current_user(request):
    if request.user.is_authenticated:
        return JsonResponse({'username': request.user.username, 'role': request.user.role})
    else:
        return JsonResponse({'user': None})
