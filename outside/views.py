#!/usr/bin/python
# -*- coding: utf-8 -*-


import urllib, os


from django.core import serializers
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

from reanalyseapp.models import Enquete, Tag, Texte, AccessRequest

from glue.models import Pin, Page
from glue.forms import AddPageForm, AddPinForm, EditPinForm

from outside.models import Enquiry, Subscriber, Confirmation_code 
from outside.sites import OUTSIDE_SITES_AVAILABLE
from outside.forms import LoginForm, AddEnquiryForm, SubscriberForm, SignupForm, AccessRequestForm, ChangePasswordForm, ReinitializePasswordForm

from django.core.mail import EmailMultiAlternatives

from django.core.urlresolvers import reverse

from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.cache import cache

#TEI PART

from reanalyseapp.utils import *
from reanalyseapp.models import *
from reanalyseapp.imexport import *
from reanalyseapp.forms import *
from reanalyseapp.visualization import *
from reanalyseapp.search import *

# Search with haystack
from haystack.views import *
from haystack.forms import *
from haystack.query import *



# settings.py
LOGIN_URL = '/%s/login/' % settings.ROOT_DIRECTORY_NAME

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
	
	
	
	if request.user.is_authenticated():
	
		subscriber = Subscriber.objects.get(user=request.user.id)
		#Fill form with user infos
		data['subscriber_form'] = SubscriberForm( auto_id="id_subscriber_%s", initial={'email': subscriber.user.email,
																		'username': request.user.username,
																		'first_name': request.user.first_name,
																		'last_name': request.user.last_name,
																		'affiliation': subscriber.affiliation,
																		'status': subscriber.status,
																		'action':'ADD'
																		} )
	else:
		data['subscriber_form'] = SubscriberForm(auto_id="id_subscriber_%s",  initial={'action':'ADD'})
	
	
	return render_to_response("%s/contacts.html" % data['template'], RequestContext(request, data ) )


def page( request, page_slug ):
	data = shared_context( request, tags=[ page_slug ] )
	data['page'] = get_object_or_404(Page, slug=page_slug, language=data['language'] )
	data['pins'] = Pin.objects.filter( page__slug=page_slug, language=data['language'], parent=None)

	return render_to_response("%s/page.html" % 'enquete', RequestContext(request, data ) )

def enquete( request, enquete_id ):
	data = shared_context( request, tags=[ "enquetes", "focus-on-enquete", 'visualizations' ] )
	data['enquete'] = get_object_or_404( Enquete, id=enquete_id )
	data['disabled'] =  [ t.slug for t in data['enquete'].tags.filter( type=Tag.DISABLE_VISUALIZATION ) ]
	
	try:
		data['enquiry'] = Enquiry.objects.get( enquete=enquete_id, language=data['language'] )
	except Enquiry.DoesNotExist,e:
		pass
		# data['enquiry'] = None


	return render_to_response('enquete/enquete.html', RequestContext(request, data ) )


"""
if(  settings.REANALYSEURL == 'http://bequali.fr' ) :
	messages.add_message(request, messages.ERROR, 'Cette enquête n\'est pas encore consultable')
	viewurl = reverse('outside.views.enquetes')
	return redirect(viewurl)
	
else :
	return render_to_response('enquete/enquete.html', RequestContext(request, data ) )
"""

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
#@permission_required('reanalyseapp.can_browse')
def enquete_download( request, enquete_id ):
	#Check if the user has access to the files
	
	if( not request.user.has_perm('reanalyseapp.can_browse') ):

		try:
	   		AccessRequest.objects.get(user=request.user.id, enquete=enquete_id, is_activated=True)
	   		
	   		
		except AccessRequest.DoesNotExist:
			
			request.flash['notice'] =  _("You don't have access to this document, please ask for access <a class='blue-link' href='%s'>here</a> to ask for permission.") % ( reverse('outside.views.access_request', kwargs={'enquete_id':enquete_id}) )

			viewurl = reverse('outside.views.enquete', kwargs={'enquete_id':enquete_id})
			return redirect(viewurl)
		else:
			pass
	else:
		pass
	
	enquete = get_object_or_404( Enquete, id=enquete_id )
	
	import zipfile, zlib

	zippath = os.path.join( "/tmp/", "enquete_%s.zip" % enquete.id )

	zf = zipfile.ZipFile( zippath, mode='w' )
	
	
	
	for t in Texte.objects.filter( enquete=enquete ):	

		if('é'.decode('utf-8') in t.locationpath):
		    
		    t.locationpath= t.locationpath.replace('é'.decode('utf-8'), 'e')
		   
		
		if os.path.isfile(t.locationpath.decode('utf-8')):
		    
		    if( t.locationpath.find('_ol.') or t.locationpath.find('_dl.') ):
				
				zf.write( t.locationpath, compress_type=zipfile.ZIP_DEFLATED, 
							arcname= t.locationpath.split('/', 7)[7])

		
	response = HttpResponse( open( zippath , 'r' ) , content_type="application/gzip"  )
	response['Content-Description'] = "File Transfer";
	response['Content-Disposition'] = "attachment; filename=enquete-%s.zip" % ( enquete.id ) 
	
	return response




