from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('registr/', registr, name='registr'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password_change/', password_change_view, name='password_change'),
    path('password_change/done/', password_change_done_view, name='password_change_done'),
    path('password_reset/', password_reset_view, name='password_reset'),
    path('password_reset_done/', password_reset_done_view, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),
    path('reset/done/', password_reset_complete_view, name='password_reset_complete'),
    path('course/<int:course_id>', course, name='course'),
    path('terms/', terms, name='terms'),
    path('policy/', policy, name='policy'),
    path('forgot/', forgot, name='forgot'),
    path('not_approved/', not_approved, name='not_approved'),
    path('english/', english, name='english'),
    path('spanish/', spanish, name='spanish'),
    path('poland/', poland, name='poland'),
    path('seamen/',seamen, name='seamen'),
    path('about_me/',about_me, name='about_me'),
    path('photo/<str:content>', photo, name='photo_view'),
    path('video/<str:content>', photo, name='photo_view'),
    path('audio/<str:content>', photo, name='photo_view'),
]
