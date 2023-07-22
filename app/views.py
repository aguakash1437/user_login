from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from app.models import *
from app.forms import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.


def registration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}
    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST ,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            NSUFO=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            NSUFO.set_password(password)
            NSUFO.save()

            NSPFO=pfd.save(commit=False)
            NSPFO.username=NSUFO
            NSPFO.save()

            send_mail('Registration', ## sub
                      "successfully done Registration!!", ## msg/body
                      'messileo143710@gmail.com', ## user_mail
                      [NSUFO.email],  ## recipent_mail
                      fail_silently=False)  ## Check errors 
            
            


            return HttpResponse('registration successfully!!!')

    return render(request,'registration.html',d)



def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')


def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO:
            if AUO.is_active:
                login(request,AUO)
                request.session['username']=username
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('Not active user')
        else:
            return HttpResponse('Invalid user')
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_details(request):
     username=request.session.get('username')
     uo=User.objects.get(username=username)
     po=Profile.objects.get(username=uo)
     d={'uo':uo,'po':po}
     return render(request,'display_details.html',d)


@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['pw']
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('Password is changed successfully')
    return render(request,'change_password.html')


@login_required
def forget_password(request):
    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']

        LUO=User.objects.filter(username=un)
        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save()
            return HttpResponse('Password reset is done')
        else:
            return HttpResponse('username is not avaialble in DB')
    return render(request,'forget_password.html')