#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db.models import Q 
from django.conf import settings as django_settings

from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

from django.template import RequestContext
from django.template.defaultfilters import slugify

from django.core.exceptions import *

#from settings import *

from glue.models import Pin
from outside.models import Enquiry, Subscriber, Message, Confirmation_code
from outside.forms import *
from glue.misc import Epoxy, API_EXCEPTION_FORMERRORS, API_EXCEPTION_INTEGRITY, API_EXCEPTION_OSERROR, API_EXCEPTION_DOESNOTEXIST, API_EXCEPTION_EMPTY
from glue.forms import AddPinForm
from django.db import IntegrityError
from reanalyseapp.models import Enquete, Tag, AccessRequest
from datetime import datetime

from django.contrib.auth import login, logout, authenticate

import os, mimetypes

from django.contrib.sites.models import get_current_site

from django.utils.translation import ugettext as _

from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.utils import translation

import string, random

from reanalyseapp.globalvars import *

from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

import json

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
				return response.throw_error( error=_("selected pin does not exists. Exception: %s" % e), code=API_EXCEPTION_DOESNOTEXIST).json()

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
	absolute_pin_path = os.path.join( django_settings.MEDIA_ROOT, pin_path )

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
	
	try:
		textes = Enquete.objects.get(id=enquete_id).texte_set
	except Enquete.DoesNotExist, e:
		response.meta('enquete_id', enquete_id )
		return response.throw_error(error="%s" % e, code=API_EXCEPTION_DOESNOTEXIST).json()
	
	response.meta('total_count', textes.count() )
	
	

	response.add('objects',[{
		'id':t.id,
		'type':t.doctype,
		'title':t.name,
		'articles': [{'article':a.name} for a in t.tags.filter(type=Tag.ARTICLE)],
		# 'tags':[ {'name':tag.name, 'type':tag.type} for tag in t.tags.all() ],
		'categories': [{'category':c} for c in t.doccat2.split(",")],
		'phases': [{'phase' : PHASE_LABEL[t.doccat1]}],
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
			
		else:
	
			
			if( form.cleaned_data['action'] == 'EDIT'):
				
			
				#GET subscriber id
				update = Subscriber.objects.filter(user=request.user.id).update(
													first_name = form.cleaned_data['first_name'],
													last_name = form.cleaned_data['last_name'],
													email = form.cleaned_data['email'],
													affiliation = form.cleaned_data['affiliation'],
													status = form.cleaned_data['status'],
													accepted_terms = form.cleaned_data['accepted_terms'],
													description = form.cleaned_data['description'])
				
				
			
			elif( form.cleaned_data['action'] == 'ADD'):
				contacts( form )
																						
			

	return response.queryset( Subscriber.objects.filter() ).json()


#Just send an email to the administrators, no inserts in DB
def contacts( form ):
	# logger.info("Welcome to GLUEBOX api")

	
	email_args = {'prenom': form.cleaned_data['first_name'],
				'nom': form.cleaned_data['last_name'],
				'email': form.cleaned_data['email'], 
				'affiliation': form.cleaned_data['affiliation'], 
				'site': django_settings.OUTSIDE_SITE_NAME, 
				'description': form.cleaned_data['description'],
				'REANALYSEURL':django_settings.REANALYSEURL+'/'+django_settings.OUTSIDE_SITE_NAME
				}
	
	#Notification mail to the client
	
	
	subject, from_email, to = _('beQuali : Message sent'),_("beQuali Team")+"<equipe@bequali.fr>", form.cleaned_data['email']
	
	
	email_args['action'] = "client_notification"			
	html_content = render_to_string('email/contact.html', email_args)
	
	
	text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
	
	# create the email, and attach the HTML version as well.
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
	msg.attach_alternative(html_content, "text/html")
	msg.send()
	
	
	#Send mail to bequali admins : sarah.cadorel@sciences-po.fr, guillaume.garcia, anne.both
	subject, from_email, to = _('beQuali contact request'),'admin@bequali.fr', django_settings.EMAIL_ADMINS
	
	email_args['action'] = "admin_notification"
	html_content = render_to_string('email/contact.html', email_args)
	text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
	
	# create the email, and attach the HTML version as well.
	msg = EmailMultiAlternatives(subject, text_content, from_email, to)
	msg.attach_alternative(html_content, "text/html")
	msg.send()


def i18n():
	from django.utils import translation	
	
	
	return {
		'LANGUAGES': django_settings.LANGUAGES,
		'LANGUAGE_CODE': translation.get_language(),
		'LANGUAGE_BIDI': translation.get_language_bidi(),
		}


def access_request( request ):
	
	#return HttpResponse(translation.get_language(), 'text')
	
	response = Epoxy( request )
	
	if response.method=="POST":

		form = AccessRequestForm( request.REQUEST )
		
		if not form.is_valid():
			return response.throw_error( error=form.errors,code=API_EXCEPTION_FORMERRORS).json()
		

		try:
			AccessRequest.objects.get( user = request.user, enquete=form.cleaned_data['enquete'] )
		
		except AccessRequest.DoesNotExist, e:
			
			# AccessRequest creation
			request_object = AccessRequest.objects.create(
				user = request.user,
				enquete = form.cleaned_data['enquete'],
				description = form.cleaned_data['description'],
				is_activated = False
			)
			path = '%s%s' % (django_settings.REANALYSEURL, reverse('admin:reanalyseapp_accessrequest_change', args=[request_object.id]) )
			
			#Send mail to bequali admin : sarah.cadorel@sciences-po.fr, guillaume.garcia, anne.both
			subject, from_email, to = _('bequali enquete request'),'admin@bequali.fr', django_settings.EMAIL_ADMINS
			

			
			email_args ={'prenom': form.cleaned_data['first_name'],
						'nom': form.cleaned_data['last_name'], 
						'email': form.cleaned_data['email'], 
						'affiliation': form.cleaned_data['affiliation'], 
						'site': django_settings.OUTSIDE_SITE_NAME,
						'description': form.cleaned_data['description'], 
						'enquete': form.cleaned_data['enquete'], 
						'url': path,
						'REANALYSEURL': django_settings.REANALYSEURL+'/'+django_settings.OUTSIDE_SITE_NAME} 
						
			
			email_args['action'] = 'ask_request'
			html_content = render_to_string('email/access_request.html', email_args)
			text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
			
			msg = EmailMultiAlternatives(subject, text_content, from_email, to)
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			
			
			to = form.cleaned_data['email']
			
			
			subject = "beQuali demande d'acces notification"
			email_args['action'] = "ask_notification"			
			html_content = render_to_string('email/access_request.html', email_args)
			text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
			
			# create the email, and attach the HTML version as well.
			
			send_mail(subject, text_content, from_email, [to])
			msg = EmailMultiAlternatives()
			msg.attach_alternative(html_content, "text/html")
			msg.send()
					
			
			
			
			
		except IntegrityError, e:

			return response.throw_error( error="%s"%e, code=API_EXCEPTION_INTEGRITY).json()
		
		else: #Request exists
						
			pass
			
			
			
	return response.json()




def signup( request, subscriber_id ):
	return Epoxy( request ).single( Signup, {'id':subscriber_id} ).json()


def signups(request):
	# logger.info("Welcome to GLUEBOX api")
	response = Epoxy( request )
	if response.method=="POST":

		form = SignupForm( request.REQUEST )
		
		if not form.is_valid():
			return response.throw_error( error=form.errors, code=API_EXCEPTION_FORMERRORS).json()
		
		
		if(form.cleaned_data['password1'] != form.cleaned_data['password2']):
			return response.throw_error( 
									error={'password1':'Please enter and confirm your password', 
										'password2':'Please enter and confirm your password'}, 
									code=API_EXCEPTION_FORMERRORS).json()
		"""else:
			if CheckPassword( form.cleaned_data['password1'] ) < 3 :
				return response.throw_error( 
									error=_('The password stength is too weak.'),
									code=API_EXCEPTION_FORMERRORS,
									fields={'password1':'', 'password2':''}
									
									).json()
		"""
		
		#Check email already exists in database
		
			
		
		if User.objects.filter( email = form.cleaned_data['email'] ).count() > 0 :
			return response.throw_error( 
									error=_('This email is already used in the database.'),
									code=API_EXCEPTION_FORMERRORS,
									fields={'email':''}).json()
		
		
		try:
			created_user =  User.objects.get( username = form.cleaned_data['username'] )
		
		except User.DoesNotExist, e:	
			# User creation
			created_user = User.objects.create(
				first_name = form.cleaned_data['first_name'],
				last_name = form.cleaned_data['last_name'],
				username = form.cleaned_data['username'].lower(),
				email = form.cleaned_data['email'],
				is_active = False,
			)
			
			created_user.set_password(str(form.cleaned_data['password2']))
			created_user.save()

	
		else: #If the user already exists
			
			return response.throw_error( error=_('This username is already used'), code=API_EXCEPTION_INTEGRITY, fields={"username":""}).json()
		
	
		
		try:
			s = Subscriber.objects.get( user=created_user )

		except Subscriber.DoesNotExist, e:

			s = Subscriber(
				user = created_user,
				affiliation = form.cleaned_data['affiliation'],
				first_name = form.cleaned_data['first_name'],
				last_name = form.cleaned_data['last_name'],
				status = form.cleaned_data['status'],
				accepted_terms = form.cleaned_data['accepted_terms'],
				description = form.cleaned_data['description'],
				email = form.cleaned_data['email'],
				email_confirmed=False
			)
			s.save()
				
			mail_send = send_confirmation_mail( subscriber=s, request=request, action="signup" )
			
			if( mail_send ==  False ):
				created_user.delete()
				return response.throw_error( error=_('This email does not exists'), code=API_EXCEPTION_INTEGRITY, fields={"email":""}).json()
	
	return response.queryset( Subscriber.objects.filter() ).json()





import re
def CheckPassword(password):
    strength = ['Blank','Very Weak','Weak','Medium','Strong','Very Strong']
    score = 1

    if len(password) < 1:
        return strength[0]
    if len(password) < 4:
        return strength[1]

    if len(password) >=8:
        score = score + 1
    if len(password) >=10:
        score = score + 1
    
    if re.search('\d+',password):
        score = score + 1
    if re.search('[a-z]',password) and re.search('[A-Z]',password):
        score = score + 1
    if re.search('.[!,@,#,$,%,^,&,*,?,_,~,-,£,(,)]',password):
        score = score + 1

    return score
		


import smtplib

def send_confirmation_mail( subscriber, request, action ):
	
	if(action == 'signup'):
		
		confirmation_code = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(33))
		
		confirmation_code_row = Confirmation_code.objects.create(
				code = confirmation_code,
				action='signup',
				activated = True,
			)
		
		confirmation_code_row.save()
		
	
		subject, from_email, to = _("beQuali signup"), _("beQuali Team")+"<equipe@bequali.fr>", subscriber.user.email
		
		confirmation_href = "%s://%s%s"% ( 'https' if request.is_secure()  else 'http', 
										request.get_host(), 
										reverse('outside.views.confirm',
											args=(confirmation_code, 
											subscriber.user.id, 
											'signup'
											)))
			
		html_content = render_to_string('email/signup.html', 
									{'action':'email_confirm',
									'prenom': subscriber.first_name,
									'nom': subscriber.last_name,
									'confirmation_href': confirmation_href,
									'username': subscriber.user.username, 
									'password': '**********',#request.REQUEST['password1'],
									
									
									}, RequestContext(request, 
													{'REANALYSEURL': django_settings.REANALYSEURL+'/'+django_settings.OUTSIDE_SITE_NAME}
													)
									)
		
		text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
		
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		
		try:
			
			msg.send()
			
		except Exception, e:
			return False
		else :
			return True
	
	elif( action == 'reinitialize_password'):
		
					
		#Send mail
		
		subject, from_email, to = _("beQuali reinitialize password request"), _("beQuali Team")+"<equipe@bequali.fr>", subscriber.user.email
		
		
		
		
		confirmation_code = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(33))
		
		confirmation_code_row = Confirmation_code.objects.create(
				code = confirmation_code,
				action='reinitPass',
				activated = True,
			)
		
		confirmation_code_row.save()
		
		

		confirmation_href = "%s://%s%s"% ( 'https' if request.is_secure()  
													else 'http', request.get_host(), reverse('outside.views.confirm', 
																							args=(confirmation_code, 
																								subscriber.user.id, 
																								'reinitPass'
																							)))
		html_content = render_to_string('email/reinitialize_password.html',{'action':'reinitialize_confirm',
									'prenom': subscriber.first_name,
									'nom': subscriber.last_name,
									'confirmation_href': confirmation_href,
									'username': subscriber.user.username, 
									
									}, RequestContext(request, {'REANALYSEURL': django_settings.REANALYSEURL+'/'+django_settings.OUTSIDE_SITE_NAME}))

		
		
		
		text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
		
		# create the email, and attach the HTML version as well.
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()

	


def reinitialize_password(request):
	
	response = Epoxy( request )
	if request.method == 'POST':
		form = ReinitializePasswordForm( request.REQUEST )
		
		if form.is_valid():
			
			try:
			
				#user = User.objects.get(username=form.cleaned_data['username'], email__iexact=form.cleaned_data['email'])
				user = User.objects.get(email__iexact=form.cleaned_data['email'])
				
			except  MultipleObjectsReturned, e:
				
				user = User.objects.filter(email__iexact=form.cleaned_data['email'])
				user = user[0]
				
			except User.DoesNotExist, e :
				return response.throw_error( error=_('This user does not exist in our database'), code=API_EXCEPTION_DOESNOTEXIST).json()
				
			
				
			subscriber = get_object_or_404( Subscriber, user__id=user.id )
			send_confirmation_mail(subscriber, request, action='reinitialize_password')
				

		else:
			return response.throw_error( error=form.errors, code=API_EXCEPTION_FORMERRORS).json()
				
	return response.json()
	


def change_password(request):
	response = Epoxy( request )
	if request.method == 'POST':
		form = ChangePasswordForm( request.REQUEST )
		
		if form.is_valid():
			uPass1 = form.cleaned_data['password1']
			uPass2 = form.cleaned_data['password2']
			
			if uPass1 == uPass2:
				user = User.objects.get(username=form.cleaned_data['username'])
				user.set_password(uPass1)
				user.save()
			else:
				return response.throw_error( error={'password1':'the 2 pwd must be the same', 'password2':'the 2 pwd must be the same'}, code=API_EXCEPTION_FORMERRORS).json()
		else:
			return response.throw_error( error=form.errors, code=API_EXCEPTION_FORMERRORS).json()
				
	return response.json()
				

def test( request ):
	response = Epoxy( request )
	response.add( 'full_path', request.get_host()  )
	
	full_url =  "%s://%s%s"% ( 'https' if request.is_secure()  else 'http', request.get_host(), reverse('outside.views.confirm', args=( "dsdsdsds", 12 ) ) )
	response.add( 'full_url',  full_url  )
	
	

	return response.json()


def subscriber( request, subscriber_id ):
	return Epoxy( request ).single( Subscriber, {'id':subscriber_id} ).json()



def captcha_refresh(request):
	""" Return json with new captcha for ajax refresh request """
	
	new_key = CaptchaStore.generate_key()
	to_json_response = {
					'key': new_key,
					'image_url': captcha_image_url(new_key),
					}
	return HttpResponse(json.dumps(to_json_response), content_type='application/json')


def captcha(request):
	# this compare captcha's number from POST and SESSION
	if(request.method == 'POST' and request.POST['captcha'] is not None and request.POST['captcha'] == request.session['captcha']):
		request.session['captcha'] = "success"# this line makes session free, we recommend you to keep it
	
	elif(request.method == 'POST' and request.POST['captcha'] is None):
		return HttpResponse('failed', 'text')
	
	else:
		rand = random.randint(0, 4)
		request.session['captcha'] = rand
		return HttpResponse(rand, 'text')


def auth_login( request ):
	
	response = Epoxy( request )

	form = LoginForm( request.POST )
	try:
		if 'next' not in request.session:
			request.session['next'] = request.REQUEST['next']
	except:
		pass
	
	
	if request.method == 'POST': 

		if form.is_valid():
			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
			if user is not None:
				if user.is_active:
					login(request, user)

					try:
						subscriber = Subscriber.objects.get(user=request.user.id)
					except Subscriber.DoesNotExist:
						return redirect( reverse('outside.views.create_profile') )
					
					next_url = request.session['next']
					
					del request.session['next']
					
					response.add( 'next', next_url  )
	
				else:
					return response.throw_error( _("user has been disabled"), code=API_EXCEPTION_FORMERRORS).json()
			else:
				return response.throw_error( error=form.errors, code=API_EXCEPTION_FORMERRORS).json()
		else:
			"""login_message['error'] = _("invalid credentials")
			login_message['invalid_fields'] = form.errors"""
			#return HttpResponse('TEST')
			return response.throw_error( error=form.errors, code=API_EXCEPTION_FORMERRORS).json()
	
		
		
		return response.json()

