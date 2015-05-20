from tastypie.resources import ModelResource,  ALL, ALL_WITH_RELATIONS
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from items.models import Item
from accounts.api import UserProfileResource

class ItemResource(ModelResource):
    user = fields.ForeignKey(UserProfileResource, 'user', null=True) #give it null val so we dont get errirs
    class Meta:
        queryset = Item.objects.all()
        resource_name = 'items'
        list_allowed_methods = ['get', 'post','put']
        authorization= Authorization() #not good fpr production
        #If your users are logged into the site & you want Javascript to be able to access the API (assuming jQuery)
        #see here http://django-tastypie.readthedocs.org/en/latest/cookbook.html
        #authentication = SessionAuthentication() #don need yet
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }
        
        

        