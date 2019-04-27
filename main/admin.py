from django.contrib import admin

from .models import StudentList, Student, Scaffold

class StudentAdmin(admin.ModelAdmin):
  list_display = [
    'year_choices',
    'cohort_choices',
    'class_number',
    'lastname',
    'firstname',
    'preferred'
    ]

class StudentListAdmin(admin.ModelAdmin):
  list_display = ['year_choices', 'cohort_choices']


admin.site.register(Scaffold)
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentList, StudentListAdmin)