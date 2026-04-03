from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, SignupModelForm, UpdateProfileForm, ChangePasswordForm, EmailForm, ResetPasswordForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from .models import AuthUser
from django.http import Http404
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from time import time
from django_ratelimit.decorators import ratelimit
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core import signing
from uuid import uuid4
from time import sleep



# Create your views here.





def gen_activation_link(user):
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)
    return reverse('accounts:activation_account_link_url', args=[uid, token])



@ratelimit(key='ip', rate='5/m', block=True)
@ratelimit(key='post:email', rate='3/m', block=True, method='POST')
def login_view(request):
    if request.user.is_authenticated:
        return redirect('product:products_url')
    
    
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            

            try:
                user = AuthUser.objects.get(email=email)
                
                if user.check_password(password):
                    # CASE (1): if valid password and the user exists but is not activated!
                    if not user.is_active:
                        request.session['activation_account'] = email
                        url = reverse('accounts:resend_activation_link_url')
                        message = mark_safe("You have to active your account.\n" \
                        f"If you haven't received the account activation link in your email, you can resend it <a href='{url}'>from here.</a>")
                        messages.error(request, message)
                        return redirect('accounts:login_view_url')
                    
                    # CASE (2): if valid password and the user exists and is activated!
                    if not remember_me:
                        request.session.set_expiry(0)

                    

                    # make sure to delete the session (activation_account) then login
                    request.session.pop('activation_account', None)

                    login(request, user)
                    next_url = request.GET.get('next')
                    if next_url and url_has_allowed_host_and_scheme(
                        url=next_url,
                        allowed_hosts={request.get_host()},
                        require_https=request.is_secure()
                    ):
                        return redirect(next_url)
                    
                    
                    return redirect('product:products_url', category="all")
                


                # CASE (3): if invalid password and the user exists
                messages.error(request, 'Invalid email or password!')
                return redirect('accounts:login_view_url')
                

            # CASE (4): if invalid email (user doesn't exist)
            except AuthUser.DoesNotExist:         
                messages.error(request, 'Invalid email or password!')
                return redirect('accounts:login_view_url')
    


    # If the request is GET show the page
    return render(request, 'accounts/login.html', {"form": form})




def signup_view(request):
    if request.user.is_authenticated:
        return redirect("pages:home_url")
    
    form = SignupModelForm()
    if request.method == 'POST':
        form = SignupModelForm(request.POST)

        if form.is_valid():
            user = form.save()
            link = request.build_absolute_uri(gen_activation_link(user))
            send_activation_link(user, link)


            request.session['activation_account'] = user.email
            
            return redirect('accounts:activation_message_url')
        return render(request, 'accounts/signup.html', {'form': form})

    return render(request, 'accounts/signup.html', {'form': form})


def activation_account(request):
    email = request.session.get('activation_account')
    if email:
        return render(request, 'accounts/activation_message.html', {'email': email})
    else:
        raise Http404
    


@ratelimit(key="ip", rate='5/m', block=True)
@ratelimit(key='post:email', rate='3/m', block=True, method="POST")
def resend_activation_link(request):
    email = request.session.get('activation_account')

    if not email:
        raise Http404
    
    # check if email already activated
    user = get_object_or_404(AuthUser, email=email)
    if user.is_active:
        messages.info(request, 'Your account is already activated!')
        request.session.pop('activation_account')
        return redirect('accounts:login_view_url')
    

    if request.method == "POST":

        # check sending time (Prevent continuous repeated sending)
        seconds = 60
        last_send_time = request.session.get('last_send_time', 0)
        current_time = time()
        if (current_time - last_send_time) < seconds:
            wait_time = int((seconds - (current_time - last_send_time)))
            messages.error(request, f'wait for {wait_time}s to resend a new link!')
            return redirect('accounts:resend_activation_link_url')
        


        # check if the user put his email (prevent sending links to other emails!)
        if request.POST.get('email') != email:
            messages.error(request, 'Please enter the email address you registered with!')
            return redirect('accounts:resend_activation_link_url')
        


        # resend
        link = request.build_absolute_uri(gen_activation_link(user))
        send_activation_link(user, link)
        request.session['last_send_time'] = current_time
        messages.info(request, 'We sent a new activation link, Please check your email.')
        return redirect('accounts:resend_activation_link_url')

        

    return render(request, 'accounts/resend_form.html')
    





def send_activation_link(user, link):
    subject = "Activation Account"
    message = f'To activate your account, please click on the link below.\nLink:\n {link}'

    user_email = user.email
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=[user_email,])





