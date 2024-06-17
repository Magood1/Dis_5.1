from django.shortcuts import render
from django.http import HttpResponse
from .models import Patient, MedicalInfo, Appointment, Prescription, Billing
from .serializers import PatientSerializer, MedicalInfoSerializer, AppointmentSerializer, PrescriptionSerializer, BillingSerializer
from rest_framework import status, filters, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from django.shortcuts import get_object_or_404
from .predict import predict
import cv2
import numpy as np
from rest_framework.decorators import api_view, permission_classes
from django.http.response import JsonResponse 
from django.utils import timezone
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from .permissions import IsDoctor


class QuickDiagnose(viewsets.ModelViewSet):
    """
    API view for performing quick medical diagnosis based on chest X-ray images.

    - Accepts a chest X-ray image file (chest_photo) as input.
    - Decodes the image content and predicts the classification (e.g., 'Pneumonia').
    - Updates the validated data with the classification and pneumonia status.
    - Returns the serialized medical information.

    URL: doctors/<int:doctor_id>/quick_diagnose'
    The doctor_id for the permission because only doctors are allowed to make a diagnosis

    Args:
        In the this version:
        chest_photo (file): The chest X-ray image file.
        But in the future: we will use all medical information. 

    Returns:
        Response: Serialized medical information with classification and pneumonia status.
                  Returns HTTP 200 OK if successful, or HTTP 400 BAD REQUEST if there are errors.
    """
    queryset = MedicalInfo.objects.all()
    serializer_class = MedicalInfoSerializer
    permission_classes = [IsAuthenticated, IsDoctor]
 
    def perform_create(self, serializer):

        image_file = self.request.data.get("chest_photo")
        
        """
          Custom validation method to check if the date of death is valid.

        date_str = self.request.data.get("death_date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if  date >= timezone.now().date():
            raise Http404("Date of death cannot be in the future.")
        """

        if image_file:
            
            file_content = image_file.read()  # Get the file content

            nparr = np.fromstring(file_content, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            classification = predict(img_np)
            print(classification)
            # Update validated data with classification and pneumonia status
            serializer.validated_data['classification'] = classification
            if 'Pneumonia' in classification:
                serializer.validated_data['pneumonia'] = True
            else:
                serializer.validated_data['pneumonia'] = False
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MedicalInfoViewSet(viewsets.ModelViewSet):
    queryset = MedicalInfo.objects.all()
    serializer_class = MedicalInfoSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return self.queryset.filter(patient__doctor=self.request.user)

    def perform_create(self, serializer):
        image_file = self.request.data.get("chest_photo")
        if image_file:
            file_content = image_file.read()  # Get the file content

            nparr = np.fromstring(file_content, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            classification = predict(img_np)
            serializer.validated_data['classification'] = classification
            if 'Pneumonia' in classification:
                serializer.validated_data['pneumonia'] = True
            else:
                serializer.validated_data['pneumonia'] = False
            serializer.save()


    def perform_update(self, serializer):
        image_file = self.request.data.get("chest_photo")
        if image_file:
            file_content = image_file.read()  # Get the file content

            nparr = np.fromstring(file_content, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            classification = predict(img_np)

            serializer.validated_data['classification'] = classification
            if 'Pneumonia' in classification:
                serializer.validated_data['pneumonia'] = True
            else:
                serializer.validated_data['pneumonia'] = False
            serializer.save()



class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return self.queryset.filter(doctor=self.request.user)

    def perform_create(self, serializer):
        serializer.validated_data['doctor'] = self.request.user
        serializer.save()

    def perform_update(self, serializer):
        serializer.validated_data['doctor'] = self.request.user
        serializer.save()
    


    

class find_patient(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsDoctor]


    def get_queryset(self):
        """
        Retrieves a list of patients based on the provided doctor ID and patient name.

        Args:
            doctor_id (int): The ID of the doctor associated with the patients.
            patient_name (str): The search string for patient names (first, last, or both).

        Returns:
            QuerySet: A filtered queryset containing patients whose names include the specified letters.
                      If no patients match the search criteria, raises Http404.         
        
        Example : http://127.0.0.1:8000/diagnose/doctor/1/patient/hndi/ 
            this example should return Magd Hndi patient information who is associated with doctor id 1
        """
        doctor_id = self.request.user
        patient_name = self.kwargs['patient_name']

        # Get the IDs of patients associated with the given doctor
        patients_ids = Appointment.objects.filter(doctor=doctor_id).values_list('patient', flat=True)

        # Filter patients by first name or last name containing the search string
        patients = Patient.objects.filter(patient_id__in=patients_ids)
        filtered_patients = patients.filter(first_name__icontains=patient_name) | patients.filter(last_name__icontains=patient_name)
        
        # Check if any patients match the search criteria
        if filtered_patients.exists():
            return filtered_patients
        else:
            raise Http404("Patient not found")

#Done
class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return self.queryset.filter(patient__doctor=self.request.user)
    
    def perform_create(self, serializer):
        serializer.validated_data['doctor'] = self.request.user
        serializer.save()

    def perform_update(self, serializer):
        serializer.validated_data['doctor'] = self.request.user
        serializer.save()
    


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return self.queryset.filter(doctor=self.request.user)

    def perform_create(self, serializer):
        serializer.validated_data['doctor'] = self.request.user
        serializer.save()

    def perform_update(self, serializer):
        serializer.validated_data['doctor'] = self.request.user
        serializer.save()
  

class find_prescription(viewsets.ModelViewSet):
    
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        """
        Retrieves prescriptions associated with a specific patient, including dosage information,
        based on the patient's ID and the doctor's ID.

        Args:
            doctor_id (int): The ID of the doctor who issued the prescriptions.
            patient_id (int): The ID of the patient for whom the prescriptions are retrieved.

        Returns:
            QuerySet: A filtered queryset containing prescriptions for the specified patient.
                      Raises Http404 if the patient does not exist.
        """
        patient_id = self.kwargs['patient_id']
        
        # Ensure the doctor is only querying their own patient's prescriptions
        return self.queryset.filter(doctor=self.request.user, patient_id=patient_id)


class SpecificAppointment(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsDoctor]
    
    def get_queryset(self):
        appointment_date = self.kwargs['appointment_date']  # Extract start date from URL
      #  print("Hi Maggooooooooood")
        patients = Appointment.objects.filter(doctor=self.request.user, appointment_date__contains=appointment_date)
        return patients


class RangeAppointment(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        start_date = self.kwargs['start_date']  # Extract start date from URL
        end_date = self.kwargs['end_date']  # Extract end date from URL

        # Ensure the doctor is only querying their own appointments
        return self.queryset.filter(
            doctor=self.request.user,
            appointment_date__range=(start_date, end_date)
        )

class SpecificPatientAppointment(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        try:
            
            # Ensure the doctor is only querying their own patient's appointments
            return self.queryset.filter(doctor=self.request.user, patient_id=patient_id)

        except Appointment.DoesNotExist:
            raise Http404("Patient not found")

class BillingViewSet(viewsets.ModelViewSet):
    
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return self.queryset.filter(doctor=self.request.user)
    
    def perform_create(self, serializer):
        serializer.validated_data['doctor'] = self.request.user
        serializer.save()

    def perform_update(self, serializer):
        serializer.validated_data['doctor'] = self.request.user
        serializer.save()
 


class find_billing(viewsets.ModelViewSet):
    
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return self.queryset.filter(doctor=self.request.user, patient_id=patient_id)
