from django.conf.urls.defaults import *

from accounts import views as accounts

urlpatterns = patterns('',
    url(r'^login/$', accounts.signin),
    url(r'^logout/$', accounts.signout),
    url(r'^profile/$', accounts.profile, name="view_profile"), #What user sees
    url(r'^profile/edit/$', accounts.update_profile),
    url(r'^profile/upload/$', accounts.upload_profile_photo),
    url(r'^(\w+)/', accounts.view_profile),
)