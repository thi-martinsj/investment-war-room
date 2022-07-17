from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth, messages

from assets.views import get_user_monitored_assets

def login(request):
    if is_authenticated(request) or check_login(request):
        return redirect("dashboard")
        
    return render(request, 'users/login.html')

def register(request):
    if create_register(request):
        return redirect("login")
    return render(request, 'users/register.html')

def dashboard(request):
    if request.user.is_authenticated:
        data = {
            'assets': get_user_monitored_assets(request),
        }

        return render(request, 'users/dashboard.html', data)

    return redirect('login')

def logout(request):
    auth.logout(request)
    return redirect("login")

def is_authenticated(request):
    return request.user.is_authenticated

def check_login(request):
    """Check user's credentials"""
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(email=email).exists():
            username = User.objects.filter(email=email).values_list("username", flat=True).get()
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return True

        messages.error(request, "Invalid email or password")

    return False

def create_register(request):
    """Create a register"""
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            print("senhas precisam ser iguais")
            messages.error(request, "Passwords must be the same")
            return False

        if User.objects.filter(email=email).exists():
            print("usuário já existe email")
            messages.error(request, "User already exists")
            return False

        if User.objects.filter(username=username).exists():
            print("usuário já existe username")
            messages.error(request, "User already exists")
            return False

        user = User.objects.create_user(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = password1
        )
        user.save()
        messages.success(request, "Successfully registered")

        return True
    
    return False


