from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
# Create your views here.



from user.forms import SignUpForm

@csrf_protect
def login_form(request):
    
    try:
        if request.method=="POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            profile=User.objects.get(email=username)
            user = authenticate(request, username=profile.username, password=password)
        
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/home")
            else:
                messages.warning(request,"Login Error ! Username or Password is incorrect ")
                return HttpResponseRedirect("/login")
        return render(request,"login.html")
    except User.DoesNotExist:
        messages.warning(request,"Login Error ! Username or Password is incorrect ")
        return render(request,"login.html")
    
def register_form(request):    
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user=authenticate(username=username, password=password)
            login(request,user)
            return HttpResponseRedirect('/home')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect('/register')
    form = SignUpForm()
    context={'form':form,}
    return render (request,'signup.html',context) 

def logout_func(request):
    logout(request)
    return HttpResponseRedirect("/")      
