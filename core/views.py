from django.template import RequestContext
from django.shortcuts import render,redirect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db import transaction
from core.forms import *

#to login
@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html') 

#user registration
def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],email=form.cleaned_data['email'])
            messages.success(request, "Registration Successful")
            return redirect('/login') 
        else:
           messages.error(request, "Please correct the error below")
           return render(request,'registration/register.html',{'form':form})
          
    else:
        form = RegistrationForm()
        return render(request,'registration/register.html',{'form':form})

#viewing user profile
@login_required(login_url='/login')
def view_profile(request):
    return render(request, 'profiles/view_profile.html')


#updating user profile
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


#viewing user settings
@login_required(login_url='/login')
def settings(request):
    return render(request, 'settings/settings.html')


#change password functionality
@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # to update session data to prevent user from logging out
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'settings/change_password.html', {'form': form})

 
#delete account
@login_required(login_url='/login')
def delete_user(request):
    if request.method == 'POST':
        form = DeleteUserForm(request.POST)
        if form.is_valid():
           cuser = request.user
           try:
                user = User.objects.get(username = form.cleaned_data['username'])
                if user.username == cuser.username:                                   
                    user.delete()
                    messages.success(request, 'Your account has been deleted successfully. Looking forward to having you back again')
                    return redirect('/login')  
                else:
                    messages.error(request, 'You are not authorised to perform this operation') 
           except ObjectDoesNotExist:
               user = None
               messages.error(request,'Invalid Username')           
        else:
            messages.error(request, 'Please correct the error below')
    else:
        form = DeleteUserForm()
    return render(request, 'settings/delete_user.html', {'form' : form}) 


#writing testimonial
@login_required(login_url='/login')
@transaction.atomic
def write_testimonial(request):
    if request.method == 'POST':
        testimonial_form = TestimonialForm(request.POST)
        if testimonial_form.is_valid():
            testimonial = testimonial_form.save(commit = False)
            testimonial.user = request.user
            testimonial.save()
            messages.success(request,'Thanks for writing')
            return redirect('/profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
       testimonial_form = TestimonialForm()
    return render(request, 'profiles/write_testimonial.html', {
        'testimonial_form' : testimonial_form
    })

#viewing testimonial
@login_required(login_url='/login')
def view_testimonial(request):
    testimonial = Testimonial.objects.get(user = request.user)
    return render(request,'profiles/view_testimonial.html', {'testimonial': testimonial})

#deleting testimonial
@login_required(login_url='/login')
def delete_testimonial(request):
    if request.method == 'GET':
        try :
            testimonial = Testimonial.objects.get(user = request.user)
            testimonial.delete()
            messages.success(request,'Testimonial deleted successfully')
            return render(request,'profiles/view_profile.html') 
        except ObjectDoesNotExist:
            messages.error(request, 'You have not written a testimonial')
            return render(request,'profiles/view_profile.html') 