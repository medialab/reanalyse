#!/usr/bin/python
# -*- coding: utf8 -*-


import urllib, os



from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _

from mimetypes import guess_extension, guess_type

from reanalyseapp.models import Enquete, Tag, Texte

from glue.models import Pin, Page
from glue.forms import LoginForm, AddPageForm, AddPinForm, EditPinForm

from outside.models import Enquiry, Subscriber
from outside.sites import OUTSIDE_SITES_AVAILABLE
from outside.forms import AddEnquiryForm, SubscriberForm, SignupForm

from django.core.mail import EmailMultiAlternatives


	
# settings.py
LOGIN_URL = '/reanalyse/login/'

#
#    Outside
#    =======
#
def index( request ):
	data = shared_context( request, tags=[ "index" ] )
	
	try:
		data['page'] = Page.objects.get( slug="index", language=data['language'])
	except Page.DoesNotExist:
		p_en = Page( title="Home Page", language='EN', slug="index")
		p_en.save()

		p_fr = Page( title="Home Page", language='FR', slug="index")
		p_fr.save()

		data['page'] = p_fr if data['language'] == 'FR' else p_en

	# load all pins without page
	data['pins'] = Pin.objects.filter(language=data['language'], page__slug="index" ).order_by("-id")

	# get news
	data['news'] = _get_news( data )

	return render_to_response( "%s/index.html" % data['template'], RequestContext(request, data ) )

def news( request ):
	data = shared_context( request, tags=[ "news" ] )
	# load all pins without page
	data['pins'] = _get_news( data )
	return render_to_response("%s/blog.html" % data['template'], RequestContext(request, data ) )

def _get_news( data ):
	return  Pin.objects.filter(language=data['language'], page__isnull=True, enquiry__isnull=True, parent__isnull=True ).order_by("-id")

def contacts( request ):
	data = shared_context( request, tags=[ "contacts" ] )
	# load all pins without page (aka news)
	data['pins'] = Pin.objects.filter(language=data['language'], page__isnull=True, parent__isnull=True ).order_by("-id")
	return render_to_response("%s/contacts.html" % data['template'], RequestContext(request, data ) )


def page( request, page_slug ):
	data = shared_context( request, tags=[ page_slug ] )
	data['page'] = get_object_or_404(Page, slug=page_slug, language=data['language'] )
	data['pins'] = Pin.objects.filter( page__slug=page_slug, language=data['language'], parent=None)

	return render_to_response("%s/page.html" % 'enquete', RequestContext(request, data ) )

def enquete( request, enquete_id ):
	data = shared_context( request, tags=[ "enquetes", "focus-on-enquete" ] )
	data['enquete'] = get_object_or_404( Enquete, id=enquete_id )
	data['disabled'] =  [ t.slug for t in data['enquete'].tags.filter( type=Tag.DISABLE_VISUALIZATION ) ]
	
	
	
	try:
		data['enquiry'] = Enquiry.objects.get( enquete=enquete_id, language=data['language'] )
	except Enquiry.DoesNotExist,e:
		pass
		# data['enquiry'] = None


	return render_to_response('enquete/enquete.html', RequestContext(request, data ) )




def enquete_metadata( request, enquete_id ):
	data = shared_context( request, tags=[ "enquetes","metadata" ] )
	enquete = get_object_or_404( Enquete, id=enquete_id )
	enquete.meta = enquete.meta_items()
	
	data['enquete'] = enquete	
	
	try:
		data['enquiry'] = Enquiry.objects.get( enquete=enquete_id, language=data['language'] )
		
	except Enquiry.DoesNotExist,e:
		pass

	return render_to_response('enquete/metadata.html', RequestContext(request, data ) )


@login_required( login_url=LOGIN_URL )
@permission_required('reanalyseapp.can_browse')
def enquete_download( request, enquete_id ):
	
	enquete = get_object_or_404( Enquete, id=enquete_id )

	import zipfile, zlib

	zippath = os.path.join( "/tmp/", "enquete_%s.zip" % enquete.id )

	zf = zipfile.ZipFile( zippath, mode='w' )

	for t in Texte.objects.filter( enquete=enquete ):
		zf.write( t.locationpath, compress_type=zipfile.ZIP_DEFLATED, arcname= os.path.join( t.doctype, os.path.basename(  t.locationpath ) ) )

	response = HttpResponse( open( zippath , 'r' ) , content_type="application/gzip"  )
	response['Content-Description'] = "File Transfer";
	response['Content-Disposition'] = "attachment; filename=enquete-%s.zip" % ( enquete.id ) 
	
	return response


@login_required( login_url=LOGIN_URL )
@permission_required('reanalyseapp.can_browse')
def document( request, document_id ):
	data = shared_context( request, tags=[ "enquetes","metadata" ] )

	data['document'] = document = get_object_or_404( Texte, id=document_id )
	data['enquete'] = document.enquete
	data['mimetype'] = guess_type( document.locationpath )[0]

	return render_to_response('enquete/document.html', RequestContext(request, data ) )


@login_required( login_url=LOGIN_URL )
@permission_required('reanalyseapp.can_browse')
def document_download( request, document_id ):
	data = shared_context( request )
	
	document = get_object_or_404( Texte, id=document_id )

	mimetype = guess_type( document.locationpath )[0]

	try:
		extension = guess_extension( mimetype )
		content_type = mimetype
	except AttributeError, e:
		filetitle, extension = os.path.splitext( document.locationpath )
		content_type = "application/octet-stream"

	response = HttpResponse( open( document.locationpath , 'r' ) , content_type=content_type  )
	response['Content-Description'] = "File Transfer";
	response['Content-Disposition'] = "attachment; filename=%s-%s-%s%s" % ( document.enquete.id, document.id, document.name, extension ) 
	
	return response

@login_required( login_url=LOGIN_URL )
@permission_required('reanalyseapp.can_browse')
def document_embed( request, document_id ):
	data = shared_context( request )
	
	document = get_object_or_404( Texte, id=document_id )


	mimetype = guess_type( document.locationpath )[0]

	try:
		extension = guess_extension( mimetype )
		content_type = mimetype
	except AttributeError, e:
		filetitle, extension = os.path.splitext( document.locationpath )
		content_type = "application/octet-stream"

	return HttpResponse( open( document.locationpath , 'r' ) , mimetype=content_type  )
	

def enquiry( request, enquete_id ):
	data = shared_context( request, tags=[ "enquetes","enquiry" ] )
	data['enquiry'] = get_object_or_404( Enquiry, enquete__id=enquete_id, language=data['language'])
	data['sections'] = data['enquiry'].pins.order_by(*["sort","-id"])

	

	return render_to_response('enquete/enquiry.html', RequestContext(request, data ) )


	
def enquiries( request ):

	data = shared_context( request, tags=[ "enquiries" ] )
	
	try:
		data['page'] = Page.objects.get( slug="enquiries", language=data['language'])
	except Page.DoesNotExist:
		p_en = Page( title="studies on studies", language='EN', slug="enquiries")
		p_en.save()

		p_fr = Page( title="enquêtes sur les enquêtes", language='FR', slug="enquiries")
		p_fr.save()

		data['page'] = p_fr if data['language'] == 'FR' else p_en

	data['enquiries'] = Enquiry.objects.filter( language=data['language'] )

	return render_to_response('enquete/enquiries.html', RequestContext(request, data ) )


def enquetes( request ):
	data = shared_context( request, tags=[ "enquetes" ] )
	data['enquetes'] = Enquete.objects.all() 
	data['page'] = get_object_or_404(Page, slug="enquetes", language=data['language'] )
	data['pins'] = Pin.objects.filter( page__slug="enquetes", language=data['language'], parent=None)

	return render_to_response("enquete/enquetes.html", RequestContext(request, data ) )

def download_view( request, pin_slug ):
	data = shared_context( request )
	pin = get_object_or_404(Pin, slug=pin_slug, language=data['language'] )
	data['root'] = settings.MEDIA_ROOT
	
	try:
		extension = guess_extension( pin.mimetype )
		content_type = pin.mimetype
	except AttributeError, e:
		filetitle, extension = os.path.splitext( pin.local.url )
		content_type = "application/octet-stream"

	response = HttpResponse( open( os.path.join( settings.MEDIA_ROOT, urllib.unquote( pin.local.url ) ), 'r' ) , content_type=content_type  )
	response['Content-Description'] = "File Transfer";
	response['Content-Disposition'] = "attachment; filename=%s%s" % ( pin_slug, extension ) 
	
	return response

def legal( request ):
	data = shared_context( request, tags=[ "legal" ] )
	
	try:
		data['page'] = Page.objects.get( slug="legal-notice", language=data['language'])
	except Page.DoesNotExist:
		p_en = Page( title="Legal", language='EN', slug="legal-notice")
		p_en.save()

		p_fr = Page( title="Mentions légales", language='FR', slug="legal-notice")
		p_fr.save()

		data['page'] = p_fr if data['language'] == 'FR' else p_en

	# load all pins without page
	data['pins'] = Pin.objects.filter(language=data['language'], page__slug="legal-notice" ).order_by("-id")

	# get news
	# data['news'] = Pin.objects.filter(language=data['language'], page__isnull=True, status=Pin.published ).order_by("-id")

	return render_to_response(  "%s/legal.html" % data['template'], RequestContext(request, data ) )



def login_view( request ):
	
	form = LoginForm( request.POST )
	login_message = { 'next':request.REQUEST.get('next', 'outside_index') }

	if form.is_valid():
		user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
		if user is not None:
			if user.is_active:
				login(request, user)
				# @todo: Redirect to next page
				return redirect( request.REQUEST.get('next', 'outside_index') )
			else:
				login_message['error'] = _("user has been disabled")
		else:
			login_message['error'] = _("invalid credentials")
			# Return a 'disabled account' error message
	else:
		login_message['error'] = _("invalid credentials")
		login_message['invalid_fields'] = form.errors


	data = shared_context( request, tags=[ "index" ], previous_context=login_message )


	return render_to_response('outside/login.html', RequestContext(request, data ) )



def signup( request, enquete_id=None ):
	
	if enquete_id is not None:
		data = shared_context( request, tags=[ "enquetes", "signup" ] )
	
		data['enquete'] = get_object_or_404( Enquete, id=enquete_id )
	else:
		data = shared_context( request, tags=[ "signup" ] )
	

	data['signup_form'] = SignupForm(  auto_id="id_signup_%s" )

	# load all pins without page (aka news)
	# data['pins'] = Pin.objects.filter(language=data['language'], page__isnull=True ).order_by("-id")
	
	if enquete_id is not None:
		return render_to_response("enquete/signup.html", RequestContext(request, data ) )
	
	return render_to_response("%s/signup.html" % data['template'], RequestContext(request, data ) )



def confirm( request, token, user_id ):
	
	subscriber = get_object_or_404( Subscriber, user__id=user_id, confirmation_code=token )

	data = shared_context( request, tags=[ "signup" ] )
	
	form_datas = {
		'1. Prenom' : subscriber.first_name,
		'2. nom' : subscriber.last_name,
		'3. email' : subscriber.email,
		'4. affiliation' : subscriber.affiliation,
		'4. status' : dict(Subscriber.STATUS_CHOICES)[subscriber.status],
		'5. message' : subscriber.description
	}	
	
	subject, from_email, to = _("Signup request"),"L'équipe Bequali <equipe@bequali.fr>", settings.EMAIL_ADMINS
	html_content = '%s<br/><br/>%s :<br/><br/>%s<br/><br/>%s</br/><br/>%s' % (
		_('Hello, you have a new signup request.'),
		_('Information'), 
		''.join(['%s : %s<br/>' % (k, v) for k, v in sorted(form_datas.items())]),
		_('Goodbye'),
		'<img src="http://quali.dime-shs.sciences-po.fr/bequali/static/img/bequali-logo.png"/>'
		)
	text_content = html_content.replace('<br/>', '\n')
	
	msg = EmailMultiAlternatives(subject, text_content, from_email, to)
	msg.attach_alternative(html_content, 'text/html')
	msg.content_subtype = 'html'
	
	msg.send()
	if not subscriber.email_confirmed :
		subscriber.email_confirmed = True
		subscriber.save()
		msg.send()
		
		return render_to_response("%s/confirm.html" % data['template'], {'error':'0'}, RequestContext(request, data ) )
		
	else:
		#TODO 
		return render_to_response("%s/confirm.html" % data['template'],{'error':'1'}, RequestContext(request, data ) )
	
	
	

	
	
	
	

										 
	
	

	send_mail(
		"Demande d'inscription", 
		'<href="%s">%s</a>' % ( confirmation_href, confirmation_href ),
		'Bequali Registration submission <signup@bequali.fr>'
		,[ 'alexandreaazzouz@gmail.com' ],
		fail_silently=False
	)
		


