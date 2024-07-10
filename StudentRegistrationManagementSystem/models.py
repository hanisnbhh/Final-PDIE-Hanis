from django.db import models

# Create your models here.
class studentClass(models.Model):
    classID = models.CharField(max_length=3, primary_key=True)
    className = models.TextField()
    maxCapacity = models.IntegerField()
    currentCapacity = models.IntegerField()

class Student(models.Model):
    studID = models.CharField(max_length=3, primary_key=True)
    studName = models.TextField()
    classID = models.ForeignKey(studentClass, on_delete=models.CASCADE, default="") 
    studEmail = models.EmailField()
    studNo = models.CharField(max_length=12)
    dateOfBirth = models.TextField() 
    gender = models.TextField()
    address = models.TextField()
    parentsName = models.TextField()
    parentsNo = models.CharField(max_length=12) 
    studPassword = models.TextField()

class Teacher(models.Model):
    teacherID = models.CharField(max_length=3, primary_key=True) 
    teacherName = models.TextField() 
    teacherEmail = models.EmailField() 
    teacherNo = models.CharField(max_length=12) 
    teacherPassword = models.TextField()

class Admin(models.Model):
    adminID = models.CharField(max_length=3, primary_key=True)
    adminName = models.TextField()
    adminEmail = models.EmailField()
    adminNo = models.CharField(max_length=12) 
    adminPassword = models.TextField()