from datetime import datetime
from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
import random #for creating nice random urls
from django.utils.translation import ugettext_lazy as _

#idea taken from https://github.com/bartTC/django-paste/blob/master/dpaste/models.py
t = 'abcdefghijkmnopqrstuvwwxyzABCDEFGHIJKLOMNOPQRSTUVWXYZ1234567890'
def generate_secret_url(length=4):
    return ''.join([random.choice(t) for i in range(length)]) #for whatever length is set to create a random choice of what is contained in T variable

"""
#debugging
>>>import random
>>>t = 'abcdefghijkmnopqrstuvwwxyzABCDEFGHIJKLOMNOPQRSTUVWXYZ1234567890'
>>>length=5
>>>for i in range(length):
...     print random.choice(t)
"""
#TODO
"""
Tagging --for tagging items. Ie: Cars, appliances, books, etc..Basically categories
Location --City and State.
    --Use django city app for that.
"""
class Item(models.Model):
    def upload_to(instance, filename):
		return 'items/%s/%s' % (instance.owner, filename)

    owner = models.ForeignKey(User,blank=True, null=True) #doesnt need an owner now,
    secret_id = models.CharField(_(u'Secret ID'), max_length=4, blank=True)
    name = models.CharField(_(u'Name'), max_length=120, blank=True)
    description = models.TextField(_(u'Description'),max_length=120,blank=True)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    image1 = models.ImageField(upload_to=upload_to, blank=True, null=True)
    image2 = models.ImageField(upload_to=upload_to, blank=True, null=True)
    price = models.DecimalField(max_digits=8 ,decimal_places=4, blank=True)
    #add later location
    created_date = models.DateTimeField(default = datetime.now())
    
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['-created_date'] #date in ascending order
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.secret_id = generate_secret_url()
        super(Item, self).save(*args, **kwargs)
        
    def get_image_url(self):
        if self.image:
            return self.image.url
    @permalink
    def get_absolute_url(self):
        return ('item_details', (self.secret_id,))
