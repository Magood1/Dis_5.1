from django.db import models
from accounts.models import UserData as Doctor


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    brithday = models.DateField()  # Date of birth
    gender = models.BooleanField(default=True)  # Male, Female
    address = models.TextField()  # Address of the patient
    phone = models.CharField(max_length=20)  # Phone number
    insurance_info = models.TextField()  # Insurance information
    personal_photo = models.ImageField(upload_to='photo/personal/%y/%m/%d', null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, editable=False)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class MedicalInfo(models.Model):
    """
    Stores medical information related to patients.
    """
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='medical_info', null=True)

    # Medical attributes
    chest_photo = models.ImageField(upload_to='photo/chest/%y/%m/%d', default='None')    
    classification = models.CharField(max_length=50, editable=False, default='None')
    pneumonia = models.BooleanField(default=True, editable=False)  
    
    died = models.BooleanField(default=False)
    death_date = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField()
    
    
    patient_type_values = [
        (1, 'Returned Home'),
        (2, 'Hospitalization')
    ]
    patient_type = models.PositiveSmallIntegerField(default=2, choices=patient_type_values)
    

    usmr_values = [
        (1,'First Level'),
        (2,'Second Level'),
        (3,'Third Level'),
    ]
    usmr = models.PositiveSmallIntegerField(default=1, choices=usmr_values)
    medical_unit = models.CharField(max_length=100, default='National Health System')
    
    
    gender_values = [
        (1, 'Male'),
        (2, 'Female'),
    ]
    gender = models.PositiveSmallIntegerField(choices=gender_values)
    
    pregnancy = models.BooleanField(default=False) 
    diabetes = models.BooleanField(default=False)
    copd = models.BooleanField(default=False) 
    
    asthma = models.BooleanField(default=False) 
    inmsupr = models.BooleanField(default=False)
    hypertension = models.BooleanField(default=False)
    
    cardiovascular =  models.BooleanField(default=False)
    renal_chronic = models.BooleanField(default=False) 
    obesity =  models.BooleanField(default=False)
    
    tobacco =  models.BooleanField(default=False)
    intubed = models.BooleanField(default=False)
    icu = models.BooleanField(default=False) 


    def __str__(self):
        return f"Medical Info for {self.patient.first_name} {self.patient.last_name}"
    
    def clean(self):
       """
       Custom validation method to check if the date of death is valid.
       """
       if self.death_date:
           if self.death_date >= timezone.now().date():
               raise ValidationError(_("Date of death cannot be in the future."))


class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=50)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, editable=False)


    def __str__(self):
        return f"Prescription for {self.patient.first_name}: {self.medication_name}"


class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, editable=False)
    appointment_date = models.DateTimeField()

    def __str__(self):
        return f"Appointment for {self.patient.first_name} with Dr. {self.doctor.last_name}"


class Billing(models.Model):
    billing_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, editable=False)
    billing_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Billing for {self.patient.first_name} {self.patient.last_name}"
