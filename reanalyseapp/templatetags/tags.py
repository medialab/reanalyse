# -*- coding: utf-8 -*-
from reanalyse.reanalyseapp.models import *
from reanalyse.reanalyseapp.utils import *

from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()
####################################################################
# don't forget to add {% load tags %} in the template
####################################################################




###########################################################################    
# simple counts (for left main menu)
@register.filter
def vizPublicCount(e):
	return e.visualization_set.filter(public=True).count()
@register.filter
def docPublicCount(e):
	return e.texte_set.filter(Q(doccat='analyse')|Q(doccat='preparatory')|Q(doccat='verbatim')|Q(doccat='publication')).count()
@register.filter
def spkPublicCount(e):
	return e.speaker_set.filter(ddi_type='SPK').count()
###########################################################################    
# to get speaker description ON THE LEFT
@register.filter
def speakerDescription(s):
	try:
	    return s.attributes.get(attributetype__name='description').name
	except:
	   	return 'error fetching description'
###########################################################################
# to get speaker description AT BEGINNING
@register.filter
def speakerMeta(s):
	try:
		return s.attributes.get(attributetype__name='description').name
# 		if s.ddi_type=='INV':
# 			return speakerDescription(s)
# 		else:
# 			st=s.attributes.get(attributetype__name='Sexe').name
# 			st+=", "+s.attributes.get(attributetype__name='Age').name+"ans"
# 			st+=", "+s.attributes.get(attributetype__name='_profession_enquete').name
# 			st+=", "+s.attributes.get(attributetype__name='Lieu').name
# 			return st
	except:
		return 'error fetching meta for speaker'
###########################################################################
# to get enquete author (ebrowse,e_base)
@register.filter
def enqueteMeta(e,typ):
	try:
		fieldcat = typ.split('/')[0]
		field = typ.split('/')[1]
	except:
		return "[meta-need-fieldcat/field]"
	try:
		return e.meta()['values'][fieldcat][field]['value'][0]
	except:
		return "[meta-"+fieldcat+"/"+field+"]"
###########################################################################



###########################################################################
@register.filter
def canExploreEnquete(user,eid):
	return user.has_perm('reanalyseapp.can_explore_'+str(eid))
###########################################################################


###########################################################################
# to get html tags from txtcontent
@register.filter
@stringfilter
def textToHtml(s):
	return makeHtmlFromText(s)
####################################################################
# to change haystack-result-highlighted style
@register.filter
@stringfilter
def replaceEmByClassedDiv(s):
	p = re.compile('em>') 
	for f in p.findall(s): 
		s = s.replace(f, 'div>')
	p = re.compile('<div>') 
	for f in p.findall(s): 
		s = s.replace(f, '<div class="result_highlighted">')
	return s
####################################################################
# to change haystack-result-highlighted style
@register.filter
@stringfilter
def highlighthtml(html,highlight):
	res=html
	logging.info("rawtext:"+res)
	words=highlight.split(" ")
	for w in words:
		p=re.compile('((>|^)[^<]* ('+w+') [^>]*(<|$))',flags=re.IGNORECASE)
		for part in re.findall(p,res):
			morc = part[0]
			w = part[2]
			logging.info("tagfunc:"+morc+" === "+w)
			nmorc = morc.replace(w,'<div class="result_highlighted">'+w+'</div>')
			res=re.sub(morc,nmorc,res)
	return res
####################################################################






# For information : a custom highlighter tag method
####################################################################
# class MyHighlighter(Highlighter): 
# 	def render_html(self, highlight_locations=None, start_offset=None, end_offset=None): 
# 		# Prepare the highlight template 
# 		if self.css_class: 
# 			hl_start = '<%s class="%s">' % (self.html_tag, self.css_class) 
# 		else: 
# 			hl_start = '<%s>' % (self.html_tag) 
# 		hl_end = '</%s>' % self.html_tag 
# 		hl_tag = hl_start + '%s' + hl_end 
# 		highlighted = self.text_block 
# 		for word in self.query_words: 
# 			# preserve original case when replacing 
# 			p = re.compile(word, re.IGNORECASE) 
# 			for f in p.findall(highlighted): 
# 				rep = hl_tag % f 
# 				highlighted = highlighted.replace(f, rep) 
# 		return highlighted 
####################################################################




# DEPRECATED ?
# ####################################################################
# @register.filter
# def lookmydic(arr,ky):
# 	try:
# 		for u in arr:
# 			if u[0]==ky:
# 				return u[1]
# 	except:
# 		return "novalue for this key"
# ####################################################################
# @register.filter
# @stringfilter
# def goodstatus(textArray,value):
# 	out=[]
# 	for t in textArray:
# 		out.append(t)
# 	return out
# ####################################################################
