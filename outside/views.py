from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth import login, logout, authenticate
from glue.forms import LoginForm, AddPageForm, AddPinForm


from reanalyseapp.models import Enquete
from glue.models import Pin, Page

#
#    Outside
#    =======
#
def index( request ):
	data = shared_context( request, tags=[ "index" ] )
	
	# load all pins without page, without Enquete
	data['pins'] = Pin.objects.filter(language=data['language'])

	return render_to_response('outside/index.html', RequestContext(request, data ) )

def page( request, page_slug ):
	data = shared_context( request, tags=[ "page" ] )
	return render_to_response('outside/index.html', RequestContext(request, data ) )

def enquete( request, enquete_id ):
	data = shared_context( request, tags=[ "enquete" ] )
	data['enquete'] = get_object_or_404( Enquete, id=enquete_id )

	return render_to_response('outside/enquete.html', RequestContext(request, data ) )

def enquetes( request ):
	data = shared_context( request, tags=[ "enquete" ] )
	data['enquetes'] = Enquete.objects.all() 

	return render_to_response('outside/enquetes.html', RequestContext(request, data ) )

def login_view( request ):
	
	form = LoginForm( request.POST )
	login_message = { 'next':request.REQUEST.get('next', 'outside_index') }

	if form.is_valid():
		user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
		if user is not None:
			if user.is_active:
				login(request, user)
				# @todo: Redirect to next page
				return redirect( 'outside_index' )
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

	# if it is not auth, pull loginform
	if request.user.is_authenticated():
		load_edit_mode( request, d )
	else:
		d['login_form'] = LoginForm()


	# load language and share it inside context
	load_language( request, d )
	

	d['pages'] = [ p for p in Page.objects.filter( language=d['language'] ).order_by('-id') ] # menu up. type PAGE should be translated via django trans tamplate tags.
	
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
		d['add_page_form'] = AddPageForm()
		d['add_pin_form'] = AddPinForm()
		#d['pageaddform'] = PageAddForm(auto_id="id_page_%s")

#
#   Load language features into view.
#	d is context dictionary
#
def load_language( request, d ):
	language = request.GET.get('lang', None)

	if language is None:
		# load from somewhere
		language = request.LANGUAGE_CODE
	
	elif language in ['en','fr'] :
		# @todo: a better language match in settings.LANGUAGES
		if hasattr(request, 'session'):
			request.session['django_language'] = language
		else:
			#response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
			translation.activate(language)
	else:
		d['warnings'] = _('language not found')
		language = 'fr'

		d['available_languages'] = settings.LANGUAGES
	d['language'] = language.upper()
	
	return language