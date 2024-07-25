from django.shortcuts import redirect, render
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from django.http import HttpResponse

from django.conf import settings
import random
from django.core.cache import cache
from django.core.mail import send_mail
from .helper import send_forgot_passwrod_mail
# import uuid
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
import hashlib


# from django.views.decorators.cache import cache_control



# Create your views here.
def sign_up(request):
    if request.user.is_authenticated:
        return redirect('home')



    if request.method == 'POST':
        # username = requset.POST.get('username')
        username  = request.POST['username']
        email     = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        #credentials are saving in session
        request.session['username'] = username
        request.session['email'] = email
        request.session['password'] = password1



        #validation for signup
        if username.strip() == '' or email.strip() == '' or password1.strip() == '' or password2.strip() == '':
            messages.error(request, "All fields are required")
            return render(request, "signup.html")
        
        if len(password1) < 8 or len(password2) < 8:
            messages.error(request, "Password must have 8 characters!")
            return render(request, "signup.html")
        
        
        if password1 == password2:
            if len(username) > 15:
                messages.error(request, "Username must be under 15 characters!")
                return render(request, "signup.html")
            elif Account.objects.filter(username=username).exists():
                messages.error(request, "Username already exists! Please try some other username")
                return render(request, "signup.html")
            elif not username.isalnum():
                messages.error(request, "Username must be in Alpha-numeric!")
                return render(request, "signup.html")
            elif Account.objects.filter(email=email).exists():
                messages.error(request, "Email already in use! Please try some other email")
                return render(request, "signup.html")
            else:
                #generating otp & saves in cache
                random_otp = str(random.randint(0000, 9999))
                key = hashlib.sha3_256(email.encode()).hexdigest()
                cache.set(key, random_otp, 50)
                print(random_otp)
                #sending email
                subject = "Welcome to StepWise !!!"
                message = (f"""Hello {username}
                           Your otp is generated
                           {random_otp}""") 
        
                to_list = [email]
                send_mail(subject, message, settings.EMAIL_HOST_USER, to_list, fail_silently=False)
                return redirect('otp_verification', key)
        else:
            messages.error(request, "Password is not matching!")
            return render(request, "signup.html")

        #creating user object
        # user = Account.objects.create_user(
        #     username = username, email = email, password = password1)
        # user.save()


    return render(request, "signup.html")


def otp_verification(request, key):
    if request.method == 'POST':
        submitted_otp = request.POST.get('submitted_otp')
        generated_otp = cache.get(key)
        print(f"submitted otp {submitted_otp}")
        print(f"generated otp {generated_otp}")

        if submitted_otp == generated_otp:
            user = Account.objects.create_user(
                username=request.session['username'],
                email=request.session['email'],
                password=request.session['password']
            )
            user.is_active = True
            user.save()

            # Clear the cache after successful verification
            cache.delete('generated_otp')
            request.session.flush()

            messages.success(request, "Your account has been successfully created.")
            return redirect('logIn')
        else:
            messages.error(request, "OTP doesn't match or has expired.")
            cache.delete('generated_otp')
            return redirect(request.META.get('HTTP_REFERER'))


    # Handle the case where the request method is not POST (GET, etc.)
    return render(request, "otp.html" ,{"key": key})
    


def resend_otp(request, key):
    if request.method == 'GET':
        print('resend function called')
        email = request.session.get('email')
        username = request.session.get('username')

        # Generating new OTP
        random_otp = str(random.randint(0000, 9999))
        cache.set(key, random_otp, 50)
        print('resended otp:', random_otp)

        # Sending email
        subject = "Resend OTP - StepWise !!!"
        message = (f"""Hello {username}
                   Your New OTP is generated
                   {random_otp}""")
        
        to_list = [email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, to_list, fail_silently=False)
        messages.success(request, "New OTP has been sent to your email")    

    # Redirect the user back to the OTP verification page
    return redirect(request.META.get('HTTP_REFERER'))


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def log_in(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        email = request.POST['email']
        password1 = request.POST['password1']

        user = authenticate(email=email, password=password1)

        if user is not None:
            if user.is_superuser:
                messages.error(request, "Admin Is Not Allowed To Log in User Side")
                return redirect('logIn')
            else:
                login(request, user)
                # username = user.username
                # messages.success(request, "Logged in successfully")
                return redirect('home')  #try to pop a successfull message when logged in with username
        else:
            messages.error(request, "invalid credentials")
            return redirect('logIn')

    return render(request, "login.html")


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def log_out(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('logIn')



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)
            encrypt_id = urlsafe_base64_encode(str(user.id).encode())
            
            reset_link = f"{request.scheme}://{request.get_host()}{reverse('changepassword', args=[encrypt_id])}"

            #store the token in cache
            cache_key = f'password_reset_{encrypt_id}'
            cache.set(cache_key, {'reset_link': reset_link}, timeout=60)

            #sending email
            send_forgot_passwrod_mail(email, reset_link)
            messages.error(request, f"An email is sent to {email}. Please verify it.")
            return redirect('forgotpassword')
        else:
            messages.error(request, "Email doesn't exist")
            return redirect('forgotpassword')
    
    return render(request, "forgotPassword.html")



def change_password(request, encrypt_id):
    #getting cache key and token
    cache_key = f'password_reset_{encrypt_id}'
    cached_data = cache.get(cache_key)

    if not cached_data:
            messages.error(request, "Expired token. Please request a new password reset.")
            return redirect('forgotpassword')
    
    if request.method == 'POST':
        new_password = request.POST['newPass']
        confirm_password = request.POST['confirmPass']

        if new_password == confirm_password:
             # Extract the user ID from the cached token
             id = str(urlsafe_base64_decode(encrypt_id), 'utf-8')
             id = int(id)

             try:
                 user = Account.objects.get(id=id)
                 user.set_password(new_password)
                 user.save()

                 cache.delete(cache_key)

                 messages.success(request, "Password has been changed successfully. You can now log in with your new password.")
                 return redirect('logIn')
             
             except Account.DoesNotExist:
                messages.success(request, "Invalid user, Please try again later")
                return redirect('changepassword', encrypt_id=encrypt_id)
        
        else:
            messages.error(request, "Passwords do not match. Please try again.")
            return redirect('change-password', encrypt_id=encrypt_id)

        
    return render(request, "changePassword.html")