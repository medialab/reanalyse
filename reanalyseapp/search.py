# -*- coding: utf-8 -*-
###########################################################################
import logging
import re
from reanalyse.reanalyseapp.models import *

# Simple search tool
from django.db.models import Q
###########################################################################





###########################################################################
def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
	''' Splits the query string in invidual keywords, getting rid of unecessary spaces
		and grouping quoted words together.
		Example:
		
		>>> normalize_query('  some random  words "with   quotes  " and   spaces')
		['some', 'random', 'words', 'with quotes', 'and', 'spaces']
	
	'''
	return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 
def get_query(query_string, search_fields):
	''' Returns a query, that is a combination of Q objects. That combination
		aims to search keywords within a model by testing the given search fields.
	
	'''
	query = None # Query to search for every search term		
	terms = normalize_query(query_string)
	for term in terms:
		or_query = None # Query to search for a given term in each field
		for field_name in search_fields:
			q = Q(**{"%s__icontains" % field_name: term})
			if or_query is None:
				or_query = q
			else:
				or_query = or_query | q
		if query is None:
			query = or_query
		else:
			query = query & or_query
	return query
###########################################################################
def highlightText(content,word):
	outContent=content
	pat=re.compile('('+word+')')
	ff=re.search(pat,outContent)
	if ff!=None:
		part=ff.group(1)
		outContent = re.sub(pat, '<span class="searchResultHighlight">'+part+'</span>', outContent)
	return outContent
###########################################################################
def giveAllContent(texte,query):
	# simple css highlighting for text results
	outContent=texte.content
	for w in normalize_query(query):
		outContent = highlightText(outContent,w)
	d=dict()
	d['name']=texte.name
	d['content']=outContent
	#d['total']= ...
	return [d]
###########################################################################
def giveExcerpts(texte,query):
	resArr=[]
	for w in normalize_query(query):
		wpat=re.compile('(( [^ ]*){,4})'+w+'(( [^ ]*){,4})')
		for u in wpat.finditer(texte.content):
			beg = u.group(1)
			end = u.group(3)
			# add excerpt to result
			d=dict()
			d['name']=texte.name
			d['before']=".."+highlightText(beg,w)
			d['after']=highlightText(end,w)+".."
			d['excerpt']='<span class="searchResultHighlight_excerpt">'+w+'</span>'
			resArr.append(d)
	return resArr
###########################################################################

