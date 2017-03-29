from django.template import RequestContext
from django.shortcuts import render,redirect #render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from core.forms import *
# Create your views here.

@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html') #{'user' : request.user})

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],email=form.cleaned_data['email'])
            return redirect('/login') #redicrect func used
        else:
            #form = RegistrationForm()
            #variables = RequestContext(request, {'form': form})
            return render(request,'registration/register.html',{'form':form})
            #return render(request, 'registration/register.html', {'form' : form})
    else:
        form = RegistrationForm()
        #variables = RequestContext(request, {'form': form})
        return render(request,'registration/register.html',{'form':form})

@login_required(login_url='/login')
def view_profile(request):
    return render(request, 'profiles/view_profile.html')



@login_required(login_url='/login')
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile was successfully updated!')
            return redirect('/profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


