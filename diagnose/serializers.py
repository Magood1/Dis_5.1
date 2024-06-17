from rest_framework import serializers
from .models import Patient, MedicalInfo, Appointment, Prescription, Billing

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'


class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = '__all__'


class MedicalInfoSerializer(serializers.ModelSerializer):
    second_attribute = serializers.IntegerField(read_only=True)

    class Meta:
        model = MedicalInfo
        fields = '__all__'

