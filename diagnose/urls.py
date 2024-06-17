from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'quick_diagnose', views.QuickDiagnose, basename='quick_diagnose')
#http://192.168.50.85:8000/diagnose/quick_diagnose/


router.register(r'medicalInfo', views.MedicalInfoViewSet, basename='medicalInfo')
#http://192.168.50.85:8000/diagnose/medicalInfo/


#not allowed becase we doon't know what is medical information id for this doctor 
#http://192.168.50.85:8000/diagnose/medicalInfo/1/


router.register(r'patients',  views.PatientViewSet)
#http://192.168.50.85:8000/diagnose/patients/


#not allowed becase we doon't know what is medical information id for this doctor
#http://192.168.50.85:8000/diagnose/patients/1/


router.register(r'patient_by_name/(?P<patient_name>[a-zA-Z]+)', views.find_patient)
#http://192.168.50.85:8000/diagnose/patient/R/


router.register(r'prescription', views.PrescriptionViewSet) 
#http://192.168.50.85:8000/diagnose/prescription/


router.register(r'prescription/patient/(?P<patient_id>\d+)', views.find_prescription)
#http://192.168.50.85:8000/diagnose/prescription/patient/1/


router.register(r'appointment', views.AppointmentViewSet)
#http://192.168.50.85:8000/diagnose/appointment/


router.register(r'appointment/specific_date/(?P<appointment_date>\d{4}-\d{2}-\d{2})', views.SpecificAppointment)
#http://192.168.50.85:8000/diagnose/appointment/specific_date/2024-03-07/


router.register(r'appointment/specific_patient/(?P<patient_id>\d+)', views.SpecificPatientAppointment)
#http://192.168.50.85:8000/diagnose/appointment/specific_patient/1/


router.register(r'appointment/in_range/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})', views.RangeAppointment)
#http://192.168.50.85:8000/diagnose/appointment/in_range/2024-03-07/2024-03-15/


router.register(r'billing', views.BillingViewSet)
router.register(r'patient_billing/(?P<patient_id>\d+)', views.find_billing)


urlpatterns = [
    path('', include(router.urls)),

    path('', include('rest_framework.urls')),
]








