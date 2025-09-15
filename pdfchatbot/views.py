from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.files.uploadedfile import UploadedFile
from typing import Optional
from .processpdf import process_pdf

file_uploaded = False
messages: list[dict[str,str]] = list()

def clear_messages():
    global messages
    messages = []

def get_messages():
    global messages
    return messages

def set_file_uploaded(val):
    global file_uploaded
    file_uploaded = val
    print(f"file_uploaded set to = {file_uploaded}")

def get_file_uploaded():
    global file_uploaded
    print(f"got file_uploaded = {file_uploaded}")
    return file_uploaded

def get_answer():
    return "take this for now"

def home(request: HttpRequest) -> HttpResponse:
    #GET is the only one allowed
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    return render(request, "home.html", {"file_uploaded": get_file_uploaded(),
                                         "chat_messages": messages != [],
                                         "messages": messages}) 

def upload(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    file: Optional[UploadedFile] = request.FILES.get("pdf_input") 
    process_pdf(file)
    set_file_uploaded(True)
    return redirect("home")

def chat(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        question = request.POST.get("chat_input")
        if question:
            messages.append({"type":"question", "content": "User: " + question})
            answer = get_answer()
            messages.append({"type":"answer", "content": "Chatbot: " + answer})
        return redirect("home")
    else:
        return HttpResponseNotAllowed(["POST"])

