from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Settings,ContactMessage,ContactForm
from django.contrib import messages
# Create your views here.


def index (request):
    setting=Settings.objects.get(pk=1)
    context={"setting":setting}
    return render(request,"index.html",context)
    


def index1 (request):
    setting=Settings.objects.get(pk=1)
    context={"setting":setting}
    return render(request,"page1.html",context)
    

def HowItWorks (request):
    setting=Settings.objects.get(pk=1)
    context={"setting":setting}
    return render(request,"HowItWorks.html",context)  
     
            
def contactus(request):
    setting=Settings.objects.get(pk=1)
    context={"setting":setting}
    if request.method=="POST":
        data=ContactMessage()
        data.name=request.POST.get('name')
        data.email=request.POST.get('email')
        data.subject=request.POST.get('subject')
        data.message=request.POST.get('message')
        data.ip=request.META.get('REMOTE_ADDR')
        data.save()
        messages.success(request,"your message has ben sent. thank you for your message")
        return HttpResponseRedirect('/contactus')
    else:
        return render(request,"contact.html",context)
       


def contactus1(request):
    setting=Settings.objects.get(pk=1)
    context={"setting":setting}
    if request.method=="POST":
        data=ContactMessage()
        data.name=request.POST.get('name')
        data.email=request.POST.get('email')
        data.subject=request.POST.get('subject')
        data.message=request.POST.get('message')
        data.ip=request.META.get('REMOTE_ADDR')
        data.save()
        messages.success(request,"your message has ben sent. thank you for your message")
        return HttpResponseRedirect('/contact')
    else:
        return render(request,"contact1.html",context)
       