@login_required( login_url=LOGIN_URL )
#@permission_required('reanalyseapp.can_browse')
def document( request, document_id ):
	
	data = shared_context( request, tags=[ "enquetes","metadata" ] )

	data['document'] = document = get_object_or_404( Texte, id=document_id )
	
	
	
	locationpath = str(document.locationpath)
	data['document'].spec_id = locationpath.split('/')[-1].replace('_', ' _ ')

	
	
	data['enquete'] = enquete = document.enquete
	data['mimetype'] = guess_type( document.locationpath )[0]
	
	data['document'].locationpath = data['document'].locationpath.split('/', 5)[5]
	
	###### ANY DOCUMENT
	e = Enquete.objects.get(id=document.enquete.id)
	texte = Texte.objects.get(id=document_id)
	ctx = {'enquete':texte.enquete,'texte':texte,'bodyid':'e','pageid':'documents'}
	
	######################################### TEI
	if texte.doctype=='TEI':
	
		###### RELATED VIZ
		# we can take all related viz if we want
		#ctx.update({'visualizations':getRelatedViz(textes=[texte])})
		# now testing with only the textstreamtimeline
		try:
			streamtimelineviz = Visualization.objects.get(textes=texte,viztype='TexteStreamTimeline')
		except:
			try:
				streamtimelineviz = Visualization.objects.filter(textes=texte,viztype='TexteStreamTimeline')[0]
			except:
				streamtimelineviz = None
		ctx.update({'visualization':streamtimelineviz})
	
		maxTextPart = texte.sentence_set.aggregate(Max('i')).values()[0]
		
		if request.GET.get('highlight'):
			ctx.update({'highlight':request.GET.get('highlight')})
		
		if request.GET.get('around'):
			around = int(request.GET.get('around'))
			minPart = max(0,around-2)
			maxPart = min(maxTextPart,around+2)
		else:
			minPart = request.GET.get('from',0)
			maxPart = request.GET.get('to',maxTextPart)
			
		ctx.update({'minpart':minPart,'maxpart':maxPart,'totalmaxparts':maxTextPart})
		
		### CODES_PARAVERBAL DICT FOR LEGEND (see globalvars)
		
		
		newPARVBCODES={}
		newPARVBCODES['Transcription'] = 	['comment']
		newPARVBCODES['Verbatim'] = 		[]
		
		newPARVBCODES={}
		newPARVBCODES['Transcription'] = 	[]
		newPARVBCODES['Verbatim'] = 		[]
		
		

		#return HttpResponse(f, 'text')
		
		for code,label,css in PARVBCODES['Verbatim'] :
			
			import commands
			
			a = commands.getoutput('grep -l %s %s' % (code, texte.locationpath) )
			

			if(a != ""):
				 newPARVBCODES['Verbatim'] += [[code, label, css]]

			   
				
		for code,label,css in PARVBCODES['Transcription'] :
			
			a = commands.getoutput('grep -l %s %s' % (code, texte.locationpath) )
			
			if(a != ""):
			    newPARVBCODES['Transcription'] += [[code, label, css]]
		
		
	
		ctx.update({'paraverbal':newPARVBCODES})	
		#ctx.update({'paraverbal':PARVBCODES})	
		
		### CODES_TREETAGGER DICT FOR display
		ctx.update({'codes_treetagger':CODES_TREETAGGER})
		
		### COLORS FOR SPEAKERS
		speakersColors = getRandomSpeakersColorsDict(e,texte)
		ctx.update({'speakersColors':speakersColors})
		
		### SPEAKERS
		inv = texte.speaker_set.filter(ddi_type="INV")
		spk = texte.speaker_set.filter(ddi_type="SPK")
		pro = texte.speaker_set.filter(ddi_type="PRO")
		
		
		ctx.update({'speakers':{'inv':inv,'spk':spk,'pro':pro}})

	#return HttpResponse(document.locationpath, 'text')
	
	if( not request.user.has_perm('reanalyseapp.can_browse') ):
		
	
		#Check if the user has access to the files
		try:
	   		req = AccessRequest.objects.get(user=request.user.id, enquete=document.enquete.id, is_activated=True)
		   
			
		except AccessRequest.DoesNotExist:
			
			
			viewurl = reverse('outside.views.enquete', kwargs={'enquete_id':document.enquete.id})
			
			request.flash['notice'] =  _("You don't have access to this document, please ask for access <a class='blue-link' href='%s'>here</a> to ask for permission.") % ( reverse('outside.views.access_request', kwargs={'enquete_id':document.enquete.id}) )
			
			return redirect(viewurl)
		else:
			pass
	
	else:
	
		pass
	
	
	
	
	return render_to_response('enquete/document.html',ctx, RequestContext(request, data ) )

	

	
	
	"""
	from lxml import etree
	
	
	
	
	if(document.doctype == "TEI"):
		
		try:
			xml_input = etree.parse(document.locationpath)
			xslt_root = etree.parse("/var/opt/reanalyse/static/xsl/tei.xsl")
			transform = etree.XSLT(xslt_root)
			
			#return HttpResponse( str(transform(xml_input)) , mimetype='texte'  )
			
		except Exception, e:
			return HttpResponse( str(e) , mimetype='application/xml'  )
			
		else:
			return render_to_response('enquete/document.html', {'xslt_render':transform(xml_input)}, RequestContext(request, data ) )
		
	
	return render_to_response('enquete/document.html', RequestContext(request, data ) )"""


@login_required( login_url=LOGIN_URL )
#@permission_required('reanalyseapp.can_browse')
def document_download( request, document_id ):
	data = shared_context( request )
	document = get_object_or_404( Texte, id=document_id )
	
	
	if( not request.user.has_perm('reanalyseapp.can_browse') ):
	
		#Check if the user has access to the files
		try:
	   		AccessRequest.objects.get(user=request.user.id, enquete=document.enquete.id, is_activated=True)
		except AccessRequest.DoesNotExist:
			
			request.flash['notice'] =  _("You don't have access to this document, please ask for access <a class='blue-link' href='%s'>here</a> to ask for permission.") % ( reverse('outside.views.access_request', kwargs={'enquete_id':document.enquete.id}) )
			viewurl = reverse('outside.views.enquete', kwargs={'enquete_id':document.enquete.id})
			return redirect(viewurl)
		else:
			pass
	
	else:
		pass
	
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
#@permission_required('reanalyseapp.can_browse')
def document_embed( request, document_id ):
	data = shared_context( request )
	document = get_object_or_404( Texte, id=document_id )
	mimetype = guess_type( document.locationpath )[0]

	
	if( not request.user.has_perm('reanalyseapp.can_browse') ):
		
		#Check if the user has access to the files
		try:
	   		AccessRequest.objects.get(user=request.user.id, enquete=document.enquete.id, is_activated=True)
		except AccessRequest.DoesNotExist:
			
			request.flash['notice'] =  _("You don't have access to this document, please ask for access <a class='blue-link' href='%s'>here</a> to ask for permission.") % ( reverse('outside.views.access_request', kwargs={'enquete_id':document.enquete.id}) )
			
			viewurl = reverse('outside.views.enquete', kwargs={'enquete_id':document.enquete.id})
			return redirect(viewurl)
		else:
			pass
	else:
		pass


	try:
		extension = guess_extension( mimetype )
		content_type = mimetype
	except AttributeError, e:
		filetitle, extension = os.path.splitext( document.locationpath )
		content_type = "application/octet-stream"
	
	return HttpResponse( open( document.locationpath , 'r' ) , mimetype=content_type  )
	

