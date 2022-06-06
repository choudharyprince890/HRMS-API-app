from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# def home(request):
#     return HttpResponse("okkk")

def login(request):
    return render(request,'login.html')


def dashboard(request):
    return render(request,'dashboard.html')

def topnav(request):
    return render(request,'topnav.html')

def employee(request):
    return render(request,'employee.html')