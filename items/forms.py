from django import forms
from django.forms import ModelForm
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from items.models import Item
import datetime

class ItemCreateForm(forms.ModelForm):
    
    class Meta:
        model = Item
        exclude = ('owner','secret_id',)
        
        
        
class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('owner','secret_id',)


    
