import re
from django.contrib.auth.models import User, Group
from core.models import Profile, Testimonial, Question, Answer, Event, EventGallery, Comment
from django.core.exceptions import ObjectDoesNotExist
from django import forms

class RegistrationForm(forms.Form):
    CHOICES = [( group.name, group.name ) for group in Group.objects.all()]
    
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password',
                          widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password (Again)',
                        widget=forms.PasswordInput())
    groupname = forms.ChoiceField(choices=CHOICES,widget = forms.widgets.RadioSelect())
    
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
               return password2        
            raise forms.ValidationError('Passwords do not match.')
                

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('pic','bio','gender', 'city', 'batch', 'website','twitter','linkedin', 'organization')

class DeleteUserForm(forms.Form):
    username = forms.CharField()

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ('content',) 

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'description')

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('answer',)

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'icon', 'date', 'time', 'venue', 'description') 

class EventGalleryForm(forms.ModelForm):
    class Meta:
        model = EventGallery
        fields = ('pic',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class EmailForm(forms.Form):
    subject = forms.CharField(max_length=50)
    body = forms.CharField(widget = forms.Textarea())








    


