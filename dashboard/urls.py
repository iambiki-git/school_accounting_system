from django.urls import path
from dashboard.views import * 

urlpatterns = [
    path('', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout_view'),
    path('students/', students, name='students'),
    path('dashboard/', dashboard, name='dashboard'),
    path('students/add/', add_student, name='add_student'),

]
