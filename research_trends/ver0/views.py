from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request, "ver0/index.html")

def keywords_page(request):
    return render(request, "ver0/keywords.html")

def researchers_page(request):
    return render(request, "ver0/researchers.html")

def institutes_page(request):
    return render(request, "ver0/institutes.html")
