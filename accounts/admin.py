from django.contrib import admin
from accounts.models import UserProfile
from accounts.models import UserProfilePhoto

class UserProfilePhotoAdmin(admin.ModelAdmin):
    list_display = ['user']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserProfilePhoto, UserProfilePhotoAdmin)
