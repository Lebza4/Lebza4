from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
# To Activate Account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import NoReverseMatch, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError

#getting token from utils.py
from .utils import TokenGenerator, generate_token


# Emails
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core import mail
from django.conf import settings
from django.contrib import messages


# Threading
import threading
import logging

# reset password
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy

logger = logging.getLogger(__name__)

class EmailThread(threading.Thread):
    def __init__(self, email_message):
        super().__init__()
        self.email_message = email_message

    def run(self):
        try:
            self.email_message.send()
        except Exception as e:
            logger.exception("Error sending email: %s", e)
 
        
         

# Create your views here.

def signup(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'auth/signup.html')

        try:
            if User.objects.get(username=email):   
                messages.warning(request,"Email is Taken")
                return render(request,'auth/signup.html')

        except Exception as indentifier:
            pass

        user=User.objects.create_user(email,email,password)
        user.is_active=False
        user.save()
        current_site=get_current_site(request)
        email_subjects="Activate Your Account"
        message=render_to_string('auth/activate.html',{
            'user':user,
            'domain':'http://127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
            
            
        })
        
        email_message = EmailMultiAlternatives(email_subjects, message, from_email=settings.EMAIL_HOST_USER, to=[email])

        EmailThread(email_message).start()
        messages.info(request,"Activate Your Account Bye click the Link on your email")
        return redirect('/leboauth/login/')

    return render(request,'auth/signup.html')



class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid= str(urlsafe_base64_decode(uidb64), 'utf-8')

            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
            
        if user is not None and generate_token.check_token(user,token):
            user.is_active= True
            user.save()
            messages.info(request,"Account Activated Successfully")
            return redirect('leboauth/login')
        return render(request,'auth/activatefail.html')
    
            

def handlelogin(request):
    if request.method=="POST":
        
        username=request.POST['email']
        userpassword=request.POST['pass1']
        myuser=authenticate(username=username,password=userpassword)
        
        if myuser is not None:
            login(request, myuser)
            messages.success(request,"Login Success")
            return render(request,'index.html')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/leboauth/login')
         
        
        
    return render(request,'auth/login.html')



                

def handlelogout(request):
    logout(request)
    messages.success(request, "Logout successful.")
    return redirect('/leboauth/login/')

from django.shortcuts import redirect

class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'leboauth/password_reset_email.html'
    template_name = 'auth/password_reset_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.success_url)
    
    


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'auth/password_reset_confirm.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'auth/password_reset_complete.html'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'leboauth/password_reset_done.html'


def password_reset_link_sent(request):
    return render(request, 'leboauth/password_reset_link_sent.html')
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'leboauth/password_reset_done.html'


