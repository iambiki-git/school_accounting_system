from django.contrib import admin
from django.utils.html import format_html
from .models import Student, Parent, Address, StudentDocument

class ParentInline(admin.TabularInline):
    model = Parent
    extra = 1
    fields = ('relation', 'full_name', 'occupation', 'phone', 'email', 'is_primary')
    ordering = ('relation',)

class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    fields = ('address_type', 'street', 'city', 'state', 'postal_code', 'country', 'is_current')
    ordering = ('address_type',)

class DocumentInline(admin.TabularInline):
    model = StudentDocument
    extra = 0
    fields = ('document_type', 'file_link', 'description', 'uploaded_at')
    readonly_fields = ('file_link', 'uploaded_at')
    
    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">View Document</a>', obj.file.url)
        return "-"
    file_link.short_description = "Document"

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'class_level', 'section', 'roll_number', 'status', 'gender', 'admission_date')
    list_filter = ('class_level', 'section', 'status', 'gender', 'religion')
    search_fields = ('first_name', 'last_name', 'middle_name', 'roll_number', 'phone', 'email')
    ordering = ('class_level', 'section', 'roll_number')
    list_per_page = 20
    inlines = [ParentInline, AddressInline, DocumentInline]
    fieldsets = (
        ('Personal Information', {
            'fields': (
                ('first_name', 'middle_name', 'last_name'),
                ('dob', 'gender', 'blood_group'),
                'religion',
            )
        }),
        ('Academic Information', {
            'fields': (
                ('class_level', 'section', 'roll_number'),
                'admission_date',
                'status',
            )
        }),
        ('Contact Information', {
            'fields': (
                'email',
                'phone',
            )
        }),
        ('Medical Information', {
            'fields': (
                'medical_conditions',
                'allergies',
            ),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "Name"
    full_name.admin_order_field = 'first_name'

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'relation', 'student_link', 'phone', 'is_primary')
    list_filter = ('relation', 'is_primary')
    search_fields = ('full_name', 'phone', 'email', 'student__first_name', 'student__last_name')
    raw_id_fields = ('student',)
    
    def student_link(self, obj):
        return format_html('<a href="/admin/student/student/{}/change/">{}</a>', obj.student.id, obj.student)
    student_link.short_description = "Student"

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('student_link', 'address_type', 'city', 'state', 'is_current')
    list_filter = ('address_type', 'city', 'state', 'is_current')
    search_fields = ('student__first_name', 'student__last_name', 'street', 'city')
    raw_id_fields = ('student',)
    
    def student_link(self, obj):
        return format_html('<a href="/admin/student/student/{}/change/">{}</a>', obj.student.id, obj.student)
    student_link.short_description = "Student"

@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display = ('student_link', 'document_type', 'uploaded_at', 'file_link')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('student__first_name', 'student__last_name', 'description')
    readonly_fields = ('uploaded_at',)
    date_hierarchy = 'uploaded_at'
    
    def student_link(self, obj):
        return format_html('<a href="/admin/student/student/{}/change/">{}</a>', obj.student.id, obj.student)
    student_link.short_description = "Student"
    
    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">View</a>', obj.file.url)
        return "-"
    file_link.short_description = "Document"