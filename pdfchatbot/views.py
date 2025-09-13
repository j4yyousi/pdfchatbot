from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

def home(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")

def upload(request: HttpRequest) -> HttpResponse:
    return redirect(reverse("home"))

