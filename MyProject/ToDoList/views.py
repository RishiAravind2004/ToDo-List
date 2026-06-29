from django.shortcuts import render, redirect
import random

from ToDoList.models import UserTB, TasksTB

# temp data
data = {}
success_msg = ""

# https://github.com/RishiAravind2004/SMTP-Mailer [ FOR SENDING EMAILS ]
import smtplib
from email.message import EmailMessage

# Replace these with your actual email and app-specific password
Sender_Email = "rishikesh1878@gmail.com"
App_password = "wpii qrvd jnlv vnbd"

def Send_Mail(Recipient_Email, Subject, Content):
    msg = EmailMessage()
    msg['From'] = Sender_Email
    msg['To'] = Recipient_Email
    msg['Subject'] = Subject
    msg.set_content(Content)
    server = None
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(Sender_Email, App_password)
        server.send_message(msg)
        print(f"Email sent successfully to {Recipient_Email}!")
    except smtplib.SMTPAuthenticationError:
        print("Failed to authenticate. Check your email and password.")
    except smtplib.SMTPException as e:
        print("SMTP error occurred:", e)
    except Exception as e:
        print("Failed to send email:", e)
    finally:
        server.quit()

def GenVerifyCode(length):
    return random.randint(int('1'*length),int('9'*length))


# Refreshing / Back to Home Page
def RefreshHomePage(request, filtered_tasks = [], filter_pattern = ""):
    session_username = request.COOKIES.get('todolist-username')

    if not session_username:
        return redirect("login-page")

    # getting user obj and their tasks
    user = UserTB.objects.get(Username=session_username)
    user_tasks = TasksTB.objects.filter(user=user).values()

    pending = 0
    completed = 0
    if filter_pattern:
        user_tasks = filtered_tasks
    for task in user_tasks:
        if task['Status']:
            completed+=1
        else:
            pending+=1

# Data Structure for context

        # data = {
        #     'name': '',
        #     'username':',
        #     'tasks' : [
        #         {
        #             'id' : 0,
        #             'username': '',
        #             'title': '',
        #             'description': '',
        #             'status': True,
        #         }
        #     ],
        #     'completed_count':0,
        #     'pending_count': 0,
        #     'search':''
        # }

    data = {
        'name': user.Name,
        'username': user.Username,
        'tasks': user_tasks,
        'completed_count': completed,
        'pending_count': pending,
        'search': filter_pattern if filter_pattern else ""
    }

    return render(
        request,
        'HomePage.html',
        context=data
    )

def HomePage(request):
    username = request.COOKIES.get('todolist-username')
    if not username:
        return redirect("login-page")
    return RefreshHomePage(request)


def LoginPage(request):
    global success_msg

    data = {
        'success': success_msg
    }
    success_msg = ""

    return render(
        request,
        'LoginPage.html',
        context=data
    )

def RegisterPage(request):
    return render(
        request,
        'RegisterPage.html'
    )

def ForgotPasswordPage(request):
    return render(
        request,
        'ForgotPasswordPage.html'
    )

def AddingTaskPage(request, Username):
    return render(
        request,
        'AddingTaskPage.html',
        context={'username': Username}
    )

def UpdatingTaskPage(request, TaskId):
    task = TasksTB.objects.get(id=TaskId)
    data = {
        'id': task.id,
        'Title': task.Title,
        'Description': task.Description,
        'Status': task.Status
    }
    return render(
        request,
        'UpdatingTaskPage.html',
        context=data
    )

def DeletingTaskPage(request, TaskId):

    task = TasksTB.objects.get(id=TaskId)

    task_data = {
        'id': task.id,
        'Title': task.Title,
        'Description': task.Description,
        'Status': task.Status
    }

    return render(
        request,
        'DeletingAKPage.html',
        context=task_data
    )

# Handling Forms Submissions

def HandleRegisterSubmittion(request):
    temp_data = {
        'name': request.POST['name'],
        'email': request.POST['email'],
        'username': request.POST['username'],
    }
    try:
        UserTB.objects.get(Email=request.POST['email'])
        temp_data['error'] = 'Email already associate with another account'
        return render(
            request,
            'RegisterPage.html',
            context=temp_data
        )
    
    except:
        try:
            UserTB.objects.get(Username=request.POST['username'])
            temp_data['error'] = 'This username was already taken'
            return render(
                request,
                'RegisterPage.html',
                context=temp_data
            )
        except:
            if request.POST['password']!=request.POST['confirm password']:
                temp_data['error'] = "Password & Confirm Password doesn't matches"
                return render(
                    request,
                    'RegisterPage.html',
                    context=temp_data
                )
            
            del temp_data
            
            code = GenVerifyCode(length=6)

            data[request.POST['email']] = {
                "code" : code,
                "name" : request.POST['name'],
                "username" : request.POST['username'],
                "password" : request.POST['password'],
            }

            Send_Mail(
                Recipient_Email=request.POST['email'],
                Subject="Get Started with Todo List – Verify Your Account",
                Content=f"""
Hello {request.POST['name']},

Welcome to Todo List!

Your email verification code is:

{code}

Please enter this code in the application to verify your email address.

This code will expire in 10 minutes.

If you did not create an account, please ignore this email.

Best regards,
Todo List Team
"""            )
            
            return render(request, 'VerifyEmailPage.html', context={"email": request.POST['email']})


