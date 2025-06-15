from django.contrib import admin
from .models import *

# Register your models here.

# class ParentInline(admin.TabularInline):
#     model = Parent
#     extra = 1

# class GuardianInline(admin.TabularInline):
#     model = Guardian
#     extra = 1

# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'current_class', 'admission_date')
#     search_fields = ('first_name', 'last_name', 'current_class')
#     list_filter = ('current_class', 'gender')
#     inlines = [ParentInline, GuardianInline]
#     fieldsets = (
#         ('Personal Info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'gender')}),
#         ('Academic Info', {'fields': ('current_class', 'section', 'admission_date')}),
#     )

# @admin.register(Parent)
# class ParentAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'relation', 'student')
#     search_fields = ('full_name', 'student__first_name')

# @admin.register(Guardian)
# class GuardianAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'relationship', 'student')
#     search_fields = ('full_name', 'student__first_name')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'class_level', 'status', 'created_at')
