# -*- coding: utf-8 -*-
###########################################################################
import settings
import re
from reanalyse.reanalyseapp.models import *
from django.core import serializers
from xml.etree.ElementTree import ElementTree
# to randomly sort an array : random.shuffle(arr)
import random
# tfidf math things
import math

# custom OR queries
from django.db.models import Q

# for unzip class made by Doug Tolton (see bottom) - used during upload in the views.py
import os, zipfile

###########################################################################
# LOGGING
###########################################################################
import logging
logger = logging.getLogger('apps')
class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())
###########################################################################







###########################################################################
# COLORS
###########################################################################
# "#648484" to [R,G,B]
def htmlColorToRgb(c):
    split = (c[1:3], c[3:5], c[5:7])
    return [int(x, 16) for x in split]
###########################################################################
def randomizeSpeakersColors(e):
	for s in e.speaker_set.all():
		i = int(len(HTML_COLORS)*random.random())
		s.color = HTML_COLORS[i]
		s.save()
def setSpeakerColorsFromType(e):
	for s in e.speaker_set.all():
		s.color = SPK_COLORS[s.ddi_type]
		s.save()	
###########################################################################
# return color dict for a text or for whole enquete
def getSpeakersColorsDict(e,texte):
	colors={}
	try:
		for s in texte.speaker_set.all():
			colors[int(s.id)]=str(s.color)
	except:
		for s in e.speaker_set.all():
			colors[int(s.id)]=str(s.color)
	return colors
###########################################################################






###########################################################################
# involved viz
def getRelatedViz(textes=[],speakers=[],user=None):
	or_query = None
	
	#### query for speakers
	for s in speakers:
		if or_query is None:
			or_query = Q(speakers=s)
		else:
			or_query = or_query | Q(speakers=s)
	
	#### query for textes
	for t in textes:
		for s in t.speaker_set.exclude(ddi_type='INV'):
			if or_query is None:
				or_query = Q(speakers=s)
			else:
				or_query = or_query | Q(speakers=s)			
		if or_query is None:
			or_query = Q(textes=t)
		else:
			or_query = or_query | Q(textes=t)
	
	if or_query==None:
		return []
	else:
		qset = Visualization.objects.filter(or_query).distinct().order_by('viztype','id')
		### if texte is given, then we have to only keep one TexteStreamTimeline
		if len(textes)==1:
			qset = qset.filter(~Q(viztype='TexteStreamTimeline') | Q(viztype='TexteStreamTimeline',textes__id=textes[0].id))
		if not user.is_staff:
			qset = qset.filter(Q(public=True))
		return qset
###########################################################################






###########################################################################
def removeQuotesStartEnd(instr):
	return re.sub('(^")|("$)','',instr)
###########################################################################
def removeSpacesReturns(instr):
	return re.sub('(\t+)|(\n+)|( +)',' ',instr)
###########################################################################
def removeAllSpacesReturns(instr):
	return re.sub('(\t+)|(\n+)|( +)','',instr)
###########################################################################
def removeSpacesBeforePunctuation(instr):
	return re.sub('( ,)',',',instr)
###########################################################################
def makeHtmlFromText(instr):
	instr = re.sub('\n+','\n',instr)
	instr = '<p>'+instr+'</p>'
	return re.sub('\n','</p><p>',instr)
def makeReturnsToHtml(instr):
	return re.sub('\n','</br>',instr)
###########################################################################
def correctTeiPunctuation(instr):
	instr = re.sub('</w><incident type="repair" /><w>','/',instr)
	return re.sub('</w><c>-</c><w>','-',instr)
###########################################################################






###########################################################################
# to be abnle to sort 123 & 98, with put all with 8 digits
def intToSortableStr(number):
	s = str(number)
	return "".join(['0' for i in range(8-len(s))])+s
###########################################################################





###########################################################################
def guess_encoding(text):
	guess_list=['utf-8','us-ascii','iso-8859-1','iso-8859-2','windows-1250','windows-1252','?']
	for best_enc in guess_list:
		try:
			unicode(text,best_enc,"strict")
		except:
			pass
		else:
			break
	if best_enc=='?':
		return 'utf-8'
	return best_enc
###########################################################################	
	



###########################################################################
def getTailOfFile(filepath,count):
	try:
		logFile = open(filepath,'r')
		res = logFile.readlines()[-count:]
		logFile.close()
	except:
		res = ['no log file found']
	res.reverse()
	return res
###########################################################################










	
		


