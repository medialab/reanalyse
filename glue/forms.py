from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _

class LoginForm(forms.Form):
	username = forms.CharField( label=_('login'), max_length=64 )
	password = forms.CharField( label=_('password'),  max_length=64, widget=forms.PasswordInput(render_value=False ) )


class AddPageForm(forms.Form):
	title_fr = forms.CharField( label=_("french title"),required=True )
	title_en = forms.CharField( label=_("english title"), required=True )
	slug = forms.SlugField( required=True )

class AddPinForm(forms.Form):
	title_fr = forms.CharField( label=_("french title"),required=True )
	title_en = forms.CharField( label=_("english title"), required=True )
	slug = forms.SlugField( required=True )
	page_slug = forms.SlugField( required=False, widget=forms.HiddenInput )
	parent_pin_slug = forms.SlugField( required=False, widget=forms.HiddenInput )

class EditPinForm(forms.Form):
	title = forms.CharField( label=_("title"),required=True )
	abstract = forms.CharField( label=_("abstract"), required=True, widget=forms.Textarea )
	content = forms.CharField( label=_("content"), required=True, widget=forms.Textarea )

class UploadPinForm(forms.Form): # an upload form without file :D (upload via ajax)
	page_slug = forms.SlugField( required=False, widget=forms.HiddenInput )
	parent_pin_slug = forms.SlugField( required=False, widget=forms.HiddenInput )