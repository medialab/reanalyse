from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.conf import settings
from glue.models import Pin
from outside.models import Enquiry
from glue.misc import Epoxy
from reanalyse.reanalyseapp.models import Enquete


#
#    API CUSTOM DECORATORS
#    =====================
#
def is_editor(user):
	if user:
		return user.groups.filter(name='CONTENT EDITOR').count() != 0
	return False

def enquiries( request ):
	response = Epoxy( request )
	response.queryset( Enquiry.objects )
	return response.json()

def enquiry( request, enquiry_id ):
	response = Epoxy( request )
	# check user permissions
	return response.single( Enquiry, {'pk':enquiry_id} ).json()

#
#    API AUTH VIEWS
#    ==============
#
API_ACCESS_DENIED_URL = "/elipss/panelmanager/api/access-restricted"


def enquete_data( request, enquete_id ):
	data = {}
	return render_to_response('outside/enquete_data.json', RequestContext(request, data ) )