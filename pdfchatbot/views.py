from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.files.uploadedfile import UploadedFile
from typing import Optional
from .chatbot import chatbot_is_file_uploaded, chatbot_process_pdf,\
                     chatbot_answer, chatbot_get_file_name

file_uploaded = False
messages: list[dict[str,str]] = list()

def clear_messages():
    global messages
    messages = []

def get_messages():
    global messages
    return messages

def home(request: HttpRequest) -> HttpResponse:
    #GET is the only one allowed
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    return render(request, "home.html", {"file_uploaded": chatbot_is_file_uploaded(),
                                         "file_name": chatbot_get_file_name(),
                                         "chat_messages": messages != [],
                                         "messages": messages}) 

def upload(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    file: Optional[UploadedFile] = request.FILES.get("pdf_input")
    chatbot_process_pdf(file)
    return redirect("home")

def chat(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        question = request.POST.get("chat_input")
        if question:
            messages.append({"type":"question", "content": "User: " + question})
            answer = chatbot_answer(question)
            messages.append({"type":"answer", "content": "Chatbot: " + answer})
        return redirect("home")
    else:
        return HttpResponseNotAllowed(["POST"])

