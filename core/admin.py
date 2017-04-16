from django.contrib import admin
from .models import Profile, Testimonial, Question, Answer, Event, EventAttendees, EventGallery, Comment
# Register your models here.

admin.site.register(Profile)
admin.site.register(Testimonial)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Event)
admin.site.register(EventAttendees)
admin.site.register(EventGallery)
admin.site.register(Comment)

