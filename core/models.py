import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime,date


# Create your models here.

#NOTE : delete all users from admin before making any changes to model

#to save user dp in media/users/user_id/filename
def get_image_path(instance, filename):
    return os.path.join('users', str(instance.id), filename)

#dummy just ignore
def get_event_image_path(instance, filename):
    return os.path.join('events', str(instance.id), filename)


class Profile(models.Model):
    
    BATCH_CHOICES = (
        ('NA', 'Not Applicable'),
        ('1998','1998'),
        ('1999','1999'),
        ('2000','2000'),
        ('2001','2001'),
        ('2002','2002'),
        ('2003','2003'),
        ('2004','2004'),
        ('2005','2005'),
        ('2006','2006'),
        ('2007','2007'),
        ('2008','2008'),
        ('2009','2009'),
        ('2010','2010'),
        ('2011','2011'),
        ('2012','2012'),
        ('2013','2013'),
        ('2014','2014'),
        ('2015','2015'),
        ('2016','2016'),
        )

    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        )

    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to=get_image_path, default = os.path.join('users', 'default_avatar.jpg'))
    bio = models.TextField(max_length=500, default = '', blank=True)
    gender = models.CharField(max_length=1, choices = GENDER_CHOICES, blank = True)
    city = models.CharField(max_length=30,default = '', blank=True)
    batch = models.CharField(max_length=4, choices = BATCH_CHOICES, blank=True)
    website = models.URLField(default='', blank=True)
    twitter = models.URLField(default='', blank=True)
    linkedin = models.URLField(default='', blank=True)
    organization = models.CharField(max_length=100, default='', blank=True)

#so that profile is created and saved each time a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Testimonial(models.Model):
    user = models.OneToOneField(User, null = True, on_delete = models.CASCADE)
    content = models.TextField(max_length = 1000, default = '', blank =  True)
    pub_date = models.DateTimeField(auto_now_add = True)


class Question(models.Model):
    user = models.ForeignKey(User, null = True, on_delete = models.CASCADE)
    title = models.TextField(max_length = 200)
    description = models.TextField(max_length = 500, default = '', blank = True)
    pub_date = models.DateTimeField(auto_now_add = True)


class Answer(models.Model):
    user = models.ForeignKey(User, null = True, on_delete = models.CASCADE)
    question = models.ForeignKey(Question, null = True, on_delete = models.CASCADE)
    answer = models.TextField(max_length = 1000)
    pub_date = models.DateTimeField(auto_now_add = True)
 

class Event(models.Model):
    user = models.ForeignKey(User, null = True, on_delete = models.CASCADE)
    title = models.TextField(max_length = 50)
    date = models.DateField(default = date.today)
    time = models.TimeField(default = datetime.now)
    venue = models.TextField(max_length = 50)
    description = models.TextField(max_length = 500, blank = True, default = '')
    icon = models.ImageField(upload_to=get_image_path, default = os.path.join('users', 'default_icon.jpg'))
    pub_date = models.DateTimeField(auto_now_add = True)
 

class EventAttendees(models.Model):
    user = models.ForeignKey(User, null = True, on_delete = models.CASCADE)
    event = models.ForeignKey(Event, null = True, on_delete = models.CASCADE)


class EventGallery(models.Model):
    user = models.ForeignKey(User, null = True, on_delete = models.CASCADE)
    event = models.ForeignKey(Event, null = True, on_delete = models.CASCADE)
    pic = models.ImageField(upload_to = get_image_path, blank = True, null = True)
    pub_date = models.DateTimeField(auto_now_add = True)


class Comment(models.Model):
    user = models.ForeignKey(User, null = True, on_delete = models.CASCADE)
    event = models.ForeignKey(Event, null = True, on_delete = models.CASCADE)
    content = models.TextField(max_length = 200)
    pub_date = models.DateTimeField(auto_now_add = True)
   
