from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from account.views import (
    CustomPasswordResetView,
    registration_view,
    LogoutView,
    LoginView,
    AccountView,
)
from school.views import(
    StudentHomeView,
    search_id,
    StudentCreateView,
    StudentView,
    search_name,
    SchoolCreateView,
    BookCreateView,
    SchoolView,
    BookView
)

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),

    path('', RedirectView.as_view(url='student/', permanent=True)),

    path('student/add/', StudentCreateView.as_view(), name='student-create'),
    path('student/', StudentHomeView.as_view(), name='home'),
    path('student/<pk>/', StudentView.as_view(), name='student'),

    path('school/add/', SchoolCreateView.as_view(), name='school-create'),
    path('school/<pk>/', SchoolView.as_view(), name='school'),
    path('book/add/', BookCreateView.as_view(), name='book-create'),
    path('book/<pk>/', BookView.as_view(), name='book'),

    # autocomplete views
    path('search-student-id/', search_id, name='search-company-id'),
    path('search-student-name/', search_name, name='search-student-name'),


    path('register/', registration_view, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('account/', AccountView.as_view(), name='account'),

    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_change.html'),
         name='password_reset_confirm'),

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]
