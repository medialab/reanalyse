from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import Q 
from django.contrib.auth.models import User


from glue.models import Pin
from outside.models import Enquiry, Subscriber, Message
from outside.forms import AddEnquiryForm, SubscriberForm, SignupForm
from glue.misc import Epoxy, API_EXCEPTION_FORMERRORS, API_EXCEPTION_INTEGRITY, API_EXCEPTION_OSERROR, API_EXCEPTION_DOESNOTEXIST, API_EXCEPTION_EMPTY
from glue.forms import AddPinForm
from django.db import IntegrityError
from reanalyseapp.models import Enquete, Tag
from datetime import datetime
import os, mimetypes

from django.contrib.sites.models import get_current_site

from django.utils.translation import ugettext as _

import string
import random

version = '0.0.3'

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


# add or retrieve a list of pins objects attached to a given enquiry
def enquiry_pins( request, enquiry_slug ):

	response = Epoxy( request )

	# get both language enquiry objects
	try:
		enquiry_en = Enquiry.objects.get( slug=enquiry_slug,language='EN')
		enquiry_fr = Enquiry.objects.get( slug=enquiry_slug,language='FR')
	except Page.DoesNotExist, e:
		return response.throw_error( error="%s" % e, code=API_EXCEPTION_DOESNOTEXIST ).json()

	response.add('enquiry', [ enquiry_en.json(), enquiry_fr.json() ] )

	if response.method =='POST':
		form = AddPinForm( request.REQUEST )
		if not form.is_valid():
			return response.throw_error( error=form.errors, code=API_EXCEPTION_FORMERRORS).json()

		if len(form.cleaned_data['parent_pin_slug']) > 0:
			# attacch new pin to a selected pin (pin children, usually displayed on the right side, both languages)
			response.add('parent_pin_slug',form.cleaned_data['parent_pin_slug'])
			
			try:
				pin_en = Pin.objects.get( slug=form.cleaned_data['parent_pin_slug'],language='EN')
				pin_fr = Pin.objects.get( slug=form.cleaned_data['parent_pin_slug'],language='FR')
			except Pin.DoesNotExist, e:
				return response.throw_error( error=_("selected pin does not exists. Exception: %s" % e), code=API_EXCEPTION_FORMERRORS).json()

			response.add('pin', [ pin_en.json(), pin_fr.json() ] )

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
		
		# attach to enquiry
		enquiry_en.pins.add( p_en )
		enquiry_en.save()
		enquiry_fr.pins.add( p_fr )
		enquiry_fr.save()

	#if response.method =='POST':
	#	form = AddPinForm( request.REQUEST )
	#	if not form.is_valid():
	#		return response.throw_error( error=form.errors, code=API_EXCEPTION_FORMERRORS).json()


	return response.queryset( Pin.objects.filter(Q(enquiry=enquiry_fr) | Q(enquiry=enquiry_en) ) ).json()




