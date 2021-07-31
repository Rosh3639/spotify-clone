from django.conf import settings
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from .models import Song, Album, Music, Users
from django.core.paginator import Paginator
from .form import AddMusicForm
import uuid
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
import threading
from django.core.mail import EmailMessage
from django.contrib.auth import login as auth_login
from django.forms import forms


# Create your views here.

def index(request):
    return render(request, 'index.html')


def home(request):
    paginator = Paginator(Song.objects.all(), 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, "home.html", context)


def home1(request):
    musics = list(Music.objects.all().values())
    return render(request, 'home1.html', {
        'musics': musics
    })


def addMusic(request):
    form = AddMusicForm()

    if request.POST:
        form = AddMusicForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            album = form.cleaned_data.get('album')
            if album:
                music_album = Album.objects.get_or_create(name=album)
                print(music_album)
                instance.album = music_album[0]
                instance.save()
                return redirect("/home1")
            else:
                instance.save()
                return redirect("/home1")

        else:
            print("no", form.data)

    return render(request, 'addPage.html', {
        'form': form
    })


def about(request):
    return render(request, 'about.html')


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password, email=email)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('/home1')
        elif user is None:
            messages.error(request, 'Incorrect Username or Password ')
            return redirect('/login')

        users_obj = Users.objects.filter(user=user).first()
        if not users_obj.is_verified:
            messages.success(request, 'Account is not verified please check your mail!')
            return redirect('/login')

        if authenticate(username=username, password=password):
            if user is not None:
                login(request, user)
                return redirect("/home1")
            else:
                return render(request, 'login.html')
    return render(request, 'login.html')


class EmailThread(threading.Thread):
    def __init__(self, msg):
        self.msg = msg
        threading.Thread.__init__(self)

    def run(self):
        self.msg.send()


def custom_login(request):
    response = login(request)
    if request.user.is_authenticated():
        messages.info(request, "Welcome ...")
    return response


def send_mail_after_registration(email, auth_token):
    subject = 'Your account need to be verified'
    message = (
        f"Hi please paste this link in your browser to verify your account https://sklone.herokuapp.com/verify/{auth_token}")
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    msg = EmailMessage(subject, message, from_email, recipient_list)
    EmailThread(msg).start()


def signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')

        try:
            if User.objects.filter(email=email).first():
                messages.success(request, 'Email is taken')
                return redirect('/signup')

            if User.objects.filter(username=username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/signup')

            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            users_obj = Users.objects.create(user=user_obj, auth_token=auth_token)
            users_obj.save()
            send_mail_after_registration(email, auth_token)
            return redirect('/email')
        except Exception as e:
            print(e)
    return render(request, 'signup.html')


def verify(request, auth_token):
    try:
        user_obj = Users.objects.filter(auth_token=auth_token).first()
        if user_obj:
            if user_obj.is_verified:
                messages.success(request, 'Account already verified!')
                return redirect('/login')

            user_obj.is_verified = True
            user_obj.save()
            messages.success(request, 'Your account has been verified!')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)


def userEmail(request):
    return render(request, 'email.html')


def error(request):
    return render(request, 'error.html')


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("There is no user registered with the specified email address!")
        return email
