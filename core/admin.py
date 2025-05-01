from django.contrib import admin
from .models import User, Application, Document, Notification, Note, Appointment

admin.site.register(User)
admin.site.register(Application)
admin.site.register(Document)
admin.site.register(Notification)
admin.site.register(Note)
admin.site.register(Appointment)
