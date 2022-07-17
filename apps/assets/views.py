from django.shortcuts import render

def assets(request):
    return render(request, 'assets/assets.html')

def configuration(request):
    return render(request, 'assets/configuration.html')