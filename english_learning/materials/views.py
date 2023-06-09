from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Course, UserProfile, Material, Commens
from django.core.exceptions import ObjectDoesNotExist
from .templatetags.password import *
from django.contrib.auth.hashers import make_password
from django.views.defaults import page_not_found
from django.http import HttpRequest
from django.http import HttpResponse
import english_learning.settings as settings



def photo_view(request, content):
    ''' this fanction for connection with telegram which return file from path'''
    p = HttpRequest.get_full_path(request)
    index = p.rindex('?') + 1
    res = p[index:]
    photo_path = f"{settings.MEDIA_ROOT}/{res}"
    with open(photo_path, 'rb') as f:
        response = HttpResponse(f.read())
    return response


def home(request):
    cours_pk = 0
    usr = request.user
    # If user authenticated and user not superuser take cours_pk argument
    if usr.is_authenticated and not usr.is_superuser:
        if UserProfile.objects.filter(user=usr).exists():
            user = UserProfile.objects.get(user=usr)
            if user.courses is not None:
                cours_pk = user.courses.pk
            else:
                return render(request, 'not_approved.html',{'user':user})
    # Take all comments from db!
    comments =Commens.objects.all()
    if request.method == 'POST':                                                                                                            
        # If request method POST and 'comment' not empty string.
        if request.POST['coment'] != '':
            comment = request.POST['coment']
            # If user authenticated create new comment with user information
            if usr.is_authenticated:
                commentos = Commens.objects.create(comment=comment,user=usr)
                commentos.save()
            # Else user not authenticated create new comment without user information
            else:
                commentos = Commens.objects.create(comment=comment, )
                commentos.save()
    # Render the home template if the request method is GET    
    return render(request, 'home.html', {'comments': comments, 'cours_pk': cours_pk})

def not_approved(request):
    user = request.user
    return render(request, 'not_approved.html',{'user':user})

def course(request, course_id):
    user = request.user
    if course_id != 0:
        course = get_object_or_404(Course, id=course_id)
        if user.is_superuser:
            topic = course.topic.pk
            mat = course.materials.filter()
            materials = Material.objects.filter(topic_id=topic)
            lessons = course.lesson1.all()
            context = {
                'course': course,'lessons': lessons,
                'user': user, 'mat': mat, 'materials': materials, 
            }
            return render(request, 'course_detail.html', context)
        url = get_object_or_404(UserProfile,user=user)
        if user.is_authenticated and url.courses.pk == course_id and url.is_approved or user.is_superuser:
            topic = course.topic.pk
            mat = course.materials.filter()
            materials = Material.objects.filter(topic_id=topic)
            lessons = course.lesson1.all()
            context = {
                'course': course,'lessons': lessons,
                'user': user, 'mat': mat, 'materials': materials, 
            }
            return render(request, 'course_detail.html', context)
        else:
            return redirect(not_approved)
    return redirect(home)


def registr(request):
    if request.method == 'POST':
        # Get form data from POST request
        name = request.POST.get('name')
        last_name = request.POST.get('surname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        # Create a new User object and save it to the database
        if not  User.objects.filter(username=email).exists():
            user = User.objects.create_user(username=email, email=email, password=password, first_name=name, last_name=last_name)
            user.save()
            # Create a new MaterialsUser object and save it to the database
            user1  = UserProfile.objects.create(user=user, phone=phone)
            user1.save()
        # Redirect to a success page or homepage
        return redirect(login_view)

    # Render the registration form template if the request method is GET
    return render(request, 'registr.html')


def login_view(request):
    try: 
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('/admin/')

                elif request.user.is_authenticated:
                    if UserProfile.objects.filter(user=request.user).exists():
                        url = UserProfile.objects.get(user=user)
                        u = 0
                        if url.is_approved:
                            u = url.courses.pk
                            return redirect(course, u)

                    else:
                        return redirect(not_approved)
                else:
                    return redirect(login_view)                   
                return redirect(home)

        return render(request, 'login.html')
    except ObjectDoesNotExist:
        return redirect(page_not_found)

def logout_view(request):
    logout(request)
    return redirect('home')

def password_change_view(request):
    return PasswordChangeView.as_view()(request, template_name='password_change.html')

def password_change_done_view(request):
    return PasswordChangeDoneView.as_view()(request, template_name='password_change_done.html')

def password_reset_view(request):
    return PasswordResetView.as_view()(request, template_name='password_reset.html')

def password_reset_done_view(request):
    return render(request, 'password_reset_done.html')

def password_reset_confirm_view(request, uidb64, token):
    return PasswordResetConfirmView.as_view()(request, uidb64=uidb64, token=token, template_name='password_reset_confirm.html')

def password_reset_complete_view(request):
    return PasswordResetCompleteView.as_view()(request, template_name='password_reset_complete.html')

def terms(request):
    return render(request, 'terms.html')

def policy(request):
    return render(request, 'policy.html')


def forgot(request):
    # This function recovers the user's password
    try:
    # Get form data from POST request
        if request.method == 'POST':
            email = request.POST.get('email')
            user1 = User.objects.get(email=email)
            if user1:
                password = generate_password()
                send_password_email(email, password)
                user1.set_password(password)
                user1.save()
            return redirect(password_reset_done_view)
    except Exception:
        return redirect(password_reset_done_view)
    # Render the recovery form template if the request method is GET
    return render(request, 'forgot.html')

def english(request):
    return render(request, 'english.html')

def spanish(request):
    return render(request, 'spanish.html')

def poland(request):
    return render(request, 'poland.html')

def seamen(request):
    return render(request, 'seamen.html')

def about_me(request):
    return render(request, 'about_me.html')

# page_not_found( HttpRequest, Exception, '404.html') 