###########################################################################
def list2dict(data):
	stop=len(data)
	keys=[data[i] for i in range(stop) if i%2==0] 
	values=[data[i] for i in range(stop) if i%2==1]
	return dict(zip(keys,values))
###########################################################################




































###########################################################################
def removeBadChars(inStr):
	inStr = re.sub(re.compile('[^\w^\.]*'),'',inStr)
	return inStr
####################################################################
def convertUnrtfHtmlToTxt(inStr):
	inStr = re.sub('&nbsp;',' ',inStr)
	inStr = re.sub('\n','',inStr)
	inStr = re.sub('<head>.*</head>','',inStr)
	sp = 'font|span|div'
	inStr = re.sub('<('+sp+')[^>]*>|</('+sp+')>','',inStr)
	sp = 'body|html|center|small|sup|b|i|u'
	inStr = re.sub('<('+sp+')>|</('+sp+')>','',inStr)
	inStr = re.sub('<br>','\n',inStr)
	return inStr
####################################################################








###########################################################################
def getIntroHtmlAsArray(templateName):
	f=open( settings.REANALYSEPROJECTPATH + "templates/"+templateName+".html",'r')
	alltxt=''.join(f.readlines())
	f.close()
	
	out=[]
	# get titles based on <h1> tags
	pat = re.compile('(<h1>([^<]*)</h1>)')
	for u in pat.finditer(alltxt):
		out.append({'content':'notyet!','title':u.group(1)})
	logger.info("LENGTH"+str(len(out)))
	
	parts = re.split(pat,alltxt)
	c=0
	for t in parts:
		out[c]['content']=t
		c+=1
	return out
	#return simplejson.dumps(out,indent=4,ensure_ascii=False)
###########################################################################





####################################################################
def getContentOfFile(filePath):
	outStr=""
	#try:
	f=open(filePath,'r')
	outStr="".join(f.readlines())
	f.close()
	#except:
		#outStr="Problem loading File"
		#logger.info(outStr)
	return outStr	
####################################################################







###########################################################################
def addFileToEnquete(f,enquete):
	filePath = settings.REANALYSEUPLOADPATH + f.name
	logger.info( "HANDLE UPLOADING FILE to",filePath)
	destination = open(filePath, 'wb+')
	for chunk in f.chunks():
		destination.write(chunk)
	destination.close()
	
	buildObjectsFromXML(filePath)
	
	# Deprecated
#	
#	# get id of Text
#	tree = ElementTree()
#	tree.parse(filePath)
#	root = tree.getroot()
#	t = root.findall('text')
#	theid = t[0].attrib['id']
#	
#	# if id already exists, replace the Document
#	try:
#		ob = Texte.objects.get(texteid=theid)
#		ob.delete()
#	except:
#		pass
#		
#	newTexte = Texte(enquete=enquete)
#	newTexte.parseXmlFile(filePath)
#	newTexte.save()
###########################################################################
def exportEnquetesAsXML():
	filePath = settings.REANALYSEUPLOADPATH+"export_enquetes.xml"
	XMLSerializer = serializers.get_serializer("xml")
	xml_serializer = XMLSerializer()
	fileOut = open(filePath, "w")
	xml_serializer.serialize(Enquete.objects.all(), stream=fileOut)
	fileOut.close()
	logger.info("Exporting all Enquetes to XML :"+filePath)
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
def giveAllContent(enquete,query):
	# simple css highlighting for text results
	outContent=enquete.content
	for w in normalize_query(query):
		outContent = highlightText(outContent,w)
	d=dict()
	d['name']=enquete.name
	d['content']=outContent
	#d['total']= ...
	return [d]
###########################################################################
def giveExcerpts(enquete,query):
	resArr=[]
	for w in normalize_query(query):
		wpat=re.compile('(( [^ ]*){,6})'+w+'(( [^ ]*){,6})')
		for u in wpat.finditer(enquete.content):
			beg = u.group(1)
			end = u.group(3)
			# add excerpt to result
			d=dict()
			d['name']=enquete.name
			d['before']=".."+highlightText(beg,w)
			d['after']=highlightText(end,w)+".."
			d['excerpt']='<span class="searchResultHighlight_excerpt">'+w+'</span>'
			resArr.append(d)
	return resArr
###########################################################################








