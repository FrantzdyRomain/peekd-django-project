from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from photologue.models import ImageModel


class UserProfile(models.Model):
	#create our own path in media
	def upload_path(instance, filename):
		import time
		import os
		from django.template.defaultfilters import slugify 
		
		extend_name = instance.user.name
		path = os.path.join('', slugify(instance.name), filename)
		return path
	#instance.user.user is the User object, #instance.user is UserProfile
	def upload_to(instance, filename):
		return 'avatars/%s/%s' % (instance.user.username, filename)

	user = models.ForeignKey(User, unique=True)
	avatar = models.ImageField(upload_to=upload_to, blank=True)
	name = models.CharField(max_length=255, blank=True)
	website = models.URLField(blank=True)
	bio = models.TextField(blank=True)

	def __unicode__(self):
		return self.name
	#get the url for avatar for user, idea "stolen" from django-userena
	def get_avatar_url(self):
		if self.avatar:
			return self.avatar.url
#have the profile created automatically when referenced, with the added bonus 
#of being able to reference a users profile as user.profile instead of user.get_profile()
#hits db everytime though :(
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
 


       
#lets take a different approach towards profile photos, we will use django-photologue
#not using this to store UserProfile Photos
class UserProfilePhoto(models.Model):
    def upload_path(instance, filename):
        import time
        import os
        from django.template.defaultfilters import slugify 
        
        extend_name = instance.user.name
        path = os.path.join('', slugify(instance.name), filename)
        return path
    #instance.user.user is the User object, #instance.user is UserProfile
    def upload_to(instance, filename):
        return 'avatars/%s/%s' % (instance.user.username, filename)
    #user = models.OneToOneField(User, primary_key=True)
    user = models.ForeignKey(User, unique=True)
    avatars = models.ImageField(upload_to=upload_to, blank=True)
    
    def get_avatars_url(self):
        if self.avatars:
            return self.avatars.url
        
   

#def create_user_callback(sender, instance, **kwargs):
#	userprofile, new = UserProfile.objects.get_or_create(user=instance)
#post_save.connect(create_user_callback, User)	


