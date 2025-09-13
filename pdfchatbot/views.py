from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

def home(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "home.html")
    else:
        #GET is the only one allowed
        return HttpResponseNotAllowed(["GET"])

def upload(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        return redirect(reverse("home"))
    else:
        #POST is the only one allowed
        return HttpResponseNotAllowed(["POST"])

