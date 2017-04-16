from django.template import RequestContext
from django.shortcuts import render,redirect 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db import transaction
from django.core.mail import send_mail
from core.models import *
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
            u = form.cleaned_data['username']
            p = form.cleaned_data['password1']
            group = form.cleaned_data['groupname']
            g = Group.objects.get(name=group)
            user.groups.add(g)
            user = authenticate(username=u,password=p)
            login(request,user)
            messages.success(request, "Please Fill Your Profile")
            return redirect('/profile/editprofile/') 
        else:
           messages.error(request, "Please correct the error below")
           return render(request,'registration/register.html',{'form':form})
          
    else:
        form = RegistrationForm()
        return render(request,'registration/register.html',{'form':form})


#to check whether user is an Alumni
def is_member(user):
    return user.groups.filter(name='Alumni').exists()


#viewing user profile
@login_required(login_url='/login')
def view_profile(request):
    return render(request, 'profiles/view_profile.html')


#viewing other's profile
@login_required(login_url='/login')
def view_profile2(request,pk2):
    user = User.objects.get(id=pk2)
    return render(request, 'profiles/view_profile2.html', {'user' : user})


#viewing all users
@login_required(login_url='/login')
def view_people(request):
    user = User.objects.all()
    return render(request, 'people.html', {'user' : user})
   


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
            return render(request, 'question_answer/post_answer.html', {'ques' : ques, 'answer_form' : answer_form} ) 
    
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
        ques = Question.objects.get(id = pk)
        answer_form = AnswerForm()
        return render(request, 'question_answer/post_answer.html', {'ques' : ques, 'answer_form' : answer_form}) 


#view asked questions
@login_required(login_url='/login')
def view_asked_question(request):
    if request.method == 'GET':
        ques = Question.objects.filter(user = request.user).order_by('-pub_date')
        if ques.exists():    
            return render(request,'question_answer/asked_question.html', {'ques' : ques}) 
        else:
            messages.error(request, 'You have not asked any questions')
            ques = Question.objects.all().order_by('-pub_date')
            return render(request, 'question_answer/question_home.html', {'ques' : ques})
            

#view answers for a question
@login_required(login_url='/login')
def view_answer(request,pk):
    ques = Question.objects.get(id=pk)
    ans = Answer.objects.filter(question_id=pk).order_by('-pub_date')
    if ans.exists():
        return render(request, 'question_answer/view_answer.html', {'ques' : ques, 'ans' : ans})
    else:
        messages.error(request, 'This question has not been answered yet')
        ques = Question.objects.filter(user = request.user).order_by('-pub_date')
        return render(request, 'question_answer/asked_question.html', {'ques' : ques})


#view answered questions
@login_required(login_url='/login')
def view_answered_question(request):
    q = []  
    ans = Answer.objects.filter(user=request.user)
    for a in ans:
        q.append(a.question_id)
    ques = Question.objects.filter(id__in=q).order_by('pub_date')
    if ques.exists():
        return render(request, 'question_answer/answered_question.html', {'ques' : ques})
    else:
        messages.error(request, 'You have not answered any questions')
        ques = Question.objects.all().order_by('-pub_date')
        return render(request, 'question_answer/question_home.html', {'ques' : ques})


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


#to create an event
@login_required(login_url='/login')
@user_passes_test(is_member)
@transaction.atomic
def create_event(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST, request.FILES)
        if event_form.is_valid():
            event = event_form.save(commit = False)
            event.user = request.user
            event.save()
            eve = Event.objects.all().order_by('-date')
            messages.success(request, 'Event Created')
            return render(request, 'events/event_home.html', {'eve' : eve}) 
        else:
            messages.error(request, 'Please correct the error below')
    else:
        event_form = EventForm()
    return render(request, 'events/create_event.html', {'event_form' : event_form}) 


#to register for an event 
@login_required(login_url='/login')
@user_passes_test(is_member)
@transaction.atomic
def register_for_event(request,pk3):
    if request.method == 'GET':
        try:
            chk = EventAttendees.objects.get(user=request.user, event_id=pk3) 
            messages.error(request, 'You have already registered!')
            eve = Event.objects.all().order_by('-date')
            return render(request, 'events/event_home.html', {'eve' : eve})
        except ObjectDoesNotExist:    
            eve_att = EventAttendees(user=request.user, event_id=pk3)
            eve_att.save()
            messages.success(request, 'Registration Successfull')
            eve = Event.objects.all().order_by('-date')
            return render(request, 'events/event_home.html', {'eve' : eve})
    
         

