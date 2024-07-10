from django.contrib import admin
from .models import studentClass, Student, Teacher, Admin

# Register your models here.

#STUDENT CLASS
admin.site.register(studentClass)

#STUDENT
admin.site.register(Student)

#TEACHER
admin.site.register(Teacher)

#ADMIN
admin.site.register(Admin)
