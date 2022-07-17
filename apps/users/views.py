from django.shortcuts import redirect, render


def login(request):
    return render(request, 'users/login.html')

def register(request):
    return render(request, 'users/register.html')

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'users/dashboard.html')

    return redirect('login')