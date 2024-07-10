from django.shortcuts import get_object_or_404, render, redirect
from StudentRegistrationManagementSystem.models import studentClass, Student, Teacher, Admin
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages

# LOGIN PAGE
def login(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        password = request.POST.get("password")
        user_type = request.POST.get("user_type")

        if user_type == "Student":
            try:
                student = Student.objects.get(studID=user_id, studPassword=password)
                request.session['studID'] = student.studID  # Store student ID in session
                request.session['studName'] = student.studName  # Store student name in session
                return redirect('home_student')
            except Student.DoesNotExist:
                messages.error(request, "Invalid Student ID or password.")
        elif user_type == "Teacher":
            try:
                teacher = Teacher.objects.get(teacherID=user_id, teacherPassword=password)
                request.session['teacherID'] = teacher.teacherID  # Store teacher ID in session
                request.session['teacherName'] = teacher.teacherName  # Store teacher name in session
                return redirect('home_teacher')
            except Teacher.DoesNotExist:
                messages.error(request, "Invalid Teacher ID or password.")
        elif user_type == "Admin":
            try:
                admin = Admin.objects.get(adminID=user_id, adminPassword=password)
                request.session['adminID'] = admin.adminID  # Store admin ID in session
                request.session['adminName'] = admin.adminName  # Store admin name in session
                return redirect('home_admin')
            except Admin.DoesNotExist:
                messages.error(request, "Invalid Admin ID or password.")

    return render(request, 'login.html')

# HOME STUDENT
def homeStudent(request):
    return render(request, 'home_student.html')

def registrationStudent(request):
    s_studID = request.session.get('studID')
    
    if not s_studID:
        return render(request, 'error.html', {'message': 'Student ID not found in session'})

    student = get_object_or_404(Student, studID=s_studID)
    class_list = studentClass.objects.all()
    message = ""

    if request.method == "POST":
        c_classID = request.POST.get('c_classID')
        s_studEmail = request.POST.get('s_studEmail')
        s_studNo = request.POST.get('s_studNo')
        s_dateOfBirth = request.POST.get('s_dateOfBirth')
        s_gender = request.POST.get('s_gender')
        s_address = request.POST.get('s_address')
        s_parentsName = request.POST.get('s_parentsName')
        s_parentsNo = request.POST.get('s_parentsNo')
        s_studPassword = request.POST.get('s_studPassword')

        try:
            class_instance = studentClass.objects.get(classID=c_classID)
        except studentClass.DoesNotExist:
            context = {
                'student': student,
                'class_list': class_list,
                'error_message': "Class ID does not exist"
            }
            return render(request, 'registration_student.html', context)

        if class_instance.currentCapacity >= class_instance.maxCapacity:
            context = {
                'student': student,
                'class_list': class_list,
                'error_message': "Class has reached maximum capacity"
            }
            return render(request, 'registration_student.html', context)
        
        # Update student information
        student.classID = class_instance
        student.studEmail = s_studEmail
        student.studNo = s_studNo
        student.dateOfBirth = s_dateOfBirth
        student.gender = s_gender
        student.address = s_address
        student.parentsName = s_parentsName
        student.parentsNo = s_parentsNo
        student.studPassword = s_studPassword
        student.save()

        # Increment the class capacity (Commented out)
        # class_instance.currentCapacity += 1
        # class_instance.save()

        # Debug statements
        print(f"Class {class_instance.classID} updated. Current Capacity: {class_instance.currentCapacity}")

        message = "Data Saved"

    context = {
        'student': student,
        'class_list': class_list,
        'message': message
    }

    return render(request, 'registration_student.html', context)


# PROFILE STUDENT
def profileStudent(request):
    print("Session Data:", request.session.items())  
    studID = request.session.get('studID')  
    if not studID:
        print("Student ID not found in session")
        return HttpResponse("Student not logged in")
    try:
        student = Student.objects.get(studID=studID)
        print("Student found:", student)
        context = {'student': student}        
        return render(request, "profile_student.html", context)
    except Student.DoesNotExist:
        print("Student not found for student ID:", studID)
        return HttpResponse("Student not found")

# PROFILE UPDATE STUDENT
def profileStudent_update(request):
    studID = request.session.get('studID')  
    if not studID:
        print("Student ID not found in session")
        return HttpResponse("Student not logged in")
    try:
        student = Student.objects.get(studID=studID)
        print("Student found:", student)
        context = {'student': student}        
        return render(request, "profile_student_update.html", context)
    except Student.DoesNotExist:
        print("Student not found for student ID:", studID)
        return HttpResponse("Student not found")

# SAVE PROFILE UPDATE STUDENT
def save_profileStudent_update(request):
    if request.method == 'POST':
        studID = request.session.get('studID')
        studEmail = request.POST.get('studEmail')  
        studNo = request.POST.get('studNo')  
        address = request.POST.get('address')
        parentsNo = request.POST.get('parentsNo')
        studPassword = request.POST.get('studPassword')
        
        student = get_object_or_404(Student, studID=studID)
        
        student.studEmail = studEmail
        student.studNo = studNo
        student.address = address
        student.parentsNo = parentsNo
        student.studPassword = studPassword

        student.save()
        
        return redirect('profile_student')
        
    return redirect('profile_student')

#HOME TEACHER
def homeTeacher(request):
    return render(request, 'home_teacher.html')

#REGISTRATION TEACHER (SEARCH)
def registrationTeacher(request):
    students = Student.objects.all()
    
    if request.method == "GET":
        s_students = request.GET.get('s_students')
        if s_students:
            students = students.filter(studID__icontains=s_students)
    
    return render(request, 'registration_teacher.html', {'student': students})

#PROFILE TEACHER
def profileTeacher(request):
    print("Session Data:", request.session.items())  
    teacherID = request.session.get('teacherID')  
    if not teacherID:
        print("Teacher ID not found in session")
        return HttpResponse("Teacher not logged in")
    try:
        teacher = Teacher.objects.get(teacherID=teacherID)
        print("Teacher found:", teacher)
        context = {'teacher': teacher}        
        return render(request, "profile_teacher.html", context)
    except Teacher.DoesNotExist:
        print("Teacher not found for teacher ID:", teacherID)
        return HttpResponse("Teacher not found")

# PROFILE UPDATE TEACHER
def profileTeacher_update(request):
    teacherID = request.session.get('teacherID')  
    if not teacherID:
        return HttpResponse("Teacher not logged in")
    try:
        teacher = Teacher.objects.get(teacherID=teacherID)
        context = {'teacher': teacher}        
        return render(request, "profile_teacher_update.html", context)
    except Teacher.DoesNotExist:
        return HttpResponse("Teacher not found")

# SAVE PROFILE UPDATE TEACHER
def save_profileTeacher_update(request):
    if request.method == 'POST':
        teacherID = request.session.get('teacherID')
        teacherEmail = request.POST.get('teacherEmail')  
        teacherNo = request.POST.get('teacherNo')  
        teacherPassword = request.POST.get('teacherPassword')
        
        teacher = get_object_or_404(Teacher, teacherID=teacherID)
        
        teacher.teacherEmail = teacherEmail
        teacher.teacherNo = teacherNo
        teacher.teacherPassword = teacherPassword

        teacher.save()
        
        return redirect('profile_teacher')
        
    return redirect('profile_teacher')

#HOME ADMIN 
def homeAdmin(request):
    return render(request, 'home_admin.html')

#REGISTRATION ADMIN
def registrationAdmin(request):
    return render(request, 'registration_admin.html')

#MANAGE STUDENT
def manageStudent(request):
    student = Student.objects.all()
    return render(request, 'manage_student.html', {'student': student})

# ADD STUDENT
def addStudent(request):
    message = ''
    c_classID = studentClass.objects.all()  # Fetch all classes to be used in the dropdown
    if request.method == "POST":
        s_studID = request.POST.get('s_studID')
        s_studName = request.POST.get('s_studName')
        c_classID = request.POST.get('classID')  # This should be corrected to fetch selected classID from form
        s_studEmail = request.POST.get('s_studEmail')
        s_studNo = request.POST.get('s_studNo')
        s_dateOfBirth = request.POST.get('s_dateOfBirth')
        s_gender = request.POST.get('s_gender')
        s_address = request.POST.get('s_address')
        s_parentsNo = request.POST.get('s_parentsNo')
        s_parentsName = request.POST.get('s_parentsName')
        s_studPassword = request.POST.get('s_studPassword')

        if s_studID and s_studName and c_classID and s_studEmail and s_studNo and s_dateOfBirth and s_gender and s_address and s_parentsNo and s_parentsName and s_studPassword:
            try:
                student_class = studentClass.objects.get(classID=c_classID)

                if student_class.currentCapacity >= student_class.maxCapacity:
                    message = "Class has reached maximum capacity"
                else:
                    # Increment the class capacity
                    student_class.currentCapacity += 1
                    student_class.save()

                    data = Student(
                        studID=s_studID,
                        studName=s_studName,
                        classID=student_class,
                        studEmail=s_studEmail,
                        studNo=s_studNo,
                        dateOfBirth=s_dateOfBirth,
                        gender=s_gender,
                        address=s_address,
                        parentsNo=s_parentsNo,
                        parentsName=s_parentsName,
                        studPassword=s_studPassword
                    )
                    data.save()
                    message = "Student added successfully"
            except Exception as e:
                message = f"An error occurred: {e}"
        else:
            message = 'Please provide all required fields'

    context = {'message': message, 'c_classID': c_classID}
    return render(request, 'add_student.html', context)

# DELETE STUDENT
def delete_student(request, studID):
    if request.method == "POST":
        try:
            student = get_object_or_404(Student, studID=studID)
            current_class = student.classID

            if current_class:
                # Decrease class capacity
                current_class.currentCapacity -= 1
                current_class.save()

            # Delete the student from the database
            student.delete()
            messages.success(request, 'Student has been deleted successfully.')
        except Student.DoesNotExist:
            messages.error(request, 'Student does not exist.')

    # Redirect back to the manage_student page after deletion
    return redirect('manage_student')

#MANAGE TEACHER
def manageTeacher(request):
    teacher = Teacher.objects.all()
    return render(request, 'manage_teacher.html', {'teacher': teacher})

#ADD TEACHER
def addTeacher(request):
    message = ''
    if request.method == "POST":
        t_teacherID = request.POST.get('t_teacherID')
        t_teacherName = request.POST.get('t_teacherName')
        t_teacherEmail = request.POST.get('t_teacherEmail')
        t_teacherNo = request.POST.get('t_teacherNo')
        t_teacherPassword = request.POST.get('t_teacherPassword')

        if t_teacherID and t_teacherName and t_teacherEmail and t_teacherNo and t_teacherPassword:
            try:
                data = Teacher(
                    teacherID=t_teacherID,
                    teacherName=t_teacherName,
                    teacherEmail=t_teacherEmail,
                    teacherNo=t_teacherNo,
                    teacherPassword=t_teacherPassword
                )
                data.save()
                message = "Teacher added successfully"
            except Exception as e:
                message = f"An error occurred: {e}"
        else:
            message = 'Please provide all required fields'

    return render(request, 'add_teacher.html', {'message': message})  

#DELETE TEACHER
def delete_teacher(request, teacherID):
    if request.method == "POST":
        try:
            teacher = get_object_or_404(Teacher, teacherID=teacherID)
            teacher.delete()
            messages.success(request, 'Teacher has been deleted successfully.')
        except Teacher.DoesNotExist:
            messages.error(request, 'Teacher does not exist.')
        return redirect('manage_teacher')

#MANAGE CLASS
def manageClass(request):
    classes = studentClass.objects.all()
    return render(request, 'manage_class.html', {'classes': classes})

#ADD CLASS
def addClass(request):
    message = ''
    if request.method == "POST":
        c_classID = request.POST.get('c_classID')
        c_className = request.POST.get('c_className')
        c_maxCapacity = request.POST.get('c_maxCapacity')
        c_currentCapacity = request.POST.get('c_currentCapacity')

        if c_classID and c_className and c_maxCapacity and c_currentCapacity :
            try:
                # Create a new student instance and save it to the database
                data = studentClass(
                    classID=c_classID,
                    className=c_className,
                    maxCapacity=c_maxCapacity,
                    currentCapacity=c_currentCapacity,
                )
                data.save()
                message = "Class added successfully"
            except Exception as e:
                message = f"An error occurred: {e}"
        else:
            message = 'Please provide all required fields'

    return render(request, 'add_class.html', {'message': message})

#DELETE CLASS
def delete_class(request, classID):
    if request.method == "POST":
        try:
            classes = get_object_or_404(studentClass, classID=classID)
            classes.delete()
            messages.success(request, 'Class has been deleted successfully.')
        except studentClass.DoesNotExist:
            messages.error(request, 'Class does not exist.')

    return redirect('manage_class')

#PROFILE ADMIN
def profileAdmin(request):
    print("Session Data:", request.session.items())  
    adminID = request.session.get('adminID')  
    if not adminID:
        print("Admin ID not found in session")
        return HttpResponse("Admin not logged in")
    try:
        admin = Admin.objects.get(adminID=adminID)
        print("Admin found:", admin)
        context = {'admin': admin}        
        return render(request, "profile_admin.html", context)
    except Admin.DoesNotExist:
        print("Admin not found for admin ID:", teacherID)
        return HttpResponse("Admin not found")

# PROFILE UPDATE TEACHER
def profileAdmin_update(request):
    adminID = request.session.get('adminID')  
    if not adminID:
        return HttpResponse("Admin not logged in")
    try:
        admin = Admin.objects.get(adminID=adminID)
        context = {'admin': admin}        
        return render(request, "profile_admin_update.html", context)
    except Admin.DoesNotExist:
        return HttpResponse("Admin not found")

# SAVE PROFILE UPDATE TEACHER
def save_profileAdmin_update(request):
    if request.method == 'POST':
        adminID = request.session.get('adminID')
        adminEmail = request.POST.get('adminEmail')  
        adminNo = request.POST.get('adminNo')  
        adminPassword = request.POST.get('adminPassword')
        
        admin = get_object_or_404(Admin, adminID=adminID)
        
        admin.adminEmail = adminEmail
        admin.adminNo = adminNo
        admin.adminPassword = adminPassword

        admin.save()
        
        return redirect('profile_admin')
        
    return redirect('profile_admin')


