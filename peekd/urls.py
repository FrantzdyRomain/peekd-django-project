from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from accounts import views as accounts
from profileimages import views as image
from django.conf import settings
from django.conf.urls.defaults import *
from accounts.api import UserProfileResource, UserResource
from items.api import ItemResource
from tastypie.api import Api
admin.autodiscover()
#user_resource = UserProfileResource()
v1_api = Api(api_name='v1')
v1_api.register(UserProfileResource())
v1_api.register(ItemResource())
v1_api.register(UserResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'peekd.views.home', name='home'),
    # url(r'^peekd/', include('peekd.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^$', accounts.home),
     url(r'signup/$', accounts.signup),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^login/$', accounts.signin),
     url(r'^logout/$', accounts.signout),
     #url(r'^profile/$', accounts.view_profile),
     url(r'^profile/edit/$', accounts.update_profile),
     url(r'^profile/upload/$', accounts.upload_profile_photo),
     url(r'^a/', include('accounts.urls')),
     #url(r'^profile/up/$', image.upload_profile_image), #for debugging a method
    #These set of urls are for password resets, handled by django
    #you need to cp the files from registration in Django
    #cp -r /path/to/django/contrib/admin/templates/registration/ /path/to/django/root/templates/
     url('^resetpassword/sentpassworddone/$', 'django.contrib.auth.views.password_reset_done'),
     url('^passwordreset/$', 'django.contrib.auth.views.password_reset'),
     url('^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
     url('^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    #for Items app
    url(r'^i/', include('items.urls')),
    #API URLS
    url(r'^api/', include(v1_api.urls)),
    
)

#in production you want apache to server the media files young sir,
if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )
