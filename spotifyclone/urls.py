from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from spotifyclone import views
from .views import EmailValidationOnForgotPassword
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='Index'),
    path('home', views.home, name='Home'),
    path('home1', views.home1, name='Home1'),
    path('addPage', views.addMusic, name='Add song'),
    path('about', views.about, name='About'),
    path('login', views.login, name='Login'),
    path('signup', views.signup, name='Signup'),
    path('verify/<auth_token>', views.verify, name="verify"),
    path('email', views.userEmail, name='Email'),
    path('error', views.error, name='Error'),

    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword),
         name="password_reset"),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
         name="password_reset_complete"),
    path('accounts/', include('allauth.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)