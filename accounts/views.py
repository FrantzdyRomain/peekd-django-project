# Create your views here
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from accounts.forms import RegistrationForm, UserUpdateAvatarForm, LoginForm, UserProfileForm, UserProfilePhotoForm
from accounts.models import UserProfile, UserProfilePhoto
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from PIL import Image as PImage
from os.path import join as pjoin

LOGIN_URL = '/login/'
def home(request):
	context =RequestContext(request)
	return render_to_response('home.html', {}, context_instance=context)


def signup(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/profile/')
	if request.method=="POST":
		form = RegistrationForm(request.POST) #take the form and fill it with what has been POST'ed
		if form.is_valid():
			user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
			user.save()
			#possibly might need these lines of code for edit profile
			#uprofile = user.get_profile() #remember its set in settings
			#uprofile.avatar = form.cleaned_data['avatar']
			#uprofile.name = form.cleaned_data['name']
			#uprofile.website = form.cleaned_data['website']
			#uprofile.bio = form.cleaned_data['bio']
			#uprofile.save() #save our UserProfile object, which contains our User extra data or subclass.
			"""create UserProfile object manually. uncomment when done in editprofile view"""
#			userprofile = UserProfile(user=user, avatar=form.cleaned_data['avatar'],name=form.cleaned_data['name'],)
#                       userprofile.save()
			return HttpResponseRedirect('/a/profile/') # because we have to return HTTP response else error is thrown
		else: #in case form isnt valid show the form again. this time possibly with errors and such
			return render_to_response('accounts/register.html', {'form':form}, context_instance=RequestContext(request))

			
			
			
	else:
		form = RegistrationForm()
		context = {'form':form}
		return render_to_response('accounts/register.html', context, context_instance=RequestContext(request))
    
#what others see
def view_profile(request, username=None):
    #see if user is us
    
    if username is None or username == request.user.username:
        userobj = request.user.get_profile
        my_profile = True
    else:
        userobj = get_object_or_404(User, username=username)
        my_profile = False
    
    try:
        user_profile = UserProfile.objects.filter(user=userobj).get()
    except UserProfile.DoesNotExist:
            raise Http404
    

    #do Query for Items later :)
    
    return render_to_response('accounts/profile.html', {'my_profile':my_profile,'userp':userobj,'userprofile':user_profile,}, context_instance=RequestContext(request))

#What user sees        
@login_required(login_url=LOGIN_URL)
def profile(request):
	if not request.user.is_authenticated():
		HttpResponseRedirect('/login')
        
        userprofile = request.user.get_profile #for User properties
            #userprofile_w_image = get_object_or_404(UserProfile, pk=request.user)
            #pic = get_object_or_404(UserProfilePhoto, user=request.user)
            #userpic = UserProfile.objects.get(user=request.user)
        
            
	context = {'userprofile': userprofile, }
    
    
	return render_to_response('accounts/my_profile.html', context, context_instance=RequestContext(request))

#Need to refactor this
@login_required(login_url=LOGIN_URL)
def update_profile(request):
    
    if request.user.is_authenticated():

        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.name = profile.name or request.user.first_name

        form = UserProfileForm(request.POST or None, instance=profile)

        

        if request.POST:
            if form.is_valid():
                form.save()
            return HttpResponseRedirect('/')
    else:
        form = None
        #messages.add_message(request, messages.INFO, 'You may sign in to update your profile.')
    return render_to_response("accounts/profile_edit.html",
        {'form': form,},context_instance=RequestContext(request))

""" #Didnt quite work 
@login_required(login_url=LOGIN_URL)
def profile_edit(request):
	if request.method == 'POST':
            form = UserProfileForm(request.POST)
            if form.is_valid():
                user = request.user
                profile = UserProfile.objects.create(user, form.cleaned_data['name'], form.cleaned_data['website'], form.cleaned_data['bio'] )
            return HttpResponseRedirect('/profile/')
	else:
            #userp = UserProfile.objects.get(user=request.user)
            #initial_data = {'name':userp.name, 'website':userp.website, 'bio':userp.bio,}
            form = UserProfileForm()
            return render_to_response('accounts/profile_edit.html', {'form':form}, context_instance=RequestContext(request)) 
"""
@login_required(login_url=LOGIN_URL)
def upload_profile_photo(request):
    if request.method == 'POST':
        # Get data from form
        #form = UserProfilePhotoForm(request.POST,request.FILES)
        user = UserProfile.objects.get(user=request.user) # we need user object as instance to know which to save it as :)
        form = UserUpdateAvatarForm(request.POST,request.FILES, instance=user)
        
        # If the form is valid, create a new object and redirect to it.
        if form.is_valid():
            form.save()
            
            
            
        #messages.success(request, 'Profile pic updated!')
            return HttpResponseRedirect('/profile/')
    
        #else:
                #for debugging purposes; Put this on the actual HTML bro
                #print form.errors
    else:
        # Fill in the field with the current user by default
        form = UserUpdateAvatarForm(initial={'user': request.user})
    # Render our template
    return render_to_response('accounts/upload_profile.html',
        {'form': form},
        context_instance=RequestContext(request))
"""        
@login_required
def upload_profile_image(request):
    if request.method == 'POST':
        form = UserProfilePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            UserProfilePhoto.objects.save_from_info(request.user, form.cleaned_data['image'])
            return HttpResponseRedirect('/profile/')
    else:
        form = UserProfilePhotoForm()

    return render_to_response('accounts/upload_profile.html',
        {'form': form},
        context_instance=RequestContext(request))
"""
def signin(request):
	error = []
	if request.user.is_authenticated():
		return HttpResponseRedirect('/profile/')
	if request.method =="POST":
		form = LoginForm(request.POST) #pass the form the request.post values
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			userprofile = authenticate(username=username, password=password) #if passwords are valid
			if userprofile is not None: #if all went well
				if userprofile.is_active:
					login(request, userprofile) #login the request as this particular user
					return HttpResponseRedirect('/a/profile/')
				else:
					errors.append('User %s is disabled' % userprofile.username)
			else:
				error.append('Username and password combination did not match.')
				return render_to_response('accounts/login.html', {'form':form, 'error':error}, context_instance=RequestContext(request)) #wrong credentials, go back and look at errors
		else:
			return render_to_response('accounts/login.html', {'form':form}, context_instance=RequestContext(request))
				
			
			
			
	else:
		""" nothing has been done, show the form"""
		form = LoginForm()
		context = {'form': form, 'errors':error,}
		return render_to_response('accounts/login.html', context, context_instance=RequestContext(request))
		

def signout(request):
	logout(request)
	return HttpResponseRedirect('/')
	
	






























