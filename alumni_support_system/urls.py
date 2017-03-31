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
    url(r'^profile/editprofile/$', core_views.update_profile, name='update_profile'),
    url(r'^settings/$', core_views.settings, name='settings'), 
    url(r'^settings/changepassword/$', core_views.change_password, name='change_password'),
    url(r'^settings/deleteuser/$', core_views.delete_user, name='delete_user'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
     