def logout_view( request ):
	logout( request )
	return redirect( 'outside_index' )

def studies( request ):
	data = shared_context( request, tags=[ "studies" ] )
	#data['studies'] = Enquete.objects.all().order_by('-id')
	#data['page'] = Bean.objects.get( slug='studies', type='PAGE', language=data['language'] )
	return render_to_response('outside/studies.html', RequestContext(request, data ) )

def shared_context( request, tags=[], previous_context={} ):
	# startup
	d = previous_context
	d['tags'] = tags
	d['site'] = settings.OUTSIDE_SITE_NAME
	d['sites_available'] = OUTSIDE_SITES_AVAILABLE
	d['stylesheet'] = settings.OUTSIDE_THEME
	d['template'] = settings.OUTSIDE_TEMPLATE_DIR

	d['subscriber_form'] = SubscriberForm( auto_id="id_subscriber_%s")

	# if it is not auth, pull loginform
	if request.user.is_authenticated():
		load_edit_mode( request, d )
	else:
		d['login_form'] = LoginForm()


	# load language and share it inside context
	load_language( request, d )
	
	d['pages'] = [ p for p in Page.objects.exclude(slug="legal-notice").filter( language=d['language'] ).order_by(*['sort','id']) ] # menu up. type PAGE should be translated via django trans tamplate tags.
	
	return d

def load_edit_mode( request, d ):
	d['has_edit_mode'] = request.user.groups.filter(name="CONTENT EDITOR").count() != 0
	# check permission
	if not d['has_edit_mode']:
		d['edit_mode'] = False;
		return

	
	# check enable action
	if request.REQUEST.get('enable-edit-mode', None) is not None:
		request.session['edit_mode'] = True
	elif request.REQUEST.get('disable-edit-mode', None) is not None:	
		request.session['edit_mode'] = False

	d['edit_mode'] = request.session['edit_mode'] if request.session.get('edit_mode', False ) else False

	# add editable field
	if d['edit_mode']:
		d['add_page_form'] = AddPageForm( auto_id="id_add_page_%s" )
		d['add_pin_form'] = AddPinForm( auto_id="id_add_pin_%s" )
		d['edit_pin_form'] = EditPinForm( auto_id="id_edit_pin_%s" )
		d['add_enquiry_form'] = AddEnquiryForm( auto_id="id_add_enquiry_%s" )
		
		#d['pageaddform'] = PageAddForm(auto_id="id_page_%s")

#
#   Load language features into view.
#	d is context dictionary
#
def load_language( request, d ):

	from django.utils.translation import activate

	language = request.GET.get('lang', None)

	# default: FR, hack
	d['language'] = language = 'FR'
	activate(language)
	return language


	if language is None:
		# load from somewhere
		language = request.LANGUAGE_CODE
	
	elif language in ['en','fr'] :
		# @todo: a better language match in settings.LANGUAGES
		if hasattr(request, 'session'):
			request.session['django_language'] = language
		else:
			#response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
			activate(language)
	else:
		d['warnings'] = _('language not found')
		language = 'fr'

		d['available_languages'] = settings.LANGUAGES
	d['language'] = language.upper()
	
	return language