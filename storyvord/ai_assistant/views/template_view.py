from django.shortcuts import render

def chat_page(request):
    return render(request, 'chat/index.html')

def wss_page(request):
    return render(request, 'chat/wss.html')