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
from .models import Student

@csrf_exempt
def add_student(request):
    if request.method == 'POST':
        try:
            # Validate required fields
            required_fields = ['first_name', 'last_name', 'class', 'phn_number']
            if not all(request.POST.get(field) for field in required_fields):
                return JsonResponse({
                    'success': False,
                    'message': 'All required fields must be filled'
                }, status=400)

            # Create student
            student = Student.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                class_level=request.POST['class'],
                status='Active'
            )

            return JsonResponse({
                'success': True,
                'message': 'Student added successfully!',
                'student_id': student.id
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=405)