from django.utils import simplejson



def enquiry( request, enquete_id ):
	data = shared_context( request, tags=[ "enquetes","enquiry" ] )
	
	try:
		data['enquiry'] = Enquiry.objects.get( enquete__id=enquete_id, language=data['language'])
		
	except Enquiry.DoesNotExist:
		request.flash['notice'] =  _("There is no research on this research")
			
		return redirect(reverse('outside.views.enquetes'))
	else:
		data['enquete'] = data['enquiry'].enquete
		data['sections'] = data['enquiry'].pins.order_by(*["sort","-id"])
		
		
		
		data['j_sections'] = serializers.serialize("json", data['enquiry'].pins.order_by(*["sort","-id"]))

		
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
	
	if request.user.is_authenticated():
		return redirect( reverse('outside_index') )
	
	
	form = LoginForm( request.POST )
	login_message = { 'next':request.REQUEST.get('next', 'outside_index') }
	
	
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
					
					
					# @todo: Redirect to next page
					#return redirect( settings.REANALYSEURL+'/'+settings.ROOT_DIRECTORY_NAME )
					
					
					
					next_url = request.session['next']
					
					del request.session['next']
					
					#return HttpResponse(next_url)
					
					return redirect( next_url )
						#return redirect( settings.REANALYSEURL+request.GET['next'] )

					
						
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


def access_request(request, enquete_id=None):
	
	data = shared_context( request, tags=[ "enquetes", "access_request" ] )
	
	if enquete_id is not None:
		data['enquete'] = get_object_or_404( Enquete, id=enquete_id )
	data['enquetes'] = Enquete.objects.all()
		
	
	#If connected ...
	if not request.user.is_authenticated():
		return redirect(LOGIN_URL+'?next='+reverse('outside.views.access_request', kwargs={'enquete_id':enquete_id}))
	else:
		
		#Verify if he has already requested the enquete
		try:
	   		access = AccessRequest.objects.get(user=request.user.id, enquete=enquete_id)
	   		
	   		
		except AccessRequest.DoesNotExist:
			
			try:
				subscriber = Subscriber.objects.get(user=request.user.id)
			except Subscriber.DoesNotExist:
				pass
			
				#redirect to creation profileS
			
			else:
				
				#Fill form with user infos
				data['access_request_form'] = AccessRequestForm( auto_id="id_access_request_%s", initial={'email': subscriber.user.email,
																				'username': request.user.username,
																				'first_name': request.user.first_name,
																				'last_name': request.user.last_name,
																				'affiliation': subscriber.affiliation,
																				'status': subscriber.status,
																				'enquete': enquete_id 
																				} )
				
				data['access_request_form']['enquete'].editable = False
		
		else:
			
			
			viewurl = reverse('outside.views.enquete', kwargs={'enquete_id':enquete_id})
			if(access.is_activated == True):
				error_str = _('You already have access to this research.')
			else:
				error_str = _('You already asked for this research, you will be notified when your access is granted.')

			
			request.flash['notice'] = error_str
			
			return redirect(viewurl)
		
		
		return render_to_response("enquete/access_form.html", RequestContext(request, data ) )


def signup( request, enquete_id=None ):
	
	if enquete_id is not None:
		data = shared_context( request, tags=[ "enquetes", "signup" ] )
	
		data['enquete'] = get_object_or_404( Enquete, id=enquete_id )
	else:
		data = shared_context( request, tags=[ "signup" ] )
	
	data['signup_form'] = SignupForm(  auto_id="id_signup_%s" )

	# load all pins without page (aka news)
	# data['pins'] = Pin.objects.filter(language=data['language'], page__isnull=True ).order_by("-id")
	
	return render_to_response("%s/signup.html" % data['template'], RequestContext(request, data ) )



