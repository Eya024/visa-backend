import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from core.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404



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


@csrf_exempt
def current_user(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'id': request.user.id,
            'username': request.user.username,
            'role': request.user.role
        })
    else:
        return JsonResponse({'user': None})


@login_required
@user_passes_test(lambda u: u.is_superuser or u.role == 'admin')
def list_users(request):
    users = User.objects.all().values('id', 'username', 'email', 'role')
    return JsonResponse({'users': list(users)})

@login_required
def get_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    })
@csrf_exempt
@login_required
def update_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            request.user.username = data.get('username', request.user.username)
            request.user.email = data.get('email', request.user.email)
            request.user.save()
            return JsonResponse({'message': 'User updated successfully'})
        except Exception as e:
            return HttpResponseBadRequest(str(e))


@csrf_exempt
@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return JsonResponse({'message': 'Account deleted successfully'})


@csrf_exempt
@login_required
def change_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            old_password = data['old_password']
            new_password = data['new_password']
            if not request.user.check_password(old_password):
                return HttpResponseBadRequest('Old password is incorrect')
            request.user.set_password(new_password)
            request.user.save()
            return JsonResponse({'message': 'Password changed successfully'})
        except Exception as e:
            return HttpResponseBadRequest(str(e))


