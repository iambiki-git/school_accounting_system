from django.db import models
from django.core.validators import RegexValidator

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    RELIGION_CHOICES = [
        ('HINDU', 'Hindu'),
        ('BUDDHIST', 'Buddhist'),
        ('MUSLIM', 'Muslim'),
        ('CHRISTIAN', 'Christian'),
        ('OTHER', 'Other'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    # Personal Information
    first_name = models.CharField(max_length=100, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    religion = models.CharField(max_length=10, choices=RELIGION_CHOICES, blank=True, null=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    
    # Academic Information
    class_level = models.CharField(max_length=20, blank=True, null=True)
    roll_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    section = models.CharField(max_length=10, default='A', blank=True, null=True)
    admission_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Active', choices=[
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('ALUMNI', 'Alumni'),
    ])
    
    # Contact Information
    email = models.EmailField(blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+977123456789'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    
    # Medical Information
    medical_conditions = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Class: {self.class_level})"

    class Meta:
        ordering = ['class_level', 'roll_number']
        unique_together = ['class_level', 'roll_number']


class Parent(models.Model):
    RELATION_CHOICES = [
        ('FATHER', 'Father'),
        ('MOTHER', 'Mother'),
        ('GUARDIAN', 'Guardian'),
        ('OTHER', 'Other'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parents')
    relation = models.CharField(max_length=10, choices=RELATION_CHOICES)
    full_name = models.CharField(max_length=200)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+977123456789'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17)
    email = models.EmailField(blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.get_relation_display()}: {self.full_name} ({self.student})"

    class Meta:
        unique_together = ['student', 'relation']


class Address(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('PERMANENT', 'Permanent'),
        ('TEMPORARY', 'Temporary'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='Nepal')
    is_current = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.get_address_type_display()} Address for {self.student}"

    class Meta:
        verbose_name_plural = "Addresses"


class StudentDocument(models.Model):
    DOCUMENT_TYPES = [
        ('BIRTH_CERT', 'Birth Certificate'),
        ('CITIZENSHIP', 'Citizenship Copy'),
        ('PHOTO', 'Photograph'),
        ('TRANSFER', 'Transfer Certificate'),
        ('OTHER', 'Other'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='student_documents/')
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_document_type_display()} for {self.student}"