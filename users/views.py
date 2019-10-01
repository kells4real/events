from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import DetailView
from django.contrib.auth.models import User
from . models import Profile
from app.models import Event
from django.contrib.auth import login
import time


from .tokens import account_activation_token


def register(request):
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.email = register_form.cleaned_data['email']
            user.set_password(register_form.cleaned_data['password'])
            user.is_active = False
            # Save the User object
            user.save()

            # get current site
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            # create Message
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # send activation link to the user
            user.email_user(subject=subject, message=message)
            messages.success(request, 'Your account has been created successfully, '
                                      ' you still have to check your mail for a link '
                                      'to activate your account before you can sign in..')
            return redirect('login')

    else:
        register_form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': register_form})


def activate_link(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError,User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('login')
    else:
        return render(request, 'users/account_activation_invalid.html')


@login_required
def profile(request):
    activate = 'profile'
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
        else:
            messages.error(request, f'Please correct the error(s) below.!')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'activate': activate,
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/edit_profile.html', context)


def display_profile(request):
    logged_in_user_events = Event.objects.filter(author=request.user).all()
    context = {"url": "profile",
               "user_event": logged_in_user_events
               }
    return render(request, 'users/profile.html', context)


class DisplayProfile(DetailView):
    model = Profile
    template_name = 'users/profile_detail.html'



