from django.urls import path, include
from . import views

urlpatterns = [
    # LOG IN & HOMEPAGE
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('login/home_student/', views.homeStudent, name='home_student'),
    path('login/home_teacher/', views.homeTeacher, name='home_teacher'),
    path('login/home_admin/', views.homeAdmin, name='home_admin'),

    # REGISTRATION STUDENT PAGE
    path('registration_student/', views.registrationStudent, name='registration_student'),

    # REGISTRATION TEACHER PAGE
    path('registration_teacher/', views.registrationTeacher, name='registration_teacher'),

    # REGISTRATION ADMIN PAGE
    path('registration_admin/', views.registrationAdmin, name='registration_admin'),

    # MANAGE STUDENT PAGE
    path('registration_admin/manage_student/', views.manageStudent, name='manage_student'),

    # ADD STUDENT PAGE
    path('registration_admin/manage_student/add_student/', views.addStudent, name='add_student'),

    # DELETE STUDENT PAGE
    path('registration_admin/manage_student/delete_student/<str:studID>/', views.delete_student, name='delete_student'),

    # MANAGE TEACHER PAGE
    path('registration_admin/manage_teacher/', views.manageTeacher, name='manage_teacher'),

    # ADD TEACHER PAGE
    path('registration_admin/manage_teacher/add_teacher/', views.addTeacher, name='add_teacher'),

    # DELETE TEACHER PAGE
    path('registration_admin/manage_teacher/delete_teacher/<str:teacherID>/', views.delete_teacher, name='delete_teacher'),

    # MANAGE CLASS PAGE
    path('registration_admin/manage_class/', views.manageClass, name='manage_class'),

    # ADD CLASS PAGE
    path('registration_admin/manage_class/add_class/', views.addClass, name='add_class'),

    # DELETE CLASS PAGE
    path('registration_admin/manage_class/delete_class/<str:classID>/', views.delete_class, name='delete_class'),

    # PROFILE STUDENT PAGE
    path('profile_student/', views.profileStudent, name='profile_student'),

    #UPDATE PROFILE STUDENT PAGE
    path('profile_student/profile_student_update/', views.profileStudent_update, name='profile_student_update'),
    path('profile_student/profile_student_update/save_profile_student_update', views.save_profileStudent_update,name='save_profile_student_update'),

    # PROFILE TEACHER PAGE
    path('profile_teacher/', views.profileTeacher, name='profile_teacher'),

    #UPDATE PROFILE TEACHER PAGE
    path('profile_teacher/profile_teacher_update/', views.profileTeacher_update, name='profile_teacher_update'),
    path('profile_teacher/profile_teacher_update/save_profile_teacher_update', views.save_profileTeacher_update,name='save_profile_teacher_update'),

    # PROFILE ADMIN PAGE
    path('profile_admin/', views.profileAdmin, name='profile_admin'),

    #UPDATE PROFILE TEACHER PAGE
    path('profile_admin/profile_admin_update/', views.profileAdmin_update, name='profile_admin_update'),
    path('profile_admin/profile_admin_update/save_profile_admin_update', views.save_profileAdmin_update,name='save_profile_admin_update'),
]