def enquiry_upload_pin( request, enquiry_id, pin_slug ):
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

	# check somethign
	try:
		parent_pin_en = Pin.objects.get(slug=pin_slug, language="EN")
		parent_pin_fr = Pin.objects.get(slug=pin_slug, language="FR")
	except Pin.DoesNotExist, e:
		return response.throw_error( error="%s" % e, code=API_EXCEPTION_DOESNOTEXIST ).json()
		

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

		parent_pin_en.children.add( p_en )
		parent_pin_fr.children.add( p_fr )
		parent_pin_en.save()
		parent_pin_fr.save()



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
		response.meta('enquete_id', enquete_id )
		return response.throw_error(error="%s" % e, code=API_EXCEPTION_DOESNOTEXIST).json()
	
	response.meta('total_count', textes.count() )
	response.meta('version', version)


	response.add('objects',[{
		'id':t.id,
		'type':t.doctype,
		'title':t.name,
		'articles': [{'article':a.name} for a in t.tags.filter(type=Tag.ARTICLE)],
		# 'tags':[ {'name':tag.name, 'type':tag.type} for tag in t.tags.all() ],
		'categories': [{'category':c} for c in t.doccat2.split(",")],
		'phases': [{'phase' : t.doccat1}],
		'times':[{'time':t.date.isoformat()} ] if t.date else [],
		'location': t.locationgeo,
		'coordinates' : {"type": "Feature","geometry": {"type": "Point","coordinates": t.locationgeo.split(",")[::-1] if t.locationgeo else [] },"properties": {"name": t.location}},
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
			
			s = Subscriber.objects.get( email=form.cleaned_data['email']  )
			

		except Subscriber.DoesNotExist, e:
			s = Subscriber(
				first_name = form.cleaned_data['first_name'],
				last_name = form.cleaned_data['last_name'],
				email = form.cleaned_data['email'],
				affiliation = form.cleaned_data['affiliation'],
				status = form.cleaned_data['status'],
				accepted_terms = form.cleaned_data['accepted_terms'],
				description = form.cleaned_data['description'])
			s.save()

		
		if s is None:
			return response.throw_error( error="", code=API_EXCEPTION_INTEGRITY).json()
		
		m = Message(
			content=form.cleaned_data['description']
		)
		m.save()

		s.messages.add( m )
		s.save()

		response.add("object", m, jsonify=True )

	return response.queryset( Subscriber.objects.filter() ).json()



def signup( request, subscriber_id ):
	return Epoxy( request ).single( Signup, {'id':subscriber_id} ).json()


def signups(request):
	# logger.info("Welcome to GLUEBOX api")
	response = Epoxy( request )
	if response.method=="POST":

		form = SignupForm( request.REQUEST )
		
		if not form.is_valid():
			return response.throw_error( error=form.errors, code=API_EXCEPTION_FORMERRORS).json()
		
		try:
			# User creation
			created_user = User.objects.create(
				first_name = form.cleaned_data['first_name'],
				last_name = form.cleaned_data['last_name'],
				username = form.cleaned_data['email'],
				email = form.cleaned_data['email'],
				password = form.cleaned_data['password'],
				is_active = False
			)
		
		except IntegrityError, e:
			return response.throw_error( error="%s"%e, code=API_EXCEPTION_INTEGRITY).json()		
		
		# desactivate user
		created_user.is_active = False
			
		confirmation_code = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(33))
		
		try:
					
			s = Subscriber(
				user = created_user,
				affiliation = form.cleaned_data['affiliation'],
				first_name = form.cleaned_data['first_name'],
				last_name = form.cleaned_data['last_name'],
				email = form.cleaned_data['email'],
				status = form.cleaned_data['status'],
				accepted_terms = form.cleaned_data['accepted_terms'],
				description = "Enquete : %s \n\n %s" % ( request.POST.get( 'enquete_id', 0 ), form.cleaned_data['message'] ),
				confirmation_code=confirmation_code
			)
			
		except IntegrityError, e:
			return response.throw_error( error="%s"%e, code=API_EXCEPTION_INTEGRITY).json()		
		
			s.save()
			
			send_registration_confirmation( subscriber=s, request=request )

			response.add('object', s, jsonify=True)

		
	return response.queryset( Subscriber.objects.filter() ).json()



def send_registration_confirmation( subscriber, request ):

	confirmation_href = "%s/%s/%s/" % ( settings.REANALYSEURL, s.confirmation_code, subscriber.user.username )

	send_mail(
		_("account confirmation"), 
		'<href="%s">%s</a>' % ( confirmation_href, confirmation_href ),
		'Bequali Registration submission <signup@bequali.fr>'
		,[ subscriber.email ],
		fail_silently=False
	)
	
	
def confirm(request, confirmation_code, username):
	try:
		user = User.objects.get(username=username)
		profile = Subscriber.objects.get(user=user)
		
		if profile.confirmation_code == confirmation_code and user.date_joined > (datetime.datetime.now()-datetime.timedelta(days=1)):
			
			#TODO : TURN CONFIRM EMAIL FLAG DBFIELD TO TRUE
			
			

			user.is_active = True
			#user.save()
			#user.backend='django.contrib.auth.backends.ModelBackend' 
			#auth_login(request,user)
		return HttpResponseRedirect('../../../../../')
	except:
		return HttpResponseRedirect('../../../../../')


def subscriber( request, subscriber_id ):
	return Epoxy( request ).single( Subscriber, {'id':subscriber_id} ).json()