def confirm( request, token, user_id, action ):
	import string
	import random
	
	def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for x in range(size))
	
	subscriber = get_object_or_404( Subscriber, user__id=user_id )
	confirmation_code = get_object_or_404( Confirmation_code, code=token, action=action, activated = True )
	
	
	data = shared_context( request, tags=[ "confirm" ] )
	
	if(action == 'signup'):
	
		subject, from_email, to = _("Signup request"), _("Bequali Team")+"<equipe@bequali.fr>", settings.EMAIL_ADMINS
		
		path = '%s%s' % (settings.REANALYSEURL, reverse('admin:auth_user_change', args=[subscriber.user.id]) )
		
		html_content = render_to_string('email/signup.html', 
											{'action':'admin_notification',
											'prenom': subscriber.first_name,
											'nom': subscriber.last_name,
											'email': subscriber.user.email,
											'affiliation': subscriber.affiliation,
											'status': unicode(dict(Subscriber.STATUS_CHOICES)[subscriber.status], 'utf-8'),
											'description': subscriber.description,
											'admin_url' : path})

		text_content = html_content.replace('<br/>', '\n')
	
		msg = EmailMultiAlternatives(subject, text_content, from_email, to)
		msg.attach_alternative(html_content, 'text/html')
		msg.content_subtype = 'html'
		
		
		msg.send()
		
		confirmation_code.activated = False
		
		confirmation_code.save()
		
		user = subscriber.user
		
		user.is_active = True
		
		user.save()
			
	elif (action == "reinitPass") :
			
		subject, from_email, to = _("beQuali password reinitialization"), _("Bequali Team")+"<equipe@bequali.fr>", subscriber.user.email
		
		login_view = reverse('outside.views.login_view')
		change_password_view = reverse('outside.views.change_password')
		login_url = '%s%s' % (settings.REANALYSEURL, login_view )
		change_password_url = '%s%s' % (settings.REANALYSEURL, change_password_view )
		
		rand_pass = id_generator()
		
		user = subscriber.user
		user.set_password(rand_pass)
		user.save()

		html_content = render_to_string('email/reinitialize_password.html', 
											{'action':'reinitialize_notification',
											'username':subscriber.user.username,
											'prenom': subscriber.first_name,
											'password':rand_pass,
											'nom': subscriber.last_name,
											'login_url' : login_url,
											'change_password_url': change_password_url,})
	
		text_content = html_content.replace('<br/>', '\n')
	
	
	
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, 'text/html')
		msg.content_subtype = 'html'
				
		msg.send()
		
		confirmation_code.activated = False
		confirmation_code.save()
		
	data['action'] = action
	data['email'] = subscriber.user.email

	return render_to_response("%s/confirm.html" % data['template'], RequestContext(request, data ) )
		


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
	d['REANALYSEURL'] = settings.REANALYSEURL
	d['next'] = request.path


	# if it is not auth, pull loginform
	if request.user.is_authenticated():
		load_edit_mode( request, d )
	else:
		d['login_form'] = LoginForm()


	# load language and share it inside context
	load_language( request, d )
	
	d['pages'] = [ p for p in Page.objects.exclude(slug="legal-notice").filter( language=d['language'], activated=True ).order_by(*['sort','id']) ] # menu up. type PAGE should be translated via django trans tamplate tags.
	
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



