import logging, os, mimetypes
import datetime as dt

from django.conf import settings
from django.db.models.loading import get_model
from django.db import IntegrityError
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

from glue.misc import Epoxy, API_EXCEPTION_FORMERRORS, API_EXCEPTION_INTEGRITY, API_EXCEPTION_DOESNOTEXIST, API_EXCEPTION_OSERROR
from glue.models import Page, Pin
from glue.forms import AddPageForm, AddPinForm, EditPinForm, UploadPinForm


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

	elif response.method=='DELETE':
		try:
			Pin.objects.filter(slug=Pin.objects.get(id=pin_id).slug).delete()
		except Pin.DoesNotExist, e:
			return response.throw_error( error="%s" % e, code=API_EXCEPTION_DOESNOTEXIST).json()
		return response.json()
	
	return response.single( Pin, {'id':pin_id} ).json()

def pin_by_slug( request, pin_slug, pin_language ):
	return Epoxy( request ).single( Pin, {'slug':pin_slug,'language':pin_language} ).json()
	
def publish_pin( request, pin_id ):
	response = Epoxy( request )
	new_status = request.POST.get("new_status")

	try:
		if new_status in dict(Pin.PIN_STATUS_CHOICES):
			p=Pin.objects.get( id=pin_id )
			p.status=new_status
			p.save()
			return response.json()
		else:
			return response.throw_error( error="status %s incorrect" % new_status).json()

	except Pin.DoesNotExist, e:
		return response.throw_error( error="%s" % e, code=API_EXCEPTION_DOESNOTEXIST).json()
		
		
def pin_upload( request ):
	response = Epoxy( request )
	d = dt.datetime.now()

	form = UploadPinForm( request.REQUEST )
	if not form.is_valid():
		return response.throw_error(error=form.errors, code=API_EXCEPTION_FORMERRORS)

	if len(form.cleaned_data['page_slug']) > 0:
		# attacch new pin to a selected page (both languages)
		response.add('page_slug',form.cleaned_data['page_slug'])
			
		try:
			page_en = Page.objects.get( slug=form.cleaned_data['page_slug'],language='EN')
			page_fr = Page.objects.get( slug=form.cleaned_data['page_slug'],language='FR')
		except Page.DoesNotExist:
			return response.throw_error( error=_("selected page does not exists"), code=API_EXCEPTION_FORMERRORS).json()

		response.add('page', [ page_en.json(), page_fr.json() ] )

	pin_path = response.add('path', "pins/%s-%s" % ( d.year, ( d.month if d.month >10 else "0%s" % d.month ) ) )
	absolute_pin_path = os.path.join( settings.MEDIA_ROOT, pin_path )

	try:
		if not os.path.exists( absolute_pin_path ): 
			os.makedirs( absolute_pin_path ) # throw an OS ERROR if exists... OR if it is not writable!
	except OSError, e:
		return response.throw_error( error="%s" % e, code=API_EXCEPTION_OSERROR ).json()

	for f in request.FILES.getlist('files[]'):
		if f.size == 0:
			return response.throw_error( error="uploaded file is empty", code=API_EXCEPTION_EMPTY ).json()

		filename = os.path.join( absolute_pin_path, f.name)
		pinup = open( filename , 'w' )

		for chunk in f.chunks():
			pinup.write( chunk )

		pinup.close()

		# guess mimetype
		pin_mimetype = mimetypes.guess_type( filename )[0]

		filetitle, extension = os.path.splitext( f.name )

		try:
			p_en = Pin( title=filetitle, language='EN', slug=slugify( "-".join( filetitle.split("_") ) ), mimetype=pin_mimetype, local=os.path.join( pin_path, os.path.basename( filename ) ) )
			p_fr = Pin( title=filetitle, language='FR', slug=slugify( "-".join( filetitle.split("_") ) ), mimetype=pin_mimetype, local=os.path.join( pin_path, os.path.basename( filename ) ) )
			p_en.save()
			p_fr.save()

		except IntegrityError, e:
			return response.throw_error( error="%s" % e, code=API_EXCEPTION_INTEGRITY ).json()

		if page_en and page_fr:
			page_en.pins.add( p_en )
			page_fr.pins.add( p_fr )
			page_en.save()
			page_fr.save()

	return response.json()

