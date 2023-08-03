
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import RegisterUserForm
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import User
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

# Create your views here.

def Signup_view(request):
    template_name = 'AUTH/signup.html'
    form=RegisterUserForm()
    if request.method == 'POST':
        form=RegisterUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            # Coverting unhasted password to hashed password and deactivating account
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(password)
            user.save()
            #Activation token generation
            token =default_token_generator.make_token(user)
            
            #Encode the users primary key and token as a URL base64 string
            uid= urlsafe_base64_encode(force_bytes(user.pk))
            #token = urlsafe_base64_encode(force_bytes(token))
            
            #Domain 
            domain = get_current_site(request)
            print(domain)
            
            #Activation link 
            activation_link = f'http://{domain}/activate/{uid}/{token}/'
            print(activation_link)
            #Email structure elements
            Subject='Activate your account'
            message = f'Hi {username} \n\n Thank you for registering, please use following link to activate your account.\n{activation_link}'
            from_email = settings.EMAIL_HOST_USER
            to_email = [email]
            send_mail(Subject,message,from_email,to_email)
            messages.success(request,"Your account is successfully created!!, Check mail for activation link")
            return redirect('lg_url')
            
    context={'form':form}
    return render(request,template_name,context)

def Login_view(request):
    template_name = 'AUTH/login.html'
    if request.method == 'POST':
        un=request.POST.get('un')
        pw=request.POST.get('pw')
        print(un)
        print(pw)
        user = authenticate(username=un,password=pw)
        print(user)
        if user is not None:
            login(request,user)
            messages.success(request,"Welcome")
            return redirect('home_url')
            
        else:
            messages.warning(request,"Your account is not activated!!")
            return redirect('home_url')
            
    
    return render(request,template_name)

def Logout_view(request):
    logout(request)
    messages.success(request,'Your account is logged out successfully')
    return redirect('lg_url')    
    
    
def Activate_account(request,uidb64,token):
    
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(user)
        print(token)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        print()
        user = None
    print(default_token_generator.check_token(user,token))
    if user is not None and default_token_generator.check_token(user,token):
        #Activate user account
        user.is_active = True
        user.save()
        messages.success(request,'Congratulation you account is activated!!')
        return redirect('lg_url')
        
    else:
        return HttpResponse('Account information is not correct')