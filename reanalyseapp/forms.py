# -*- coding: utf-8 -*-
###########################################################################################
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms

# for TextInput
from django.forms.widgets import Textarea

# haystack forms
from haystack.forms import *

from reanalyse.reanalyseapp.models import *
###########################################################################################






############################################################
# SIMPLE USER CREATION
class BrowseUserForm(UserCreationForm):
	affiliation = forms.CharField(label=("Affiliation"),max_length=40,required=True)
	def __init__(self, *args, **kwargs):
		super(BrowseUserForm, self).__init__(*args,**kwargs)
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True
	class Meta:
		model = User
		fields = ('username','last_name','first_name','email','affiliation') 
############################################################
# UPDATE USER STATUS FOR ENQUETE
class ExploreUserForm(forms.Form):
	#enqueteid = forms.CharField(label=("Enquete Id"),max_length=20,required=True)
	motivation = forms.CharField(widget=Textarea(attrs={'rows':15,'cols':40,'title':"Motivation"}))
	class Meta:
		fields = ('motivation') 
############################################################
# class UploadFileForm(forms.Form):
# 	#title = forms.CharField(max_length=50)
# 	files  = forms.FileField()
############################################################










from django.forms.widgets import RadioSelect, CheckboxSelectMultiple

#RADIO_CHOICES = ( ('d','doc'), ('s','speak') )
CHECKBOX_CHOICES = ( ('i','interventions'), ('w','wordentities'), ('t','textes') )

# HAYSTACK SEARCH FORMS
############################################################
class SentenceSearchForm(SearchForm):
	# main searchfield
	#q = forms.CharField(required=False, label='chercher:')
	
	#Textes = forms.CharField(required=False)
	rawQuery = forms.BooleanField(required=False)
	autocomplete = forms.BooleanField(required=False)
	autocompletew = forms.BooleanField(required=False)
	#thetype = forms.ChoiceField(required=False, widget=RadioSelect, choices=RADIO_CHOICES)
	
	# to search only in specidied model
	#searchOnly = forms.MultipleChoiceField(required=False, widget=CheckboxSelectMultiple, choices=CHECKBOX_CHOICES)
	
	
	##### DEPRECATED, to do facets or advanced search (by Texte/Speaker)
	#inTextes = forms.ModelMultipleChoiceField(queryset=Texte.objects.all(),widget=forms.CheckboxSelectMultiple(), label='Dans les textes')
	
	#inTextes = forms.ModelMultipleChoiceField(queryset=Texte.objects.all(), label='Dans les textes', required=False)
	#inSpeakers = forms.ModelMultipleChoiceField(queryset=Speaker.objects.all(), label='Participants', required=False)
	
	# trying to change options in certain fields
#	def __init__(self, *args, **kwargs):
		# adding facets parameters a la mano
# 		if kwargs.get('selected_facets') is None:
# 			try:
# 				kwargs['selected_facets'] = args[0].getlist("selected_facets")
# 			except:
# 				donothing=1
# 		super(SearchForm, self).__init__(*args, **kwargs)
			
		#choices = 'ALl Textes'
		#choices = Texte.objects.all()
		#self.fields['inTextes'].queryset = choices 
		
# 	def search(self):
# 		# First, store the SearchQuerySet received from other processing.
# 		sqs = super(MyFacetedSearchForm, self).search()
# 		
# 		#sqs = sqs.filter(content__icontains='et')
# 		
# 		return sqs
############################################################