@login_required( login_url=LOGIN_URL )
def change_password(request):
	data = shared_context( request, tags=[ "form", "change_password" ] )
	data['change_password_form'] = ChangePasswordForm(  auto_id="id_change_password_%s", initial={'username': request.user.username} )
	
	data['change_password_form']['username'].editable = False;

	return render_to_response("hub/change_password.html", RequestContext(request, data ) )
	
	"""message = 'Change Password'
	pForm = ChangePasswordForm()

	if request.method == 'POST':
		if request.POST['submit'] == 'Change':
			postDict = request.POST.copy()
			pForm = LoginForm(postDict)
			if pForm.is_valid():
				uPass1 = request.POST['password']
				uPass2 = request.POST['password1']
				if uPass1 == uPass2:
					user = get_object_or_404(Employee.objects.get(name__exact= request.session['uid']))
					#user = request.session['uid']
					print 'User: ' + user
					user.set_password(uPass1)
					user.save()
					return HttpResponseRedirect(next)
				else:
					message = 'Passwords dont match'
					pForm = ChangePasswordForm()
	
	return render_to_response('employee/change_password.html', {
	                                  'pForm': pForm,
	                                  'message': message })"""




@login_required( login_url=LOGIN_URL )
def edit_profile(request):
	data = shared_context( request, tags=[ "form", "edit_profile" ] )
	form = SubscriberForm( auto_id="id_subscriber_%s")
	
	
	subscriber = Subscriber.objects.get(user=request.user.id)
	#Fill form with user infos
	data['edit_profile_form'] = SubscriberForm( auto_id="id_edit_profile_%s", initial={'email': subscriber.user.email,
																	'first_name': subscriber.first_name,
																	'last_name':subscriber.last_name,
																	'email':subscriber.email,
																	'affiliation':subscriber.affiliation,
																	'status':subscriber.status,
																	'description':subscriber.description,
																	'action':'EDIT',
																	} )
	
	
	return render_to_response("hub/edit_profile.html", RequestContext(request, data ) )



@login_required( login_url=LOGIN_URL )
def create_profile(request):
	
	#return HttpResponse( request.user.id, mimetype='texte'  )
	
	try:
		subscriber = Subscriber.objects.get(user=request.user.id)
	
	except Subscriber.DoesNotExist:
		
		data = shared_context( request, tags=[ "form", "create_profile" ] )
		form = SubscriberForm( auto_id="id_subscriber_%s")
		
		#Fill form with user infos
		data['create_profile_form'] = SubscriberForm( auto_id="id_subscriber_%s", initial={'action':'ADD'})
	
	else:
		request.flash['notice'] =  _("You already have a profile")
		
		return redirect( request.REQUEST.get('next', 'outside_index') )
	
	
	return render_to_response("hub/create_profile.html", RequestContext(request, data ) )
	
	
def reinitialize_password(request):
	data = shared_context( request, tags=[ "form", "reinitialize_passwd" ] )
	
	data['reinitialize_password_form'] = ReinitializePasswordForm(auto_id="id_reinitialize_password_%s")
	
	return render_to_response("hub/reinitialize_passwd.html", RequestContext(request, data ) )
	
	
	

def download_page( request, enquete_id ):

	data = shared_context( request, tags=[ "download" ] )
	
	if( not request.user.has_perm('reanalyseapp.can_browse') ):
		try:
	   		AccessRequest.objects.get(user=request.user.id, enquete=enquete_id, is_activated=True)
		except AccessRequest.DoesNotExist:
			
			request.flash['notice'] =  _("You don't have access to this document, please ask for access <a class='blue-link' href='%s'>here</a> to ask for permission.") % ( reverse('outside.views.access_request', kwargs={'enquete_id':enquete_id}) )
			
			viewurl = reverse('outside.views.enquete', kwargs={'enquete_id':enquete_id})
			return redirect(viewurl)
	else:
		pass
	
	if enquete_id is not None:
		data['enquete'] = get_object_or_404( Enquete, id=enquete_id )
	data['dl_link'] = reverse('outside_enquete_download', args=[enquete_id])
	return render_to_response("hub/download.html", RequestContext(request, data ) )


def evGetJson(request,eid,vid):
	v = Visualization.objects.get(enquete__id=eid,id=vid)
	return HttpResponse(v.json, mimetype="application/json")
###########################################################################

@login_required
def evSaveHtml(request,eid,vid):
	
	v = Visualization.objects.get(enquete__id=eid,id=vid)
	
	thehtml = request.POST
	v.contenthtml = thehtml
	v.save()
	return HttpResponse("done", mimetype="application/json")

from django.views.decorators.cache import cache_page


