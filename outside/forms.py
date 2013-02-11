from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from captcha.fields import ReCaptchaField
from outside.models import Subscriber


class AddEnquiryForm(forms.Form):
	title_fr = forms.CharField( label=_("french title"),required=True )
	title_en = forms.CharField( label=_("english title"), required=True )
	enquete = forms.IntegerField( label=_("enquete id"), required=True, widget=forms.HiddenInput )
	slug = forms.SlugField( required=True )


class SubscriberForm (forms.Form):
	first_name = forms.CharField( max_length = 64 ) # longer than standard field
	last_name = forms.CharField( max_length = 64 ) # longer than standard field
	email = forms.EmailField()
	affiliation = forms.CharField( max_length = 128, required=False )
	status = forms.CharField(max_length=3, widget=forms.Select(choices=Subscriber.STATUS_CHOICES))
	accepted_terms = forms.BooleanField()
	description = forms.CharField( widget=forms.Textarea) # personal description
	captcha = ReCaptchaField(attrs={'theme':'clean'})

    
class LoginForm( forms.Form ):
	username = forms.CharField( max_length=32, widget=forms.TextInput )
	password = forms.CharField( max_length=64, label='Password', widget=forms.PasswordInput(render_value=False ) )
	
	
	
class SignupForm( forms.Form ):
    first_name = forms.CharField( max_length = 64,  ) # longer than standard field
    last_name = forms.CharField( max_length = 64,  ) # longer than standard field
    
    #username = forms.CharField( max_length=32, widget=forms.TextInput,  )
    
    password = forms.CharField( max_length=64, label='Password', widget=forms.PasswordInput(render_value=False ),  required=True )
    #password2 = forms.CharField( max_length=64, label='Password2', widget=forms.PasswordInput(render_value=False ), required=True )
    
    email = forms.EmailField()
    
    affiliation = forms.CharField( max_length = 128, required=True,  )
    status = forms.CharField(max_length=3, widget=forms.Select(choices=Subscriber.STATUS_CHOICES), )
    accepted_terms = forms.BooleanField(initial=1)
    
    message = forms.CharField( widget=forms.Textarea) # personal message

    captcha = ReCaptchaField(attrs={'theme':'clean'})
    
    

    