from django.contrib import admin
from .models import User, Doctor, Appointment,Patient

admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Patient)