from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def home(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<title>PDF Q/A Chatbot</title>")

