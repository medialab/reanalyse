from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _

class AddEnquiryForm(forms.Form):
	title_fr = forms.CharField( label=_("french title"),required=True )
	title_en = forms.CharField( label=_("english title"), required=True )
	slug = forms.SlugField( required=True )