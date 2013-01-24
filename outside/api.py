from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.conf import settings

from glue.models import Pin
from outside.models import Enquiry
from outside.forms import AddEnquiryForm
from glue.misc import Epoxy, API_EXCEPTION_FORMERRORS, API_EXCEPTION_INTEGRITY, API_EXCEPTION_OSERROR, API_EXCEPTION_DOESNOTEXIST, API_EXCEPTION_EMPTY
from django.db import IntegrityError
from reanalyseapp.models import Enquete
from datetime import datetime
import os, mimetypes


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

def enquiry_upload_pin( request, enquiry_id ):
	response = Epoxy( request )
	d = datetime.now()
	try:
		enquiry = Enquiry.objects.get(id=enquiry_id)

		enquiry_en = Enquiry.objects.get( language="EN", slug=enquiry.slug )
		enquiry_fr = Enquiry.objects.get( language="FR", slug=enquiry.slug )
	except Enquiry.DoesNotExist, e:
		return response.throw_error( error="%s" % e, code=API_EXCEPTION_DOESNOTEXIST ).json()
	response.add('enquiries', [ enquiry_en.json(), enquiry_fr.json() ] )

	pin_path = response.add('path', "pins/%s-%s" % ( d.year, ( d.month if d.month >10 else "0%s" % d.month ) ) )
	absolute_pin_path = os.path.join( settings.MEDIA_ROOT, pin_path )

	try:
		if not os.path.exists( absolute_pin_path ): 
			os.makedirs( absolute_pin_path ) # throw an OS ERROR if exists... OR if it is not writable
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

		try:
			p_en = Pin( title=f.name, language='EN', slug=slugify( f.name ), mimetype=pin_mimetype, local=os.path.join( pin_path, os.path.basename( filename ) ) )
			p_fr = Pin( title=f.name, language='FR', slug=slugify( f.name ), mimetype=pin_mimetype, local=os.path.join( pin_path, os.path.basename( filename ) ) )
			p_en.save()
			p_fr.save()

		except IntegrityError, e:
			return response.throw_error( error="%s" % e, code=API_EXCEPTION_INTEGRITY ).json()

		enquiry_en.pins.add( p_en )
		enquiry_fr.pins.add( p_fr )
		enquiry_en.save()
		enquiry_fr.save()

	return response.json()

#
#    API AUTH VIEWS
#    ==============
#
API_ACCESS_DENIED_URL = "/elipss/panelmanager/api/access-restricted"


def enquete_data( request, enquete_id ):
	data = {}
	# return render_to_response('outside/enquete_data.json', RequestContext(request, data ) )
	
	response = Epoxy( request )
	import random
	try:
		textes = Enquete.objects.get(id=enquete_id).texte_set
	except Enquete.DoesNotExist, e:
		return response.throw_error(error="%s" % e, code=API_EXCEPTION_DOESNOTEXIST).json()
	
	response.meta('total_count', textes.count() )

	response.add('objects',[{
		'id':t.id,
		'type':t.doctype,
		'title':t.name,
		'tags':[ {'name':tag.name, 'type':tag.type} for tag in t.tags.all() ],
		'categories': [{'category':c} for c in t.doccat2.split(",")],
		'phases': [{'phase' : t.doccat1}],
		'times':[{'time':t.date.isoformat()} ] if t.date else [],
		'location': t.locationgeo,
		'coordinates' : {"type": "Feature","geometry": {"type": "Point","coordinates": [ 360*random.random() - 180, 180*random.random() - 90 ]},"properties": {"name": t.location}},
		'date':t.date.isoformat() if t.date else None
	} for t in textes.all() ])	
	return response.json()
	data = {}
	return render_to_response('outside/enquete_data.json', RequestContext(request, data ) )


def subscribers(request):
	# logger.info("Welcome to GLUEBOX api")
	response = Epoxy( request )
	if response.method=="POST":

		form = SubscriberForm( request.REQUEST )
		
		if not form.is_valid():
			return response.throw_error( error=form.errors, code=API_EXCEPTION_FORMERRORS).json()
		try:
			s = Subscriber(
				first_name = form.cleaned_data['first_name'],
				last_name = form.cleaned_data['last_name'],
				email = form.cleaned_data['email'],
				affiliation = form.cleaned_data['affiliation'],
				accepted_terms = form.cleaned_data['accepted_terms'],
				description = form.cleaned_data['description']).save()
		except IntegrityError, e:
			return response.throw_error( error="%s" % e, code=API_EXCEPTION_INTEGRITY).json()

	return response.queryset( Subscriber.objects.filter() ).json()
	

def subscriber( request, subscriber_id ):
	return Epoxy( request ).single( Subscriber, {'id':subscriber_id} ).json()
