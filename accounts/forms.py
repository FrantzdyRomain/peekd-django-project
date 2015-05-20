from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from accounts.models import UserProfile, UserProfilePhoto
from PIL import Image

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
    
class RegistrationForm(ModelForm):
	username = forms.CharField(label=(u'Username'))
	email	 = forms.CharField(label=(u'Email'))
	password = forms.CharField(label=(u'Password'),widget=forms.PasswordInput(render_value=False))
	password1 = forms.CharField(label=(u'Verify Password'),widget=forms.PasswordInput(render_value=False))
	
	class Meta:
		model = UserProfile #create form out of UserProfile model but exclude some things
		exclude = ('user','avatar','website','bio','name',)

	#clean methods for forms in views
	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			User.objects.get(username=username)

		except User.DoesNotExist:
			return username
		raise forms.ValidationError("We're sorry. That username is taken.Try another")

        #this method has access to all the vars in the form :)
	def clean_password1(self):
		password = self.cleaned_data.get('password','')
		password1 = self.cleaned_data.get('password1','')
		if password != password1:
			raise forms.ValidationError("Passwords did not match")
		return password1
    
    

class UserProfileForm(ModelForm):
    """
    name = forms.CharField(label=(u'Name'))
    website	 = forms.URLField(label=(u'Website'))
    bio = forms.CharField(label=(u'Bio'),widget=forms.Textarea)
    """
    class Meta:
        model = UserProfile
        exclude = ('user','avatar')
class UserUpdateAvatarForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user','website','bio','name')
    def clean_image(self):
        if 'image' in self.cleaned_data:
            image = self.cleaned_data['image']
            if len(image['content']) > settings.PROFILE_IMAGE_MAX_SIZE * 1024:
                raise forms.ValidationError('The image you are trying to upload is larger than %d Kb.' % settings.PROFILE_IMAGE_MAX_SIZE)
            try:
                data = Image.open(StringIO.StringIO(image['content']))
                data.verify()
            except:
                raise forms.ValidationError('The file you are uploading does not seem to be an image.')
            return image
        

#form with all fields of DB including avatar. May be used.
class UserUpdateForm:
    class Meta:
        model= UserProfile
class UserProfilePhotoForm(ModelForm):
    class Meta:
        model = UserProfilePhoto
        exclude = ('user',)
        
    def clean_image(self):
        if 'image' in self.cleaned_data:
            image = self.cleaned_data['image']
            if len(image['content']) > settings.PROFILE_IMAGE_MAX_SIZE * 1024:
                raise forms.ValidationError('The image you are trying to upload is larger than %d Kb.' % settings.PROFILE_IMAGE_MAX_SIZE)
            try:
                data = Image.open(StringIO.StringIO(image['content']))
                data.verify()
            except:
                raise forms.ValidationError('The file you are uploading does not seem to be an image.')
            return image
    
class LoginForm(forms.Form):
    username    = forms.CharField(label=(u'Username'))
    password    = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))

class AppRegistrationForm(ModelForm):
	pass
"""
class UserProfilePhotoForm(ModelForm):
    class Meta:
        model = UserProfilePhoto
        exclude = ('user',)
"""	

