from django.db import models
# Create your models here.

# from django.db import models
# from django.core.validators import RegexValidator
# class Student(models.Model):
#     GENDER_CHOICES = [
#         ('M', 'Male'),
#         ('F', 'Female'),
#         ('O', 'Other'),
#     ]

#     BLOOD_GROUP_CHOICES = [
#         ('A+', 'A+'),
#         ('A-', 'A-'),
#         ('B+', 'B+'),
#         ('B-', 'B-'),
#         ('AB+', 'AB+'),
#         ('AB-', 'AB-'),
#         ('O+', 'O+'),
#         ('O-', 'O-'),
#         ('U', 'Unknown'),
#     ]

#     RELIGION_CHOICES = [
#         ('CH', 'Christianity'),
#         ('IS', 'Islam'),
#         ('HI', 'Hinduism'),
#         ('BU', 'Buddhism'),
#         ('OT', 'Other'),
#     ]

#     # Personal Information
#     first_name = models.CharField(max_length=100, blank=True, null=True)
#     middle_name = models.CharField(max_length=100, blank=True, null=True)
#     last_name = models.CharField(max_length=100, blank=True, null=True)
#     date_of_birth = models.DateField(blank=True, null=True)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
#     blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
#     religion = models.CharField(max_length=2, choices=RELIGION_CHOICES, blank=True, null=True)
#     nationality = models.CharField(max_length=100, blank=True, null=True)
#     photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

#     # Contact Information
#     email = models.EmailField(blank=True, null=True)
#     phone_regex = RegexValidator(
#         regex=r'^\+?1?\d{9,15}$',
#         message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
#     )
#     phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)

#     # Academic Information
#     admission_date = models.DateField(blank=True, null=True)
#     current_class = models.CharField(max_length=50, blank=True, null=True)
#     section = models.CharField(max_length=1, blank=True, null=True)
#     roll_number = models.CharField(max_length=20, blank=True, null=True)
#     previous_school = models.TextField(blank=True, null=True)

#     # Address Information
#     current_address = models.TextField(blank=True, null=True)
#     city = models.CharField(max_length=100, blank=True, null=True)
#     state = models.CharField(max_length=100, blank=True, null=True)
#     country = models.CharField(max_length=100, blank=True, null=True)
#     permanent_address = models.TextField(blank=True, null=True)
#     same_as_current_address = models.BooleanField(default=False)

#     # Medical Information
#     medical_conditions = models.TextField(blank=True, null=True)
#     allergies = models.TextField(blank=True, null=True)
#     additional_notes = models.TextField(blank=True, null=True)

#     # System Fields
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name} ({self.current_class})"

# class Parent(models.Model):
#     RELATION_CHOICES = [
#         ('F', 'Father'),
#         ('M', 'Mother'),
#         ('G', 'Guardian'),
#     ]

#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parents')
#     relation = models.CharField(max_length=1, choices=RELATION_CHOICES)
#     full_name = models.CharField(max_length=255)
#     occupation = models.CharField(max_length=100, blank=True, null=True)
#     email = models.EmailField(blank=True, null=True)
#     phone_regex = RegexValidator(
#         regex=r'^\+?1?\d{9,15}$',
#         message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
#     )
#     phone_number = models.CharField(validators=[phone_regex], max_length=17)
#     is_primary = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.get_relation_display()}: {self.full_name}"

# class Guardian(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='guardians')
#     full_name = models.CharField(max_length=255)
#     relationship = models.CharField(max_length=100)
#     occupation = models.CharField(max_length=100, blank=True, null=True)
#     email = models.EmailField(blank=True, null=True)
#     phone_regex = RegexValidator(
#         regex=r'^\+?1?\d{9,15}$',
#         message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
#     )
#     phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"Guardian: {self.full_name} ({self.relationship})"    


from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    class_level = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=20, default='Active', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"