import logging

from django.db.models.loading import get_model
from django.db import IntegrityError
from django.utils.translation import ugettext as _

from glue.misc import Epoxy, API_EXCEPTION_FORMERRORS, API_EXCEPTION_INTEGRITY, API_EXCEPTION_DOESNOTEXIST
from glue.models import Page, Pin
from glue.forms import AddPageForm, AddPinForm, EditPinForm


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
		form = AddPageForm( request.REQUEST )
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

def pins( request ):
	response = Epoxy( request )
	if response.method =='POST':
		form = AddPinForm( request.REQUEST )
		if not form.is_valid():
			return response.throw_error( error=form.errors, code=API_EXCEPTION_FORMERRORS).json()

		if len(form.cleaned_data['page_slug']) > 0:
			# attacch new pin to a selected page (both languages)
			response.add('page_slug',form.cleaned_data['page_slug'])
			
			try:
				page_en = Page.objects.get( slug=form.cleaned_data['page_slug'],language='EN')
				page_fr = Page.objects.get( slug=form.cleaned_data['page_slug'],language='FR')
			except Page.DoesNotExist:
				return response.throw_error( error=_("selected page does not exists"), code=API_EXCEPTION_FORMERRORS).json()

			response.add('page', [ page_en.json(), page_fr.json() ] )

		if len(form.cleaned_data['parent_pin_slug']) > 0:
			# attacch new pin to a selected pin (pin children, usually displayed on the right side, both languages)
			response.add('parent_pin_slug',form.cleaned_data['parent_pin_slug'])
			
			try:
				pin_en = Pin.objects.get( slug=form.cleaned_data['parent_pin_slug'],language='EN')
				pin_fr = Pin.objects.get( slug=form.cleaned_data['parent_pin_slug'],language='FR')
			except Pin.DoesNotExist, e:
				return response.throw_error( error=_("selected pin does not exists. Exception: %s" % e), code=API_EXCEPTION_FORMERRORS).json()

			response.add('pin', [ pin_en.json(), pin_fr.json() ] )

		#return response.queryset( Pin.objects.filter() ).json()

		try:
			p_en = Pin( title=form.cleaned_data['title_en'], language='EN', slug=form.cleaned_data['slug'])
			p_fr = Pin( title=form.cleaned_data['title_fr'], language='FR', slug=form.cleaned_data['slug'])
			
			if len(form.cleaned_data['parent_pin_slug']) > 0:
				p_en.parent = pin_en
				p_fr.parent = pin_fr

			
			p_en.save()
			p_fr.save() 
		except IntegrityError, e:
			return response.throw_error( error={'slug':"Exception %s" % e}, code=API_EXCEPTION_INTEGRITY).json()
		
		if len(form.cleaned_data['page_slug']) > 0:
			page_en.pins.add( p_en )
			page_en.save()
			page_fr.pins.add( p_fr )
			page_fr.save()

		response.add('object',[ p_en.json(), p_fr.json() ])

	return response.queryset( Pin.objects.filter() ).json()


def pin( request, pin_id ):
	# @todo: check pin permissions
	response = Epoxy( request )
	if response.method == 'POST':
		form = EditPinForm( request.REQUEST )
		if form.is_valid():
			try:
				pin = Pin.objects.get( id=pin_id )
				pin.title = form.cleaned_data['title']
				pin.abstract = form.cleaned_data['abstract']
				pin.content = form.cleaned_data['content']
				pin.save()
			except Pin.DoesNotExist, e:
				return response.throw_error( error="%s" % e, code=API_EXCEPTION_DOESNOTEXIST).json()
		else:
			return response.throw_error( error=form.errors, code=API_EXCEPTION_FORMERRORS).json()

	return response.single( Pin, {'id':pin_id} ).json()

def pin_by_slug( request, pin_slug, pin_language ):
	return Epoxy( request ).single( Pin, {'slug':pin_slug,'language':pin_language} ).json()