def dGetHtmlContent(request,eid,did):

	texte = Texte.objects.get(id=did)
	sStart = request.GET.get('from',0)
	sEnd = request.GET.get('to',0)
	
	key = "timeparts_%s_%s" % ( eid, did )
	
	timeparts = cache.get(key)
	
	if (timeparts == None) :
	  timeparts = getTextContent(texte,sStart,sEnd)
	  cache.set(key, timeparts, 1000)
	

	if request.GET.get('highlight'):
		ctx.update({'highlight':request.GET.get('highlight')})
	
	ctx={'timeparts':timeparts}
	
	return render_to_response('bq_render_d.html', ctx, context_instance=RequestContext(request))
###################################################################################################################################
	


@login_required
def enquete_admin(request):
    ### unique foldername if some upload is done 
    sessionFolderName = "up_"+str(time())
    ctx = {'bodyid':'admin','foldname':sessionFolderName}
    """
    ### todo: move that somewhere else to do it just when website/database is reset
    try:
        init_users()
    except:
        donothing=1
    
    ### check if solr launched, relaunch it if needed
    if checkSolrProcess():
        ctx.update({'solrstatus':'was off. but refreshing this page has relaunched it. wait 5,7s and refresh again to be sure'})
    else:
        ctx.update({'solrstatus':'is running !'})
    ctx.update({'staffemail':settings.STAFF_EMAIL})
    
    ### log file
    #logger.info("Looking at ADMIN page")
    wantedCount = int(request.GET.get('log','50'))
    log_django     = getTailOfFile(settings.REANALYSELOGDJANGO,wantedCount)
    #log_solr     = getTailOfFile(settings.REANALYSELOGSOLR,wantedCount)
    ctx.update({'log_django':log_django})
        
    ### solr path
    ctx.update({'BASE_URL':settings.BASE_URL,'solr_url':settings.SOLR_URL})
    """
    ### all enquetes
    ctx.update({'enquetes':Enquete.objects.all()})
    """
    ### default page is 'users'
    ctx.update({'page':request.GET.get('page','users')})
    
    ### static pages : (they are also loaded one at at time on the home page) load them all now
    for name in ['project','method','access']:
        for lan in ['en','fr']:
            nothing = getStaticHtmlContent(name,lan)
    
    ### users
    users={}
    users['header']=['username','name','email','status','group','full study access','joined','last login']
    users['rows']=[]
    for u in User.objects.order_by('id'):
        uTab=[]
        uTab.append('<a href="'+settings.BASE_URL+'admin/auth/user/'+str(u.id)+'">'+u.username+'</a>')
        uTab.append(u.last_name +" "+ u.first_name)
        uTab.append(u.email)
        # STATUS (activated?)
        sstr="need to be activated..."
        if u.is_active:
            sstr="activated"
        uTab.append(sstr)
        # GROUPS
        gstr=""
        if u.is_staff:
            gstr="STAFF "
        for g in u.groups.all():
            gstr+=g.name+" "
        uTab.append(gstr)
        # PERMISSIONS
        pstr=""
        for e in Enquete.objects.order_by('id'):
            if u.has_perm('reanalyseapp.can_explore_'+str(e.id)):
                pstr+="["+str(e.id)+"] "+e.name+"<br/>"        
        uTab.append(pstr)
        # DATES JOINED LASTLOGIN
        uTab.append(u.date_joined.strftime("%a %x"))
        uTab.append(u.last_login.strftime("%a %d at %Hh%M"))
        users['rows'].append(uTab)
    ctx.update({'users':users})
    """
    ### upload of available studies
    
    
    
    serverAvailableStudies = []
    for foldername in os.listdir(settings.REANALYSESAMPLE_STUDIES_FILES):
        #logger.info("Listing existing study folder: "+foldername)
        serverAvailableStudies.append({'foldername':foldername})
    ctx.update({'serverAvailableStudies':serverAvailableStudies})
    
    
    data = shared_context( request, tags=[ "enquete_admin" ] )
    ctx.update({'data':data})
    
    return render_to_response('enquete/enquete_admin.html', ctx , context_instance=RequestContext(request, data))

	
	