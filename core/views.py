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
    if request.method == 'GET':
         try:
            testimonial = Testimonial.objects.get(user = request.user)
            messages.success(request, 'You have already written a testimonial')
            return render(request,'profiles/view_testimonial.html', {'testimonial': testimonial})
         except ObjectDoesNotExist:
            testimonial_form = TestimonialForm()
            return render(request, 'profiles/write_testimonial.html', {'testimonial_form':testimonial_form})

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
    if request.method == 'GET':    
        try:        
            testimonial = Testimonial.objects.get(user = request.user)
            return render(request,'profiles/view_testimonial.html', {'testimonial': testimonial})
        except ObjectDoesNotExist:
            messages.error(request,'You have not written a testimonial')
            return render(request, 'profiles/view_profile.html')


#deleting testimonial
@login_required(login_url='/login')
@transaction.atomic
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


#question and answer page
@login_required(login_url='/login')
def question_answer(request):
    q = []
    if request.method == 'GET':
        answer = Answer.objects.all()
        for a in answer:
            q.append(a.question_id)
        ques = Question.objects.filter(pk__in=q).order_by('-pub_date')
        if ques.exists():
            return render(request, 'question_answer/question_home.html', {'ques':ques})
        else:
            messages.error(request, 'No questions to display')
            return render(request, 'question_answer/question_home.html')


#view unanswered questions
@login_required(login_url='/login')
def view_unanswered_question(request):
    q = []
    if request.method == 'GET':
        answer = Answer.objects.all()
        for a in answer:
            q.append(a.question_id)
        ques = Question.objects.exclude(pk__in=q).order_by('-pub_date')
        if ques.exists():
            return render(request, 'question_answer/unanswered_question.html', {'ques':ques})
        else:
            messages.error(request, 'No questions to display')
            return render(request, 'question_answer/question_home.html')
                

#post a question
@login_required(login_url='/login')
@transaction.atomic
def post_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit = False)
            question.user = request.user
            question.save()
            ques = Question.objects.filter(user = request.user).order_by('-pub_date')
            messages.success(request, 'Question Posted')
            return render(request, 'question_answer/asked_question.html', {'ques' : ques}) 
        else:
            messages.error(request, 'Please correct the error below')
    else:
        question_form = QuestionForm()
        return render(request, 'question_answer/post_question.html', {'question_form' : question_form}) 


#answer a question
@login_required(login_url='/login')
@transaction.atomic
def post_answer(request,pk):
    if request.method == 'GET':
        ques = Question.objects.get(id=pk)
        ans = Answer.objects.filter(user=request.user, question=pk) 
        if ans.exists():    
            messages.success(request, 'You have already answered this question')
            return render(request, 'question_answer/view_answer.html', {'ques':ques, 'ans':ans} ) 
        else:
            answer_form = AnswerForm()
            return render(request, 'question_answer/post_answer.html', {'answer_form' : answer_form} ) 
    
    if request.method == 'POST':
        ques = Question.objects.get(id = pk)
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            ans = answer_form.save(commit = False)
            ans.user = request.user
            ans.question_id = pk
            ans.save()
            ans = Answer.objects.filter(question_id=pk).order_by('-pub_date')
            messages.success(request, 'Answer submitted successfully')
            return render(request, 'question_answer/view_answer.html', {'ques' : ques , 'ans' : ans}) 
        else:
            messages.error(request, 'Please correct the error below')
    else:
        answer_form = AnswerForm()
        return render(request, 'question_answer/post_answer.html', {'answer_form' : answer_form}) 


#view asked questions
@login_required(login_url='/login')
def view_asked_question(request):
    if request.method == 'GET':
        ques = Question.objects.filter(user = request.user).order_by('-pub_date')
        if ques.exists():    
            return render(request,'question_answer/asked_question.html', {'ques' : ques}) 
        else:
            messages.error(request, 'You have not asked any questions')
            

#view answers for a question
@login_required(login_url='/login')
def view_answer(request,pk):
    ques = Question.objects.get(id=pk)
    ans = Answer.objects.filter(question_id=pk).order_by('-pub_date')
    if ans.exists():
        return render(request, 'question_answer/view_answer.html', {'ques' : ques, 'ans' : ans})
    else:
        messages.error(request, 'This question has not been answered yet')
        return render(request, 'question_answer/asked_question.html', {'ques' : ques})


#view answered questions
@login_required(login_url='/login')
def view_answered_question(request):
        question = Question.objects.all()
        ques = question.answer_set.filter(user = request.user).order_by('-pub_date')
        if ques.exists():
            return render(request, 'question_answer/answered_question.html', {'ques' : ques})
        else:
            message.error(request, 'You have not answered any questions')


#delete question
@login_required(login_url='/login')
@transaction.atomic
def delete_question(request,pk2):
    if request.method == 'GET':
        ques = Question.objects.get(id=pk2)
        if ques.user == request.user:
            ques.delete()
            ques = Question.objects.all().order_by('-pub_date')
            messages.success(request, 'Question deleted successfully')
            return render(request, 'question_answer/question_home.html', {'ques' : ques})
        else:
            messages.error(request, 'You are not authorised to perform this action')
            ques = Question.objects.all().order_by('-pub_date')
            return render(request, 'question_answer/question_home.html', {'ques' : ques})



    