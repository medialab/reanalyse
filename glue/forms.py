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
	page_slug = forms.SlugField( required=False )
	parent_pin_slug = forms.SlugField( required=False )