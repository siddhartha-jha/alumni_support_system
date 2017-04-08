"""
Definition of urls for alumni_support_system.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url
from django.contrib.auth import views
from core import views as core_views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', alumni_support_system.views.home, name='home'),
    # url(r'^alumni_support_system/', include('alumni_support_system.alumni_support_system.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', core_views.home, name = 'home'),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout, {'next_page' : '/login'}),
    url(r'^login/register/$', core_views.register_page),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    
    url(r'^profile/$', core_views.view_profile, name = 'view_profile'),
    url(r'^profile/editprofile/$', core_views.update_profile, name='edit_profile'),
    url(r'^profile/writetestimonial/$', core_views.write_testimonial, name='write_testimonial'),
    url(r'^profile/viewtestimonial/$', core_views.view_testimonial, name='view_testimonial'),
    url(r'^profile/deletetestimonial/$', core_views.delete_testimonial, name='delete_testimonial'),
    
    url(r'^settings/$', core_views.settings, name='settings'), 
    url(r'^settings/changepassword/$', core_views.change_password, name='change_password'),
    url(r'^settings/deleteuser/$', core_views.delete_user, name='delete_user'),
    
    url(r'^questionanswer/$', core_views.question_answer, name='question_answer_home'),
    url(r'^questionasnwer/askquestion/$', core_views.post_question, name='post_question'),
    url(r'^questionanswer/answerquestion/(?P<pk>\d+)/$', core_views.post_answer, name='post_answer'),
    url(r'^questionanswer/viewanswers/(?P<pk>\d+)/$', core_views.view_answer, name='view_answer'),
    url(r'^questionanswer/viewaskedquestions/$', core_views.view_asked_question, name='view_asked_question'),
    url(r'^questionanswer/viewaskedquestions/viewanswers/(?P<pk>\d+)/$', core_views.view_answer, name='view_answer2'),
    url(r'^questionanswer/viewansweredquestions/$', core_views.view_answered_question, name='view_answered_question'),
    url(r'^questionanswer/viewansweredquestions/viewanswers/(?P<pk>\d+)/$', core_views.view_answer, name='view_answer3'),
    url(r'^questionanswer/viewunansweredquestions/$', core_views.view_unanswered_question, name = 'view_unanswered_question'),
    url(r'^questionanswer/viewaskedquestions/deletequestion/(?P<pk2>\d+)/$', core_views.delete_question, name = 'delete_question'),
    #url(r'^questionanswer/viewanswers/(?P<pk>\d+)/deleteanswer/(?P<pk2>\d+)/$', core_views.delete_answer, name='delete_answer'),
    #url(r'^questionanswer/viewaskedquestions/viewanswers/(?P<pk>\d+)/deleteanswer/(?P<pk2>\d+)/$', core_views.delete_answer, name='delete_answer'),
    #url(r'^questionanswer/viewansweredquestions/viewanswers/(?P<pk>\d+)/deleteanswer/(?P<pk2>\d+)/$', core_views.delete_answer, name='delete_answer'),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
     