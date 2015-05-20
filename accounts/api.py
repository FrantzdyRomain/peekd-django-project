from tastypie.resources import ModelResource,  ALL, ALL_WITH_RELATIONS
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from accounts.models import UserProfile

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        list_allowed_methods = ['get', 'post','put']
        authorization= Authorization() #not for production
        filtering = {
            'username': ALL,
        }
class UserProfileResource(ModelResource):
    class Meta:
        #debugging
        queryset = UserProfile.objects.all() #get all Objects os U..Profile
        resource_name = 'userprofiles' #used after api in url
        #If your users are logged into the site & you want Javascript to be able to access the API (assuming jQuery)
        #see here http://django-tastypie.readthedocs.org/en/latest/cookbook.html
        #authentication = SessionAuthentication() #don need yet
        filtering = {
            'username': ALL,
        }
        