def HandleRegisterVerification(request):
    global success_msg

    if int(request.POST['code'])!=data[request.POST['email']]['code']:
        return render(
            request,
            'VerifyEmailPage.html',
            context={
                'email': request.POST['email'],           
                'error': "Code doesn't matches"
            }
        )
    
    user = UserTB()
    user.Name = data[request.POST['email']]['name']
    user.Email = request.POST['email']
    user.Username = data[request.POST['email']]['username']
    user.Password = data[request.POST['email']]['password']
    user.save()

    del data[request.POST['email']]
    success_msg = "Created an Account!"

    return redirect("login-page")

def HandleForgotPasswordVerficiation(request):
    try:
        user = UserTB.objects.get(Email=request.POST['email'])
        code = GenVerifyCode(8)

        data[request.POST['email']] = {
            'code':code
        }

        Send_Mail(
            Recipient_Email=request.POST['email'],
            Subject="Password Reset Verification Code - ToDo List",
            Content=f"""
Hello {user.Name},

We received a request to reset the password for your Todo List account.

Please use the verification code below to continue:

Verification Code: {code}

If you did not request a password reset, please ignore this email.

Best regards,
Todo List Team
"""
        )
        return render(
            request,
            'UpdatePasswordPage.html',
            context={'email': request.POST['email']}
        )
    except:
        return render(
            request, 
            'ForgotPasswordPage.html',
            context={
                'email': request.POST['email'],
                'error': "Email doesn't exists"
                }
            )

def HandlePasswordUpdation(request):
    global success_msg

    if int(request.POST['code']) != data[request.POST['email']]['code']:
        return render(
            request,
            'UpdatePasswordPage.html',
            context={
                'email': request.POST['email'],
                'error':"Verify code doesn't matches"
            }
        )
    if request.POST['new password'] != request.POST['confirm password']:
        return render(
            request,
            'UpdatePasswordPage.html',
            context={
                'email': request.POST['email'],
                'code': request.POST['code'],
                'error':"Password & Confirm Password doesn't matches"
            }
        )
    user = UserTB.objects.get(Email=request.POST['email'])
    user.Password = request.POST['new password']
    user.save()
    success_msg = "Password Updated!"
    return redirect("login-page")


def HandleLoginForm(request):
    try:
        user = UserTB.objects.get(Email=request.POST['email'])

        if user.Password != request.POST['password']:
            return render(
                request,
                'LoginPage.html',
                context={
                    'email': request.POST['email'],
                    'error': "Password doesn't matches"
                }
            )
        
        response = redirect("home-page")

        # cookiestodolist-username
        response.set_cookie('todolist-username',user.Username)

        return response
    
    except Exception as err:
        print(err)
        return render(
            request,
            'LoginPage.html',
            context={
                'email': request.POST['email'],
                'error': "Email doesn't exists"
            }
        )
    


# CURD Operations on Tasks
def HandleTaskAddForm(request, Username):

    user = UserTB.objects.get(Username=Username)

    new_task = TasksTB()
    new_task.user = user
    new_task.Title = request.POST['title']
    new_task.Description = request.POST['description']
    new_task.Status = True if(request.POST['status']=="True") else False
    new_task.save()

    return redirect("home-page")

def HandleTaskUpdateForm(request, TaskId):
    task = TasksTB.objects.get(id=TaskId)

    task.Title = request.POST['title']
    task.Description = request.POST['description']
    task.Status = True if(request.POST['status']=="True") else False
    task.save()

    return redirect("home-page")

def HandleTaskStatusMarkAsCompletedForm(request, TaskId):
    task = TasksTB.objects.get(id=TaskId)

    task.Status = True
    task.save()

    return redirect("home-page")

def HandleTaskStatusReDoForm(request, TaskId):
    task = TasksTB.objects.get(id=TaskId)

    task.Status = False
    task.save()

    return redirect("home-page")


def HandleTaskDeleteForm(request, TaskId):
    task = TasksTB.objects.get(id=TaskId)
    task.delete()

    return redirect("home-page")

# Regular expression for filter matchings
import re

def HandleTaskSeachingForm(request):
    regex_pattern = request.POST["search"]

    if not regex_pattern:
        return redirect("home-page")

    pattern = re.compile(re.escape(regex_pattern), re.IGNORECASE)
    filtered_tasks = []

    user_tasks = TasksTB.objects.filter(
        user=UserTB.objects.get(Username=request.COOKIES.get("todolist-username"))
    ).values()

    for task in user_tasks:
        found = False

        for field in ("Title", "Description", "id"):
            value = str(task[field])

            if pattern.search(value):
                found = True

            task[field] = pattern.sub(r"<mark>\g<0></mark>", value)

        if found:
            filtered_tasks.append(task)

    return RefreshHomePage(request, filtered_tasks, regex_pattern)

def HandleTaskSearchClear(request):
    return redirect("home-page")

def HandelBackBtn(request):
    return redirect("home-page")

def HandelLogOutBtn(request):
    # Delete cookie
    response = redirect("login-page")
    response.delete_cookie("todolist-username")
    return response