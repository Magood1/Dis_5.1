from django.contrib import admin
from .models import Patient, MedicalInfo, Appointment, Prescription, Billing



admin.site.register(Patient)
admin.site.register(MedicalInfo)
admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(Billing)
