import re
from django.shortcuts import render


def login(request):
    return render(request, 'usuarios/login.html')