def activation_error_message(request):
    email = request.session.get('activation_account')
    if email:
        return render(request, 'accounts/activation_error_message.html', {'email': email})
    else:
        raise Http404



def activation_account_link(request, uid, token):
    
    try:
        uid = urlsafe_base64_decode(uid).decode()
        user = AuthUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, AuthUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if user.is_active:
            messages.info(request, 'Your account is already activated!')
            return redirect('accounts:login_view_url')
        
        user.is_active = True
        user.save()
        request.session.pop('activation_account')
        messages.success(request, 'Your account has been activated!')
        return redirect('accounts:login_view_url')
    

    url = reverse('accounts:resend_activation_link_url')
    error_message = mark_safe("The activation link is invalid or expired.\n" \
    f"Please resend a new activation link <a href='{url}'>from here</a>.")
    messages.error(request, error_message)
    return redirect('accounts:activation_error_message_url')
    


@login_required
@ratelimit(key='post:user', rate='10/m', block=True)
def profile(request, username):
    the_user = get_object_or_404(AuthUser, username=username)

    if request.user.username != the_user.username:
        raise PermissionDenied()

    if request.method == "POST":
        form = UpdateProfileForm(request.POST, request.FILES, instance=the_user)
        if form.is_valid():
            account = form.save(commit=False)
            should_remove = request.POST.get('remove-image-flag')

            if should_remove == "true":
                account.img = None
            account.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile_view_url', username=username)
        


    else:
        form = UpdateProfileForm(instance=the_user)
    return render(request, 'accounts/profile.html', {'the_user': the_user, "form": form})



@login_required
@ratelimit(key='post:user', rate='10/m', block=True)
def change_password(request, username):
    the_user = get_object_or_404(AuthUser, username=username)
    if request.user.username != the_user.username:
        raise PermissionDenied
    
    if request.method == "POST":
        form = ChangePasswordForm(data=request.POST, user=the_user)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            the_user.set_password(new_password)
            the_user.save()
            update_session_auth_hash(request, the_user)
            messages.success(request, 'Your password has been updated!')
            return redirect('accounts:change_password_url', username=the_user.username)
        
        return render(request, 'accounts/change_password.html', {'the_user': the_user, "form": form})
            
            

    else:
        form = ChangePasswordForm(user=the_user)
        return render(request, 'accounts/change_password.html', {'the_user': the_user, "form": form})




@login_required
def logout_account(request):
    if request.method == "POST":
        logout(request)
        return redirect('accounts:login_view_url')

    return redirect("pages:home_url")




@ratelimit(key="post:user.email", rate='5/m', block=True)
def check_email(request):
    if request.user.is_authenticated:
        return redirect('pages:home_url')
    

    if request.method == "POST":
        form = EmailForm(request.POST)

        if form.is_valid():
            try:
                user = AuthUser.objects.get(email=form.cleaned_data['email'])
                random_uuid = str(user.pk)
                token = signing.dumps(random_uuid, salt=f'reset_password-{user.password}')
                url = reverse('accounts:reset_password_url', args=[token])
                link = request.build_absolute_uri(url)

                
                send_mail(
                    subject="Reset Your Password",
                    message=f'Please enter the link below to reset password\nLink: {link}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email]
                )
                messages.info(request, 'If your email address is registered with us, we have sent you a link to change your password. Check your email.')
                return redirect('accounts:check_email_url')
            except AuthUser.DoesNotExist:
                sleep(3)
                messages.info(request, 'If your email address is registered with us, we have sent you a link to change your password. Check your email.')
                return redirect('accounts:check_email_url')

    form = EmailForm()
    return render(request, 'accounts/email.html', {'form': form})



def reset_password(request, token):
    if request.user.is_authenticated:
        return redirect('pages:home_url')
    
    try:
        payload = token.split(":")[0]
        
        user_id_json = signing.b64_decode(payload.encode()).decode()
        import json
        user_id = json.loads(user_id_json)

        user = AuthUser.objects.get(pk=user_id)
        user_id = signing.loads(token, salt=f'reset_password-{user.password}', max_age=600)
        
    except (signing.SignatureExpired, signing.BadSignature, AuthUser.DoesNotExist):
        messages.error(request, 'The link is invalid or expired!')
        return redirect('accounts:check_email_url')

    
    if request.method == "POST":
        form = ResetPasswordForm(data=request.POST, user=user)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            messages.info(request, 'Your password has been updated!')
            return redirect('accounts:login_view_url')
    else:
        form = ResetPasswordForm(user=user)
        
    return render(request, 'accounts/reset_password.html', {'form': form})
