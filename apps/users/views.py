from django.shortcuts import redirect, render


def login(request):
    return render(request, 'usuarios/login.html')

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/dashboard.html')

    return redirect('login')