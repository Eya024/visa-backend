from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def send_contact_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        country = data.get('country')
        message = data.get('message')

        full_message = f"""
        New Contact Message from Elegant Visa Website:

        Name: {name}
        Email: {email}
        Phone: {phone}
        Country: {country}
        Message: {message}
        """

        try:
            send_mail(
                subject="New Contact Form Submission",
                message=full_message,
                from_email=email,
                recipient_list=['yourcompanyemail@gmail.com'],
                fail_silently=False,
            )
            return JsonResponse({'success': True, 'message': 'Email sent successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
