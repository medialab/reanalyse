from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.conf import settings
from glue.models import Pin
from outside.models import Enquiry
from outside.forms import AddEnquiryForm
from glue.misc import Epoxy, API_EXCEPTION_FORMERRORS, API_EXCEPTION_INTEGRITY
from django.db import IntegrityError
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
	if response.method =='POST':
		form = AddEnquiryForm( request.REQUEST )
		if not form.is_valid():
			return response.throw_error( error=form.errors, code=API_EXCEPTION_FORMERRORS).json()


		try:
			enquete = Enquete.objects.get(id=form.cleaned_data['enquete'])

			enquiry_en = Enquiry(
				title=form.cleaned_data['title_en'], language='EN', slug=form.cleaned_data['slug'], enquete = enquete
			)

			enquiry_fr = Enquiry(
				title=form.cleaned_data['title_fr'], language='FR', slug=form.cleaned_data['slug'], enquete = enquete
			)

			enquiry_en.save()
			enquiry_fr.save()

		#try:
			#e_en = Page( title=form.cleaned_data['title_en'], language='EN', slug=form.cleaned_data['slug'])
			#e_en.save()

			#p_fr = Page( title=form.cleaned_data['title_fr'], language='FR', slug=form.cleaned_data['slug'])
			#p_fr.save() 
		except IntegrityError, e:
			return response.throw_error( error="%s" % e, code=API_EXCEPTION_INTEGRITY).json()

		# response.add('object',[ p_en.json(), p_fr.json() ])


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