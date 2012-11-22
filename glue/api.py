import logging

from django.db.models.loading import get_model
from django.db import IntegrityError
from glue.misc import Epoxy, API_EXCEPTION_FORMERRORS, API_EXCEPTION_INTEGRITY
from glue.models import Page, Pin
from glue.forms import AddPageForm

logger = logging.getLogger(__name__)

def index(request):
	# logger.info("Welcome to GLUEBOX api")
	return Epoxy( request ).json()

def manage_objects( request, model_name ):
	# logger.info("Welcome to GLUEBOX api")
	return Epoxy( request ).queryset( get_model( "glue", model_name ).objects.filter(), model_name=model_name ).json()

def manage_single_object( request, model_name, pk ):
	# logger.info("Welcome to GLUEBOX api")
	return Epoxy( request ).single( Page, {'pk':pk} ).json()

def pages(request):
	# logger.info("Welcome to GLUEBOX api")
	response = Epoxy( request )
	if response.method =='POST':
		form = AddPageForm( response.request )
		if not form.is_valid():
			return response.throw_error( error=form.errors, code=API_EXCEPTION_FORMERRORS).json()
		try:
			p_en = Page( title=form.cleaned_data['title_en'], language='EN', slug=form.cleaned_data['slug'])
			p_en.save()

			p_fr = Page( title=form.cleaned_data['title_fr'], language='FR', slug=form.cleaned_data['slug'])
			p_fr.save() 
		except IntegrityError, e:
			return response.throw_error( error="%s" % e, code=API_EXCEPTION_INTEGRITY).json()

		response.add('object',[ p_en.json(), p_fr.json() ])

	return response.queryset( Page.objects.filter() ).json()
	

def page( request, page_id ):
	return Epoxy( request ).single( Page, {'id':page_id} ).json()

def page_by_slug( request, page_slug, page_language ):
	return Epoxy( request ).single( Page, {'slug':page_slug,'language':page_language} ).json()

def pin( request, page_id ):
	return Epoxy( request ).single( Pin, {'id':pin_id} ).json()

def pin_by_slug( request, pin_slug, pin_language ):
	return Epoxy( request ).single( Pin, {'slug':pin_slug,'language':pin_language} ).json()