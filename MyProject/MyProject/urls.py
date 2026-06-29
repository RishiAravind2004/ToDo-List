"""
URL configuration for MyProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from ToDoList import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.HomePage, name="home-page"),
    path('login', views.LoginPage, name="login-page"),
    path('register', views.RegisterPage, name="register-page"),
    path('forgot-password', views.ForgotPasswordPage, name="forgot-pass-page"),

    path('register-form', views.HandleRegisterSubmittion),
    path('register-verify', views.HandleRegisterVerification),

    path('forgot-password-verify', views.HandleForgotPasswordVerficiation),
    path('forgot-password-form', views.HandlePasswordUpdation),

    path('login-form', views.HandleLoginForm),

    path('addtask-<str:Username>', views.AddingTaskPage),
    path('addtaskform-<str:Username>', views.HandleTaskAddForm),

    path('updatetask-<int:TaskId>', views.UpdatingTaskPage),
    path('updatetaskform-<int:TaskId>', views.HandleTaskUpdateForm),

    path('updatetaskstatuscompleted-<int:TaskId>', views.HandleTaskStatusMarkAsCompletedForm),
    path('updatetaskstatusnotcompleted-<int:TaskId>', views.HandleTaskStatusReDoForm),

    path('deletetask-<int:TaskId>', views.DeletingTaskPage),
    path('deletetaskform-<int:TaskId>',views.HandleTaskDeleteForm),

    path('search-task-form', views.HandleTaskSeachingForm),
    path('search-task-clear', views.HandleTaskSearchClear),

    path('logout-btn', views.HandelLogOutBtn),
    path('back-btn', views.HandelBackBtn),
]
