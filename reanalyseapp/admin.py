# -*- coding: utf-8 -*-
############################################################
from django.contrib import admin
from reanalyseapp.models import *
from django.db import models
import settings
############################################################



#############################################################
# FOR HTML CONTENTS (editable) 'SiteContent' model
############################################################
class CommonMedia:
	js = (
		'https://ajax.googleapis.com/ajax/libs/dojo/1.6.0/dojo/dojo.xd.js',
		settings.MEDIA_URL+'/js/dojoRichEditor.js',
	)
	css = {
		'all': (settings.MEDIA_URL+'/css/admin.css',),
	}
#############################################################
# class SiteContentAdmin(admin.ModelAdmin):
# 	fieldsets = [
# 		(None,			 { 'fields': ('name','description','contenthtml')}),
# 		#('Description', {'fields': [], 'classes': ['collapse']}),
# 	]
# 	Media = CommonMedia
#############################################################






#############################################################
# ENQUETES, TEXTES, ...
#############################################################
class TexteAdmin(admin.ModelAdmin):
	fields = ('name','contenttxt')
	Media = CommonMedia
#############################################################






#############################################################

#admin.site.register(SiteContent, SiteContentAdmin) # tryout to edit html contents using admin
admin.site.register(Enquete)
admin.site.register(Texte,TexteAdmin)
############################################################



