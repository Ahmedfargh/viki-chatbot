from django.shortcuts import render
from django.shortcuts import render

# Create your views here.
def get_to_chat_page(request):
    return render(request,"messages.html")