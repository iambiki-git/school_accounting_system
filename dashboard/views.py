from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from dashboard.models import *
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.db import transaction
from datetime import datetime
import json


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Username and password are required!')
            return render(request, 'dashboard/login.html')
        
        if not username:
            messages.error(request, 'Username is required!')
            return render(request, 'dashboard/login.html')

        if not password:
            messages.error(request, 'Password is required!')
            return render(request, 'dashboard/login.html')
        
        # Check if user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Username not found!')
            return render(request, 'dashboard/login.html')

        # Authenticate password
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Password does not match!')
            return render(request, 'dashboard/login.html')

            
    return render(request, 'dashboard/login.html')


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')



def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def students(request):
    return render(request, 'dashboard/students.html')



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .models import Student, Parent, Address
from datetime import datetime
import json

@csrf_exempt
def add_student(request):
    if request.method == 'POST':
        try:
            # Parse JSON data if content-type is application/json
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST.dict()
            
            # Validate required fields
            required_fields = [
                'first_name', 'last_name', 'class_level', 'roll_number',
                'father_name', 'father_phone', 'mother_name',
                'dob', 'gender', 'admission_date',
                'street', 'city', 'state', 'postal_code'
            ]
            
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                return JsonResponse({
                    'success': False,
                    'message': f'Missing required fields: {", ".join(missing_fields)}',
                    'missing_fields': missing_fields
                }, status=400)

            # Parse dates
            dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
            admission_date = datetime.strptime(data['admission_date'], '%Y-%m-%d').date()

            # Create student
            student = Student.objects.create(
                # Personal Information
                first_name=data['first_name'],
                middle_name=data.get('middle_name', ''),
                last_name=data['last_name'],
                dob=dob,
                gender=data['gender'],
                religion=data.get('religion', ''),
                blood_group=data.get('blood_group', ''),
                
                # Academic Information
                class_level=data['class_level'],
                roll_number=data['roll_number'],
                section=data.get('section', 'A'),
                admission_date=admission_date,
                status='ACTIVE',
                
                # Contact Information
                email=data.get('email', ''),
                phone=data.get('phone', ''),
                
                # Medical Information
                medical_conditions=data.get('medical_conditions', ''),
                allergies=data.get('allergies', '')
            )

            # Create permanent address
            Address.objects.create(
                student=student,
                address_type='PERMANENT',
                street=data['street'],
                city=data['city'],
                state=data['state'],
                postal_code=data['postal_code'],
                country=data.get('country', 'Nepal'),
                is_current=True
            )

            # Create temporary address if different
            if data.get('temporary_address') and not data.get('same_as_permanent', False):
                Address.objects.create(
                    student=student,
                    address_type='TEMPORARY',
                    street=data.get('temporary_street', ''),
                    city=data.get('temporary_city', ''),
                    state=data.get('temporary_state', ''),
                    postal_code=data.get('temporary_postal_code', ''),
                    country=data.get('temporary_country', 'Nepal'),
                    is_current=True
                )

            # Create parents
            Parent.objects.create(
                student=student,
                relation='FATHER',
                full_name=data['father_name'],
                occupation=data.get('father_occupation', ''),
                phone=data['father_phone'],
                email=data.get('father_email', ''),
                is_primary=True
            )

            Parent.objects.create(
                student=student,
                relation='MOTHER',
                full_name=data['mother_name'],
                occupation=data.get('mother_occupation', ''),
                phone=data.get('mother_phone', ''),
                email=data.get('mother_email', ''),
                is_primary=False
            )

            # Create guardian if specified
            if data.get('guardian_name'):
                Parent.objects.create(
                    student=student,
                    relation=data.get('guardian_relation', 'GUARDIAN'),
                    full_name=data['guardian_name'],
                    phone=data['guardian_phone'],
                    email=data.get('guardian_email', ''),
                    is_primary=False
                )

            # Prepare response data
            response_data = {
                'success': True,
                'message': 'Student added successfully!',
                'student': {
                    'id': student.id,
                    'name': f"{student.first_name} {student.last_name}",
                    'class': student.class_level,
                    'roll_number': student.roll_number
                },
                'parents': list(student.parents.values('relation', 'full_name', 'phone')),
                'addresses': list(student.addresses.values('address_type', 'city', 'state'))
            }

            return JsonResponse(response_data, status=201)

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data'
            }, status=400)

        except ValidationError as e:
            return JsonResponse({
                'success': False,
                'message': 'Validation error',
                'errors': dict(e)
            }, status=400)

        except IntegrityError as e:
            return JsonResponse({
                'success': False,
                'message': 'Database integrity error',
                'detail': 'A student with this roll number already exists in this class.'
            }, status=409)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Server error',
                'detail': str(e)
            }, status=500)

    return JsonResponse({
        'success': False,
        'message': 'Method not allowed',
        'allowed_methods': ['POST']
    }, status=405)