################################################################################
class unzip:
	"""
	By Doug Tolton
	cf http://code.activestate.com/recipes/252508-file-unzip/
	"""
	def __init__(self, verbose = False, percent = 10):
		self.verbose = verbose
		self.percent = percent
	def extract(self, file, dir):
		if not dir.endswith(':') and not os.path.exists(dir):
			os.mkdir(dir)
		zf = zipfile.ZipFile(file)
		# create directory structure to house files
		self._createstructure(file, dir)

		num_files = len(zf.namelist())
		percent = self.percent
		divisions = 100 / percent
		perc = int(num_files / divisions)

		# extract files to directory structure
		for i, name in enumerate(zf.namelist()):
			if not name.endswith('/'):
				outfile = open(os.path.join(dir, name), 'wb')
				outfile.write(zf.read(name))
				outfile.flush()
				outfile.close()

	def _createstructure(self, file, dir):
		self._makedirs(self._listdirs(file), dir)

	def _makedirs(self, directories, basedir):
		""" Create any directories that don't currently exist """
		for dir in directories:
			curdir = os.path.join(basedir, dir)
			if not os.path.exists(curdir):
				os.mkdir(curdir)

	def _listdirs(self, file):
		""" Grabs all the directories in the zip structure
		This is necessary to create the structure before trying
		to extract the file to it. """
		zf = zipfile.ZipFile(file)

		dirs = []

		for name in zf.namelist():
			if name.endswith('/'):
				dirs.append(name)

		dirs.sort()
		return dirs
################################################################################







###########################################################################
# Deprecated, since we can use csv.DictReader instead...
def parseCsvFile(inPath):
	header=[]
	content=[]
	inFile = open(inPath,'r')
	nm=0
	for l in inFile.readlines():
		arr=l.split('\t')
		if nm==0:
			nm+=1
			for v in arr:
				header.append(removeQuotesStartEnd(v))
		else:
			valtab=arr
			values=dict()
			for k in range(len(header)):
				values[header[k]] = removeQuotesStartEnd(valtab[k])
			if values[header[k]]=="":
				values[header[k]]="[NC]"
			content.append(values)
	inFile.close()
	return {'header':header,'content':content}
###########################################################################
# GET HTML around intervention
MAX_EXTRACT_WORDS=200
def getHtmlAroundIntervention(intervention):
	intervention.contenthtml = stylizeTeiInterventionToHtml(intervention)
	intervention.save()
	return intervention.contenthtml
###########################################################################








####################################################################
# NB:
#
#tf			nocc of a word / nb of words for a speaker
#			Speaker s
#			WordEntity we
#			TF = we.word_set.count() / s.word.count()
#
#df			number of speaker having a word / total number of speakers
#			WordEntity we
#			DF = we.wordentityspeaker_set.count() / Speaker.objects.count()
#			
#idf		log(1/df)
#tf-idf		tf * idf
####################################################################
# DEPRECATED handmade TFIDF
####################################################################
# def calculateTfidf(enquete):
# 	# Update DF/ TF-IDF
# 	# todo: https://docs.djangoproject.com/en/dev/topics/db/queries/
# 	# more efficient using Queries with F()
# 	# to calculate directly in SQL queries
# 	# ex: Entry.objects.all().update(n_pingbacks=F('n_pingbacks') + 1)
# 	enquete.status=1
# 	enquete.save()
# 	
# 	############## DF
# 	a=True
# 	#nSpeakers = Speaker.objects.count()
# 	#for the moment, testing with 3 texts and 3 speakers
# 	nSpeakers = 10
# 	for we in WordEntity.objects.all():
# 		we.df = we.wordentityspeaker_set.count() / float(nSpeakers)
# 		if a:
# 			logger.info("Sample DF:" + str(we.df))
# 		a=False
# 		we.save()
# 	############## TF-IDF
# 	a=True
# 	for wes in WordEntitySpeaker.objects.all():
# 		# TF
# 		s = wes.speaker
# 		we = wes.wordentity
# 		wes.tf = wes.word_set.count() / float(s.word_set.count())
# 		if a:
# 			logger.info("Sample TF:" + str(wes.tf))
# 		wes.tfidf = wes.tf * math.log( 1 / float(we.df) )
# 		if a:
# 			logger.info("Sample TF-IDF:" + str(wes.tfidf))
# 		a=False
# 		wes.save()
# 	############## Storing max(TF-IDF,for each WordEntitySpeaker) in each WordEntity
# 	for we in WordEntity.objects.all():
# 		maxtfidf=0
# 		maxspeakerid=0
# 		for wes in we.wordentityspeaker_set.all():
# 			if wes.tfidf > maxtfidf:
# 				maxtfidf = wes.tfidf
# 				maxspeakerid = wes.speaker.id
# 		we.maxtfidf = maxtfidf
# 		we.maxspeakerid = maxspeakerid
# 		we.save()
# 	
# 	enquete.status=0
# 	enquete.save()
####################################################################

