# Create your views here.
#IDea of views from https://github.com/bartTC/django-paste/blob/master/dpaste/views.py
"""
Functions:
    Create
    Edit
    View
        --ALL:by tag[categories], location,
        --One
"""
from items.models import Item
from items.forms import * #for now
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils import simplejson
from items.forms import ItemCreateForm, ItemUpdateForm
#list of all Items
def item_list():
    pass
    
#idea here https://github.com/django-de/djangosnippets.org/blob/master/cab/views/snippets.py def mathces_tag
#query of Item(s) by tag
def items_by_tag():
    pass

#query of Item(s) by location
def items_by_location():
    pass

def snippet_new(request, template_name='items/create_item.html'):

    if request.method == "POST":
        form = ItemCreateForm(data=request.POST)
        if form.is_valid():
            request, new_item = form.save()
            return HttpResponseRedirect(new_item.get_absolute_url())
    else:
        form = ItemCreateForm()

    template_context = {
        'form': form,
    }

    return render_to_response(
        template_name,
        template_context,
        RequestContext(request)
    )
        
#create/update ITem. https://github.com/humanfromearth/snippify/blob/master/snippets/views.py
def item_process(request, pk=None):
    if pk is not None: #update
        item = get_object_or_404(Item, pk=pk)
        form = ItemUpdateForm(instance=Item)
         #check for ownership 
        if request.user != Item.author and not request.user.is_staff:
            request.session['flash'] = ['Access denied', 'error']
            return HttpResponseRedirect('/accounts/profile/')
        
        if 'delete' in request.POST:
            item.delete()
            request.session['flash'] = ['#%s deleted successfuly' % pk,
                                        'sucess']
            return HttpResponseRedirect('/accounts/profile/')
    else: #create
        item = None
        form = ItemCreateForm()
    if request.method == 'POST':
        form = ItemCreateForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            messages.info(request, 'Your item has been saved')
            return HttpResponseRedirect(item.get_absolute_url())
    else:
        form = ItemCreateForm(instance=item)
        
    return render_to_response('items/create_new.html',
        {'form': form}, context_instance=RequestContext(request))
            
            
	   
def item_details(request, item_id, template_name='items/item_details.html'):
    item = get_object_or_404(Item, secret_id=item_id)

    

    new_item_initial = {
        'content': item.description,
        
    }

    if request.method == "POST":
        form = ItemCreateForm(data=request.POST, initial=new_item_initial)
        if form.is_valid():
            request, new_item = form.save()
            return HttpResponseRedirect(new_item.get_absolute_url())
    else:
         form = ItemCreateForm(initial=new_item_initial)

    template_context = {
        'form':  form,
        'item': item,
        
    }

    response = render_to_response(
        template_name,
        template_context,
        context_instance=RequestContext(request)
    )
    return response

    
    
    #render_to_response('items/item_details.html', {'item':item}, context_instance=RequestContext(request))
    
def item_delete():
    pass
    