#to upload images for an event
@login_required(login_url='/login')
@user_passes_test(is_member)
@transaction.atomic
def update_event_gallery(request,pk3):
    if request.method == 'POST':
        image_upload_form = EventGalleryForm(request.POST, request.FILES)
        if image_upload_form.is_valid():
            eve_img = image_upload_form.save(commit=False)
            eve_img.user=request.user
            eve_img.event_id=pk3
            eve_img.save()
            eve = Event.objects.filter(user=request.user).order_by('-date')
            messages.success(request, 'Image uploaded successfully')
            return render(request, 'events/my_event.html', {'eve' : eve})
        else:
            messages.error(request, 'Image upload not successfull. Please try again')
    else:
        eve = Event.objects.get(id=pk3)
        image_upload_form = EventGalleryForm()
        return render(request, 'events/upload_event_image.html', {'eve' : eve, 'image_upload_form' : image_upload_form})


#to post a comment in event 
@login_required(login_url='/login')
@user_passes_test(is_member)
@transaction.atomic
def post_comment(request,pk3,pk1):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.event_id = pk3
            comment.save()
            eve = Event.objects.get(id=pk3)
            com = Comment.objects.filter(event_id=pk3).order_by('pub_date')
            gal = EventGallery.objects.filter(event_id=pk3)
            att = EventAttendees.objects.filter(event_id=pk3)
            messages.success(request, 'Comment Posted')
            return render(request, 'events/view_event.html', {'eve' : eve, 'com' : com, 'gal' : gal, 'att' : att})
        else:
            messages.error(request, 'Please correct the error below')
    else:
        comment_form = CommentForm()
        return render(request, 'events/post_comment.html', {'comment_form' : comment_form})


#event homepage
@login_required(login_url='/login')
@user_passes_test(is_member)
def event_home(request):
    eve = Event.objects.all().order_by('-date')
    return render(request, 'events/event_home.html', {'eve' : eve})


#to view user created events
@login_required(login_url='/login')
@user_passes_test(is_member)
def my_event(request):
    eve = Event.objects.filter(user=request.user).order_by('-date')
    return render(request, 'events/my_event.html', {'eve' : eve})


#view event details
@login_required(login_url='/login')
@user_passes_test(is_member)
def view_event(request,pk1):
    eve = Event.objects.get(id=pk1)
    com = Comment.objects.filter(event_id=pk1).order_by('pub_date')
    gal = EventGallery.objects.filter(event_id=pk1)
    att = EventAttendees.objects.filter(event_id=pk1)
    return render(request, 'events/view_event.html', {'eve' : eve, 'com' : com, 'gal' : gal, 'att' : att})


#to delete an event
@login_required(login_url='/login')
@user_passes_test(is_member)
@transaction.atomic
def delete_event(request,pk2):
    eve = Event.objects.get(id=pk2)
    if request.user == eve.user:
        eve.delete()
        messages.success(request, 'Event deleted')
        eve = Event.objects.filter(user=request.user).order_by('-date')
        return render(request, 'events/my_event.html', {'eve' : eve})
    else:
        messages.error(request, 'You are not authorised to perform this operation')
        eve = Event.objects.filter(user=request.user).order_by('-date')
        return render(request, 'events/my_event.html', {'eve' : eve})


#to view registered events
@login_required(login_url='/login')
@user_passes_test(is_member)
def registered_event(request):
    event = []
    eve = EventAttendees.objects.filter(user=request.user)
    if eve.exists():
        for e in eve:
            event.append(e.event_id)
        eve = Event.objects.filter(id__in = event).order_by('-date')
        return render(request, 'events/registered_event.html', {'eve' : eve})
    else:
        messages.error(request, 'You have not registered for any event')
        return redirect('/event')


#to send email to career services department
@login_required(login_url='/login')
def query_to_csd(request):
    if request.method == 'GET':
        email_form = EmailForm()
        return render(request, 'career_services_deptt.html', {'email_form' : email_form})
    
    if request.method == 'POST':
        email_form = EmailForm(request.POST)
        if email_form.is_valid():
            subject = email_form.cleaned_data['subject']
            body = email_form.cleaned_data['body']
            send_mail(
                        subject,
                        body,
                        request.user.email,
                        ['careerservices@example.com'],
                        fail_silently=False,
                    )
            messages.success(request, 'Mail sent successfully')
            return redirect('/careerservicesdepartment')
        else:
            messages.error(request, 'Please correct the error below')
    else:
        email_form = EmailForm()
        return render(request, 'career_services_deptt.html', {'email_form' : email_form})

   



            



    