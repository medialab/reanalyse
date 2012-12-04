
# -*- coding: utf-8 -*-
################################################
from reanalyse.reanalyseapp.globalvars import *

# for removeSpacesBeforePunctuation()
from reanalyse.reanalyseapp.utils import *

from django.db import models

# For math manipulations in TF,DF,TFIDF
from django.db.models import Avg, Max, Min, Count

from xml.etree.ElementTree import ElementTree
from lxml import etree

from django.conf import settings

# for date manip on parsing
import datetime

import simplejson

from itertools import chain

from string import maketrans
import re, os

# Python memory lookup
#import psutil

####################
import django_tables2 as tables
from django.utils.safestring import mark_safe

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


####################################################################
# SITECONTENT for static html pages, allowing edit in admin pages
class SiteContent(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=400)
	lang = models.CharField(max_length=2,choices=LANG_CHOICES)
	contenthtml = models.TextField()
	def __unicode__(self):
		return self.name
####################################################################



##############################################################################		
# SOLR INSTANCE
##############################################################################
#
# we could store the pid in the db
# rather search for process using (unique) defined SOLR_PORT
#
# class SolrProcess(models.Model):
# 	# used to keep track of solr process pid
# 	# (there will only be one object of this type)
# 	pid = models.CharField(max_length=20)



##############################################################################		
# ENQUETE
##############################################################################
class Enquete(models.Model):
	#connection_name="enquetes"				# todo: one db for each enquete ?
	name = models.CharField(max_length=250)
	uploadpath	 = models.CharField(max_length=250)	# root path of uploaded folder (if we want to remove everything)
	locationpath = models.CharField(max_length=250)	# root path of the extracted folder (used as base during import)
	metadata = models.TextField(default='{}') 		# store all metadata as json dict
	ese = models.TextField()						# ese is not yet included/structured in enquete, let's put all infos from ese.xml into a json dict
	status = models.CharField(max_length=2, choices=STATUS_CHOICES)		# see globalvars
	statuscomplete = models.BigIntegerField(default=0) 					# loading 0-100%
	date = models.DateTimeField(auto_now_add=True)							# date uploaded
	ddi_id = models.CharField(max_length=170)
	#permission = models.ForeignKey(Permission)
	class Meta: # Users & Groups are initialized in views
		permissions = (
			("can_browse", "BROWSE Can see enquete overview"),
			("can_explore", "EXPLORE Can see whole enquete"),
			("can_make", "MAKE Can upload enquetes and make viz"),
		)
	def __unicode__(self):
		return str(self.id)+":"+self.name
	def meta(self):
		if self.metadata:
			return simplejson.loads(self.metadata)
		else:
			return {'metainfo':'no meta was parsed'}
####################################################################





##############################################################################
class Visualization(models.Model):
	enquete = models.ForeignKey(Enquete)
	name = models.CharField(max_length=200)
	locationpath = models.CharField(max_length=250) # mainly for gexf graphs
	description = models.TextField()
	viztype = models.CharField(max_length=50)
	status = models.CharField(max_length=2, choices=STATUS_CHOICES)
	public = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add=True)
	contenthtml = models.TextField()		# unused yet, could be useful if you want to store rendered html
	json = models.TextField()
	# keeping link with texts/speakers involved
	textes = models.ManyToManyField('Texte')
	speakers = models.ManyToManyField('Speaker')
	def __unicode__(self):
		return self.name
##############################################################################
# 'Texte' model .... ( to rename to 'Document'? )
class Texte(models.Model):
	enquete = models.ForeignKey(Enquete)
	# file
	locationpath = models.CharField(max_length=500)
	filesize = models.BigIntegerField(default=0)
	# meta
	doctype = models.CharField(max_length=4, choices=DOCUMENT_TYPE_CHOICES)
	doccat1 = models.CharField(max_length=25)	# see globalvars.py
	doccat2 = models.CharField(max_length=25)	# see globalvars.py
	name = models.CharField(max_length=100)
	description = models.TextField()
	# todo
	date = models.DateField(default=datetime.datetime.today())	# "2011-01-02"
	location = models.CharField(max_length=30) 					# "Paris" todo: change to gps specific field ?
	#
	public = models.BooleanField(default=False)					# visible in edbrowse or not
	status = models.CharField(max_length=2, choices=STATUS_CHOICES)
	statuscomplete = models.BigIntegerField(default=0) 			# 0-100%
	# for verbatims, we store content in DB
	contenttxt = models.TextField()		# unused ? (full text for indexation)
	contenthtml = models.TextField()	# styled html for display
	contentxml = models.TextField()		# original xml TEI
	def __unicode__(self):
		return str(self.id)+":"+self.name
	def parseXml(self):
		self.status='2'
		self.save()
		if self.doctype=='TEI':
			#try:
			# building Structure found in the tei xml
			parseXmlDocument(self)
			self.status='0'
			#except:
				#self.status='-1'
		self.save()
##############################################################################


		





##############################################################################	
# age,sex,profession,...
class AttributeType(models.Model):
	enquete = models.ForeignKey(Enquete)
	name = models.CharField(max_length=200)
	publicy = models.CharField(max_length=1, choices=ATTRIBUTE_PUBLICY_CHOICES)
	def __unicode__(self):
		return self.name
##############################################################################	
# 45,33,12,H,F,pêcheur diplomé & groupeType2,groupeType3
class Attribute(models.Model):
	enquete = models.ForeignKey(Enquete)
	attributetype = models.ForeignKey(AttributeType)
	name = models.TextField()	# was/should be .CharField(max_length=300) - but avoid problem of VERY long cells in studies
	#description = models.TextField() # deprecatedcould be long text to describe a group
	def __unicode__(self):
		return self.name
##############################################################################
class Speaker(models.Model):
	enquete = models.ForeignKey(Enquete)
	name = models.CharField(max_length=70)
	textes = models.ManyToManyField(Texte)
	#################
	## USED IN TEI XML and CSV list of spk
	ddi_id = models.CharField(max_length=170)
	## USED TO KNOW (investigator/speaker/protagonist)
	ddi_type = models.CharField(max_length=3, choices=SPEAKER_TYPE_CHOICES)
	#################
	public = models.BooleanField(default=False)					# visible in esbrowse or not
	attributes = models.ManyToManyField(Attribute)
	color = models.CharField(max_length=7,default=HTML_COLORS[0])
	# we may have to put all his text content in a TextField, to index with solr...
	# made in the parsing
	contenttxt = models.TextField()
	def __unicode__(self):
		return str(self.id)+":"+self.name
##############################################################################
# to store sets of speakers
class SpeakerSet(models.Model):
	enquete = models.ForeignKey(Enquete)
	speakers = models.ManyToManyField(Speaker)
	name = models.CharField(max_length=50)
	description = models.TextField()
	def __unicode__(self):
		return "SpeakerSet:"+str(self.id)+":"+self.name
##############################################################################







##############################################################################
# for sentences[exclamative,interrogative,...] and for paraverbal[silence,break,comment]
class Code(models.Model):
	enquete = models.ForeignKey(Enquete)
	name = models.CharField(max_length=50)
	textes = models.ManyToManyField(Texte)
 	def __unicode__(self):
 		return self.name
#################################################
class Sentence(models.Model):
	# Enfin •• je crois ((rire)).
	enquete = models.ForeignKey(Enquete)
	texte = models.ForeignKey(Texte)
	speaker = models.ForeignKey(Speaker)
	# DEPRECATED: intervention = models.ForeignKey(Intervention)
	code = models.ForeignKey(Code)
	#####
	contenttxt = models.TextField()
	contenthtml = models.TextField() 
	##### time location
	i = models.BigIntegerField(default=0)
	o = models.BigIntegerField(default=0)
	##### order if same time location
	n = models.BigIntegerField(default=0)
	######
	def __unicode__(self):
		return "part"+str(self.n)+"["+str(self.i)+","+str(self.o)+"]from"+str(self.speaker.id)+":"+self.contenttxt[:7]
####################################################################################
class WordEntity(models.Model):
	# Word used by all Speakers
	enquete = models.ForeignKey(Enquete)
	code = models.ForeignKey(Code)
	######
	textes = models.ManyToManyField(Texte)
	######
	content = models.CharField(max_length=50) 			# word content
	description = models.TextField(max_length=400) 		# quite big 'cause can be the content of a paraverbal comment for ex.
	df = models.FloatField(default=0)
	maxtfidf = models.FloatField(default=0)
	maxspeakerid = models.BigIntegerField(default=0)
	######
	def __unicode__(self):
		return "WordEntity:"+self.content
####################################################################################
class WordEntitySpeaker(models.Model):
	# Word used by a Speaker
	speaker = models.ForeignKey(Speaker)
	wordentity = models.ForeignKey(WordEntity)
	######
	textes = models.ManyToManyField(Texte)
	######
	tf = models.FloatField(default=0)
	tfidf = models.FloatField(default=0)
	######
	def __unicode__(self):
		return "WordEntitySpeaker:"+self.speaker.name
####################################################################################
class Word(models.Model):
	# Unique instance of WordEntitySpeaker in a Text
	enquete = models.ForeignKey(Enquete)
	wordentityspeaker = models.ForeignKey(WordEntitySpeaker)
	sentence = models.ForeignKey(Sentence)
	speaker = models.ForeignKey(Speaker)
	##### increment, just to keep words order
	n = models.BigIntegerField(default=0)
	def __unicode__(self):
		return "Word:"+str(self.n)+":"+self.wordentity.content	
####################################################################





####################################################################
# Storing solr ngrams & tfidf results !
# it looks like deprecated WordEntity & WordEntitySpeaker models at the beginning of the project
# ... but here it's lighter because we only keep high tfidf words.. (see viz.py - makeAllTfidf())
####################################################################
class Ngram(models.Model):
	enquete = models.ForeignKey(Enquete)
	content = models.CharField(max_length=100)
	######
	df = models.FloatField(default=0)			# % of speakers using this word
	#dn = ngramspeaker_set.count()				# n of speakers using this word (easy using django queries)
	# NB: no need to store max values here ! do it using django queries !
	# maxtfidf = models.FloatField(default=0)
	# maxspeakerid = models.BigIntegerField(default=0)
	def __unicode__(self):
		return "Ngram:"+str(self.n)+":"+self.content
####################################################################
class NgramSpeaker(models.Model):
	enquete = models.ForeignKey(Enquete)
	ngram = models.ForeignKey(Ngram)
	speaker = models.ForeignKey(Speaker)
	######
	tf = models.FloatField(default=0)			# term frequency 	for that speaker
	tn = models.BigIntegerField(default=0)		# term count		for that speaker
	tfidf = models.FloatField(default=0)
	def __unicode__(self):
		return "NgramSpeaker:"+str(self.n)+":"+self.ngram
####################################################################







############################################################################################
# TEI XML PARSER
############################################################################################
def parseXmlDocument(texte):
	e = texte.enquete
	
	# WE ERASE ALL OBJECTS if there is (will erase Sentences & Words too)
	texte.sentence_set.all().delete()
	
	tree = etree.parse(texte.locationpath)
	root = tree.getroot()
	roottag = root.tag
	
	######################### NB + todo
	# the current parsing loops are expensive !
	# it may be better to use xslt to "parse" xml
	# xslt could also fetch subparts of the original xml file !
	#
	# ...to do:
	#
	# 1) using xslt, extract:
	# 	- txtcontent of each speaker , to populate each speaker.contenttxt
	# 	- txtcontent of whole document, to populate texte.contenttxt
	# both are used for indexation
	#
	# 2) using xslt, style wanted part of original TEI xml, to populate html template
	#
	
	
	######################### NB
	# we don't care about speakers !
	# we just get_or_create(ddi_id=theidfoundinTEI)
	# supposing all speaker infos/attributes were or will be updated using .csv file
	# however, we keep a speaker array to store/update total txt content of each spk (see bellow)
	
	speakersArray=[]
	
	######################### NB
	# only 2 DTD are supported :
	#	- XML-TEI file made by Exmaralda > TEI Drop 	tag <Trans>
	#	- XML-TXM file made by Transcriber > TXM		tag <TEI>
	# todo: use DTD to parse any schema..
	
	######################### XML TXM		## Built using Formatted .txt > TXM
	if roottag=='Trans':
		logger.info("["+str(e.id)+"] parsing type: TXM")
		persons = root.findall('Speakers/Speaker')
		for n,p in enumerate(persons):
			speakersArray.append( p.attrib['id'] )
		# every speaker turn
		childs = root.findall('Episode/Section/Turn')
		parseTXMDivs(texte,childs,speakersArray)
	
	######################### XML TEI		## Built using: Formatted .txt > Exmaralda .exb > TEI Drop
	elif roottag==XMLTEINMS+'TEI':
		logger.info("["+str(e.id)+"] parsing type: Exmaralda TEI")
		persons = root.findall(XMLTEINMS+'teiHeader/'+XMLTEINMS+'profileDesc/'+XMLTEINMS+'particDesc/'+XMLTEINMS+'person')
		# putting speakers ddi_id from TEI header in a dict to access them (if the <who> tags contains #references to that header)
		speakersDDIDict={}
		if persons[0].attrib[XMLNMS+'id']=='SPK0': # means that ddi ids are defined in header
			for n,p in enumerate(persons):
				pid=p.attrib[XMLNMS+'id']
				name=p.findall(XMLTEINMS+'persName/'+XMLTEINMS+'abbr')[0].text
				speakersDDIDict['#'+pid]=name
				speakersArray.append( name )
		else:
			for n,p in enumerate(persons):
				speakersArray.append( p.attrib[XMLNMS+'id'] )
		# every speaker turn
		tnode = root.findall(XMLTEINMS+'text/'+XMLTEINMS+'body')[0]
		childs = tnode.getchildren()
		parseTEIDivs(texte,childs,speakersArray,speakersDDIDict)
	
	#########################
	else:
		logger.info("PB:XML file not parsed cause neither <Trans> or <TEI> tag was found")
####################################################################






############################################################################################################### PARSE TXM
# NB: we build long sentences without looking at punctuation
def parseTXMDivs(texte,nodes,speakersArray):
	e=texte.enquete
	speakerContentDict = dict((theid,'') for theid in speakersArray)
	
	# loop over each speaker turn, make ONE sentence for each
	allTextContentTxt = ""
	curTime = 0
	for node in nodes:
		spk_ddiid = node.attrib['speaker']
		
		# new Speaker
		theSpeaker,isnew = Speaker.objects.get_or_create(enquete=texte.enquete,ddi_id=spk_ddiid)
		theSpeaker.textes.add(texte)
		theSpeaker.save()
		
		# new Sentence
		theCode,isnew = Code.objects.get_or_create(enquete=e,name="txm_normal_sentence")
		theCode.textes.add(texte)
		theCode.save()
		theSentence,isnew = Sentence.objects.get_or_create(enquete=e,texte=texte,speaker=theSpeaker,code=theCode,i=curTime,o=curTime+1,n=0,contenttxt='emptyforthemoment')
		
		# fill sentence with words
		words = node.findall('w')
		allSentencesContentTxt = parseTXMWords(theSentence,words,0)
		theSentence.contenttxt = allSentencesContentTxt
		theSentence.save()
		speakerContentDict[spk_ddiid] += allSentencesContentTxt + '\n\n'
		allTextContentTxt += allSentencesContentTxt + '\n\n'
		
		curTime += 1
	
		# gets % of "loading completeness"
		compl = int(curTime*100/len(nodes))
	 	# texte.save() is taking a lot of memory !!
		# MONITORING : print("MEMORY:"+str(psutil.phymem_usage()[3]))
		if compl!=texte.statuscomplete and compl%5==0:
			texte.statuscomplete = compl
			texte.save()
	
	texte.contenttxt = allTextContentTxt
	texte.save()
	
	# store/add all contenttxt for each spk
	for s in texte.speaker_set.all():
		s.contenttxt += speakerContentDict[s.ddi_id] + '\n'
		s.save()
################################################
def parseTXMWords(sentence,words,N):
	# for the moment only looking at normal words+punctuation
	allSentenceTxt=""
	allSentenceHtml=""
	
	for wnode in words:
		w_content = wnode.find(XMLTXM+'form').text
		w_lem = wnode.find('interp[@type="#ttlemma"]').text
		w_pos = wnode.find('interp[@type="#ttpos"]').text
		w_pos = w_pos.replace(":","_") # because we will use CSS
		
		allSentenceTxt += w_content+' '
		# nb: we put content in css class to allow some display
		wclasses = 'w_'+w_content.lower()+' lem_'+w_lem+' pos_'+w_pos
		allSentenceHtml += '<span class="'+wclasses+'">' + w_content + '</span> '
	
	#### save all content of that sentence
	endS = ' | '
	sentence.contenttxt = allSentenceTxt + endS
	sentence.contenthtml = allSentenceHtml + endS
	sentence.save()
	
	return allSentenceTxt
########################################################################









############################################################################################################### PARSE TEI
####################################################################
def getTeiAnchorTime(elem):
	# because of weird TEI use of "#T453" or "T453" for time anchors
	att=elem.attrib['synch']
	if att[0]==("T"):
		return int(att[1:])
	else:
		return int(att[2:])
################################################
def splitElemListByTimeAnchor(elemList,initTime):
	# the yield returns [ time, list of words ]
	j=0
	anchorTime = initTime
	for k,el in enumerate(elemList):
		if el.tag==XMLTEINMS+'anchor':
			yield [anchorTime, elemList[j:k]]
			#
			anchorTime = getTeiAnchorTime(el)
			j=k+1
	# last part
	yield [anchorTime, elemList[j:k+1]]
######################################################################## manage list of all <div>
def parseTEIDivs(texte,nodes,speakersArray,speakersDDIDict):
	# init speakerContentDict which will store all text for one speaker
	speakerContentDict = dict((theid,'') for theid in speakersArray)
		
	allTextContent=""
	texte.statuscomplete=0
	texte.save()
	divNodesTotal=len(nodes)
	divNodesCur=0
	# here we note the complete %, based on the total number of interventions
	for node in nodes:
		if node.tag==XMLTEINMS+'div':
			unode = node.findall(XMLTEINMS+'u')[0]
			ddiid = unode.attrib['who']
			if ddiid.startswith('#'): # means that the real ddi_id is in the header
				try:
					ddiid = speakersDDIDict[ddiid]
				except:
					logger.info("["+str(texte.enquete.id)+"] EXCEPT pb parsing TEI xml ids: texteid="+str(texte.id))
			# DEPRECATED: theCodeType,isnew = CodeType.objects.get_or_create(enquete=texte.enquete,name='speaker')
			theSpeaker,isnew = Speaker.objects.get_or_create(enquete=texte.enquete,ddi_id=ddiid)
			theSpeaker.textes.add(texte)
			theSpeaker.save()
			# get sub-elements (and get time <anchor synch="#T16" /> information !)
			childs = unode.getchildren()
			# DEPRECATED: i = getTeiAnchorTime(childs[0])
			# DEPRECATED: o = getTeiAnchorTime(childs[-1])
			# DEPRECATED: theIntervention,isnew = Intervention.objects.get_or_create(enquete=texte.enquete,texte=texte,speaker=theSpeaker,i=i,o=o)
			curtxt = parseTEISentences(texte,childs,theSpeaker)
			allTextContent += curtxt + '\n\n'
			#speakerContentDict[speaker] = speakerContentDict[speaker] + curtxt + '\n\nt='+str(texte.id)+':i='+str(curIntervention)+'\n\n'
			speakerContentDict[ddiid] = speakerContentDict[ddiid] + curtxt + '\n'
			divNodesCur+=1
		# gets % of "loading completeness"
		compl=int(divNodesCur*100/divNodesTotal)
	 	# texte.save() is taking a lot of memory !!
		# MONITORING : print("MEMORY:"+str(psutil.phymem_usage()[3]))
		if compl!=texte.statuscomplete and compl%5==0:
			texte.statuscomplete = compl
			texte.save()
	# save all content of that text (used by solr indexing)
	texte.contenttxt = allTextContent
	texte.save()
	# save all contents of speakers (nb: already saved as text.speaker_set)
	for s in texte.speaker_set.all():
		#s.content = s.content + '\n\nSTART_TEXT t='+str(texte.id)+'\n\n'+ speakerContentDict[s.name] + '\n\nEND_TEXT t='+str(texte.id)+'\n\n'
		allt = s.contenttxt + speakerContentDict[s.ddi_id] + '\n'
		s.contenttxt = re.sub('( ,)',',',allt)
		s.save()
########################
def parseTEISentences(texte,nodes,speaker):
	e=texte.enquete
	allSentencesContent=""
	n=0 # index of sentences if many in same intervention
	for node in nodes:
		if node.tag==XMLTEINMS+'anchor':
			# note that "global" i/o is already stored for the current intervention (see above)
			# nodes[0] = <anchor> start time of sentences
			startTime = getTeiAnchorTime(node)
		if node.tag==XMLTEINMS+'seg':	
			# nodes[1] = <seg> the sentence(s)
			typ=node.attrib['type']
			# todo: type of sentence should only apply to last part of <seg> element, previous ones should have 'not_classified'
			# get all children and split by (time) <anchor>
			childsElem = node.getchildren()
			if len(childsElem)>0:
				sentsSplitted = list(splitElemListByTimeAnchor(childsElem,startTime))
				# then create sentence for each part
				for part in sentsSplitted:
					curTime = part[0]
					childList = part[1]
					#theCodeType,isnew = CodeType.objects.get_or_create(enquete=e,name='sentence')
					theCode,isnew = Code.objects.get_or_create(enquete=e,name=typ)
					theCode.textes.add(texte)
					theCode.save()
					theSentence,isnew = Sentence.objects.get_or_create(enquete=e,texte=texte,speaker=speaker,code=theCode,i=curTime,o=curTime+1,n=n,contenttxt='emptyforthemoment')
					allSentencesContent += parseTEIWords(theSentence,childList,0)
					n+=1
		# note that 'out' time is always 'in'+1 (we suppose every sentence is surrounded by consecutive time <anchors>)
	# DEPRECATED: save all content of that intervention
	# DEPRECATED: intervention.contenttxt = allSentencesContent
	# DEPRECATED: intervention.save()
	return allSentencesContent
########################
def parseTEIWords(sentence,nodes,N):
	e=sentence.texte.enquete
	t=sentence.texte
	s=sentence.speaker
	allSentenceTxt=""
	allSentenceHtml=""
	onlyMarginParaverbal=True	
	for node in nodes:
		incidDesc=''
		createWord = True
		isParaverbal=False
		###################################################################### WORDS & PUNCTUATION
		if node.tag==XMLTEINMS+'w':
			# TRASH: codeTypeName = 'word'
			wordContent = node.text
			allSentenceTxt += wordContent+" "
			# nb: if we want to, we can put content in css class to allow some display
			#allSentenceHtml += '<span class="w_'+wordContent+'">' + wordContent + "</span> "
			allSentenceHtml += wordContent + " "
		elif node.tag==XMLTEINMS+'c':
			# TRASH: codeTypeName = 'ponctuation'
			wordContent = node.text
			allSentenceTxt += wordContent+" "
			allSentenceHtml += wordContent+" "
		###################################################################### PARAVERBAL PARSING, see globalvars.py for codes
		elif node.tag==XMLTEINMS+'pause':
			# TRASH: codeTypeName = 'paraverbal'
			isParaverbal = True
			codeName = 'silence'
			try:
				wordContent = node.attrib['type'] # short/long
			except:
				wordContent = 'silence'
		elif node.tag==XMLTEINMS+'incident':
			# TRASH: codeTypeName = 'paraverbal'
			isParaverbal = True
			codeName = 'incident'
			wordContent = 'incident'
			try:
				incidDesc = node.findall(XMLTEINMS+'desc')[0].text
			except:
				incidDesc = 'nodescr.orpbparsing.forthisincident'
			################################ look into description to manage know incidents
			if incidDesc in CODES_IMAGE.keys():
				codeName = CODES_IMAGE[incidDesc]
			else:
				for nms in CODES_IMAGE_TOOLTIP.keys():
					if incidDesc.startswith(nms):
						codeName = CODES_IMAGE_TOOLTIP[nms]
						incidDesc = incidDesc[len(nms):]
				for nms in CODES_TEXT_TOOLTIP.keys():
					if incidDesc.startswith(nms):
						codeName = CODES_TEXT_TOOLTIP[nms]
						incidDesc = incidDesc[len(nms):]
				for nms in CODES_TEXT.keys():
					if incidDesc.startswith(nms):
						codeName = CODES_TEXT[nms]
						incidDesc = incidDesc[len(nms):]
			################################
		else:
			# TRASH: codeTypeName = 'unknown'
			createWord = False
		
		###################################################################### PARAVERBAL HTML
		if isParaverbal:
			try:
				cssClass='text_anyparvb ' + CODE_TO_CSS[codeName]
				# add classes if you want certain types to be located on the margin
				if codeName in PARVBMARGL:
					cssClass+= ' text_margL'
				if codeName in PARVBMARGR:
					cssClass+= ' text_margR'
			except:
				cssClass='text_anyparvb text_incident'
			
			# NB: for tooltips, location of bubble depends on 'onlyMarginParaverbal'... see javascript for the location
			
			if codeName in CODES_IMAGE.values(): 				# dont keep content, only image
				#allSentenceHtml += '<div class="'+cssClass+'">&nbsp;</div>'
				# todo: content even if no descr (rappel)
				allSentenceHtml += '<a rel="text_tooltip" title="'+codeName+'" class="'+cssClass+'"><div>&nbsp;</div></a> '
			elif codeName in CODES_IMAGE_TOOLTIP.values(): 		# keep content as popup on image (tooltip made with js)
				allSentenceHtml += '<a rel="text_tooltip" title="'+incidDesc+'" class="'+cssClass+'"><div>&nbsp;</div></a> '
			elif codeName in CODES_TEXT.values(): 				# text styling
				allSentenceTxt += incidDesc+" "
				allSentenceHtml += '<div class="'+cssClass+'">'+incidDesc+'</div> '
			elif codeName in CODES_TEXT_TOOLTIP.values(): 		# text styling with tooltip
				allSentenceHtml += '<a rel="text_tooltip" title="'+codeName+'" class="'+cssClass+'"><div>'+incidDesc+'</div></a> '
			else: # unkown (ie 'incident')
				allSentenceHtml += '<a rel="text_tooltip" title="'+incidDesc+'" class="'+cssClass+'"><div>&nbsp;</div></a> '
			
			if codeName not in PARVBMARGL+PARVBMARGR:
				onlyMarginParaverbal=False
		else:
			onlyMarginParaverbal=False
		

		################################################################
		# NB:
		# BEFORECHRIST : 	we created models based on words, storing every single word in DB (easy to make stats, but heavy!)
		# AFTERCHRIST : 	then trying just to store Intervention+Sentence contents (indexing/search made by lucene/solr on Interventions)
		# AFTERBUDDHA 1 : 	saving codes+words for paraverbal content only (not yet indexed)
		# AFTERBUDDHA 2 : 	forgetting "Interventions", only keep "Sentences"(indexed) and "WordEntities"(paraverbal only)
		if createWord and isParaverbal:
			try:
				# TRASH: theCodeType,isnew = CodeType.objects.get_or_create(enquete=e,name=codeTypeName)
				theCode,isnew = Code.objects.get_or_create(enquete=e,name=codeName)
				# new unique Word or Incident description
				newWordEntity,isnew = WordEntity.objects.get_or_create(enquete=e,code=theCode,content=wordContent,description=incidDesc)
				newWordEntity.textes.add(t)
				newWordEntity.save()
				# new unique Word for that speaker
				newWordEntitySpeaker,isnew = WordEntitySpeaker.objects.get_or_create(wordentity=newWordEntity,speaker=s)
				newWordEntitySpeaker.textes.add(t)
				newWordEntitySpeaker.save()
				# new unique Word in the text
				newWord,isnew = Word.objects.get_or_create(enquete=e,sentence=sentence,wordentityspeaker=newWordEntitySpeaker,n=N,speaker=s)
				N+=1
			except:
				# todo: to solve that thread-not-safe problem with get_or_create, which can produce duplicate entries !!!!
				# update: is there really a problem here ?
				logger.info("PROBLEM: get_or_create problem :"+codeName+","+wordContent+","+str(N) )
				
	# end symbol
	
	typ = sentence.code.name
	try:
		endS = SENTENCE_UTT_SYMBOLS[typ]
	except:
		endS = SENTENCE_UTT_SYMBOLS['not_classified']
		
	#### save all TEXT content of that sentence
	sentence.contenttxt = allSentenceTxt + endS
	
	#### also save TEXT + PARAVERBAL html-styled content
	sentence.contenthtml = allSentenceHtml + endS
	
	# if only [time/comment], change code of sentence (not displayed in template!)
	if onlyMarginParaverbal:
		# TRASH: marginCodeType,isnew = CodeType.objects.get_or_create(enquete=e,name='sentence')
		marginCode,isnew = Code.objects.get_or_create(enquete=e,name='only_margin')
		# no need to add current text (we don't care about finding all textes with only_margin ...)
		#marginCode.textes.add(t)
		sentence.code = marginCode
		
	sentence.save()
	return allSentenceTxt + endS
####################################################################








########################################################################################################################################
########################################################################################################################################
########################################################################################################################################


########### NB: TEI TEXT IS STRUCTURED USING SENTENCES ONLY (no more "Interventions neither "Words):


##################################################################################
#	n		i	o	speakerid		sentence
################################################################################## TIMEPART (one timepart is said in same instant [i,o])
#	0		0	1		A		je ne crois pas.
#	1		0	1		A		enfin tu fais comme tu veux. 
################################################################################## TIMEPART 
#	0		1	2		B		non.
#	1		1	2		B		c'est faux.
#	0		1	2		C		si !
#	1		1	2		C		je te dis que si !
################################################################################## TIMEPART 
#	0		2	3		D		j'ai mangé un chien
#	0		2	3		B		impossible
################################################################################## TIMEPART (most of time, we have only one speaker per [i,o])
#	0		3	4		E		taisez-vous.
#	1		3	4		E		c'est inadmissible.
#	2		3	4		E		je continue mes phrases ?
#	3		3	4		E		je suis brun.
#	4		3	4		E		ah ah ah !
################################################################################## TIMEPART 
#	0		4	5		B
################################################################################## TIMEPART 

# to reconstruct text, we have to : order_by('i','speakerid','n')


# NEW ONE FETCHING only [i,j] timeparts (if interested, see old deprecated way below)
####################################################################
# getTextContent() returns an array of successive styled (ie, with html tags) sentences
# additionnal styling (for blocks of verbatim) is made in template render_d.html
# the array is asked at each new texte pagination in the view
#
# NB: hard styled in sentence.contenthtml, made during parsing
#	<div class="text_anyparvb">
#	<a rel="text_tooltip"
#	<span class="w_manger"> ...
#
# NB: styled in django template, see render_d.html
#	<div class="text_part speakerColor_23">
#	<div class="text_speaker"> ...
#
####################################################################
def getTextContent(texte,fromT,toT):
	RESARRAY = []
	curTimePart = []
	curSentences = []
	
	minT = max(0,fromT)
	toT = max(0,toT)
	
	sIdCur = texte.sentence_set.filter(i__range=[fromT,toT]).order_by('i','speaker','n')[0].speaker.id
	timeCur = 0
	onlyMargin = True
	
	for s in texte.sentence_set.filter(i__range=[fromT,toT]).order_by('i','speaker','n'):
		
		if s.i == timeCur: # SAME TIMEPART
			if s.speaker.id != sIdCur: # NEW SPEAKER
				curTimePart.append(curSentences)
				curSentences = []
			else: # SAME SPEAKER
				donothing=1
					
		else: # NEW TIMEPART
			curTimePart.append(curSentences)
			RESARRAY.append([onlyMargin,curTimePart])
			curTimePart = []
			curSentences = []
			onlyMargin = True
		
		timeCur = s.i 
		sIdCur = s.speaker.id
		if s.code.name != 'only_margin':
			onlyMargin = False
			
		curSentences.append(s)
	
	# flush last part
	curTimePart.append(curSentences)
	RESARRAY.append([onlyMargin,curTimePart])
	return RESARRAY
####################################################################






















# DEPRECATED way to stylize verbatims
# ####################################################################
# # returns time-grouped same-speaker-parts made of 1+ sentences
# def splitSentencesByTime(sentList):	
# 	curTime = 0
# 	curSpeakId = sentList[0].speaker.id
# 	partList=[] 	# is the list of concurrent speaks = parts
# 	sentInPart=[]	# for one speak (same speaker), there may be many sentences
# 	for sent in sentList:
# 		sId = sent.speaker.id
# 		if sent.i!=curTime: # new part because new time !			
# 			partList.append(sentInPart)		# add not-stored-last-part
# 			yield [curTime,partList] 		# returns the new part
# 			curTime=sent.i					# new time
# 			curSpeakId=sId					# new speaker
# 			partList=[]
# 			sentInPart=[]
# 			sentInPart.append(sent)			# adding curr sent to the same-speaker-part
# 		else:	# same time, ...look at the cur sent
# 			if sId!=curSpeakId:	# changing part cause new speaker
# 				partList.append(sentInPart)	# add builded-(last)-part in the parts
# 				curSpeakId=sId
# 				sentInPart=[]				# new part
# 				sentInPart.append(sent)		# put the current sent in the part
# 			else:	# same speaker, same part
# 				sentInPart.append(sent)		
# 	partList.append(sentInPart)
# 	yield [curTime,partList]
# ####################################################################
# # DEPRECATED New version, getting all sentences
# def stylizeTeiToHtml(texte):
# 	HTMLSTR=""
# 	texte.statuscomplete=0
# 	texte.save()
# 	totalSentences=texte.sentence_set.count()
# 	nDoneSents=0
# 	
# 	queueHtmlSentStr=""
# 	queueOnlyMargin=True
# 	# init lastSId to first speaker
# 	lastSId = texte.sentence_set.all().order_by('i','speaker','n')[0].speaker.id
# 	NPARTS=0
# 	# looping over array made of each time
# 	for sentParts in list( splitSentencesByTime(texte.sentence_set.all().order_by('i','speaker','n')) ):
# 		curTimeStr = str(sentParts[0])
# 		parts = sentParts[1]
# 		nConcurent = len(parts)
# 		sameTimeMultipleDiv=""
# 		sameTimeSingleDiv=""
# 		
# 		firstSent = parts[0][0]
# 		curAloneSId = firstSent.speaker.id
# 		curSpeakName = firstSent.speaker.name
# 		
# 		# todo: !!!! flush the queue for the last element !!!!! not done there
# 		
# 		################# we have to regroup time-successive-alone-speaks to the same div
# 		################# flush queued single-speaks if NEXT = new speaker OR multiple "speaks"
# 		if queueHtmlSentStr:
# 			if (nConcurent>1) or (nConcurent==1 and queuelastSId!=curAloneSId):
# 				if queueOnlyMargin: # then, put it raw (it must be a div styled to be in margin)
# 					HTMLSTR += queueHtmlSentStr
# 				else:
# 					speakNameDiv='<div class="text_speaker_name">'+queuelastSName+' <span class="text_speaker_namecount">.'+str(NPARTS)+'</span></div>'
# 					sameTimeSingleDiv += '<div class="text_speaker speakerColor_'+str(queuelastSId)+' speaker_'+str(queuelastSId)+'">'
# 					sameTimeSingleDiv += speakNameDiv + queueHtmlSentStr
# 					sameTimeSingleDiv += '</div>'
# 					HTMLSTR += '<div class="text_part part_'+str(NPARTS)+'" id="part_'+str(NPARTS)+'">' + sameTimeSingleDiv +'</div>'
# 					NPARTS+=1
# 				queueHtmlSentStr=""
# 				queuelastSId=curAloneSId
# 				queuelastSname=curSpeakName
# 				queueOnlyMargin=True
# 			
# 		################# =1 : most of time, there is only one "speak"... queue them (we'll eventually flush them on next loop)
# 		if nConcurent==1:
# 			sents = parts[0]
# 			inMargin,html = stylizeTeiSentencesToHtml(sents)
# 			nDoneSents+=len(sents)
# 			queueHtmlSentStr += html
# 			queuelastSId=curAloneSId
# 			queuelastSName=curSpeakName
# 			queueOnlyMargin=queueOnlyMargin and inMargin
# 
# 		################# >1 : but sometimes, we have many "speaks" on the same time...
# 		else:
# 			# reset queue for alone speaks of same speakers (see above)
# 			queueHtmlSentStr=""
# 			htmlSentStr=""
# 			
# 			########## Before, we were trying a table view with 2/3 columns, so we had to set the width and borders
# 			# <th> width depends on nConcurent
# 			# we will use <th> border style to set horizontal margin between concurrent "interventions"
# 			#thWidth = str(100/nConcurent)+"%"
# 			#thBorder="5px solid white"
# 			########## Now, we also use the table, but with different lines and a special-yellow border
# 			
# 			##### Looping over parts, made of same-speaker-sentences
# 			for k,sents in enumerate(parts):
# 				# get htmlStr for the 1+ sentences
# 				# IMPORTANT: 	we dont care about inMargin
# 				#				supposing (time:) & (comment:) alone are never involved in concurrent "speaks"
# 				#				so if they are, we display them anyway
# 				inMargin,htmlSentStr = stylizeTeiSentencesToHtml(sents)
# 				nDoneSents+=len(sents)
# 				speak = sents[0].speaker
# 				sId = speak.id
# 				sName = speak.name
# 				speakNameDiv='<div class="text_speaker_name">'+sName+' <span class="text_speaker_namecount">.'+str(NPARTS)+'</span></div>'
# 				# note: CLASS speakerColor_id to set bckg color		set in Template
# 				# note: ID speaker_id to show/hide					set in Javascript
# 				sameTimeMultipleDiv += '<tr><th class="speakerColor_'+str(sId)+'">'
# 				sameTimeMultipleDiv += '<div class="text_speaker speakerColor_'+str(sId)+' speaker_'+str(sId)+'">'
# 				sameTimeMultipleDiv += speakNameDiv
# 				sameTimeMultipleDiv += htmlSentStr
# 				sameTimeMultipleDiv += '</div></th></tr>'
# 			# table with only one row and as many columns as concurrent "interventions"
#  			HTMLSTR += '<div class="text_part part_'+str(NPARTS)+'" id="part_'+str(NPARTS)+'"><table>'
#  			HTMLSTR += sameTimeMultipleDiv # note that there is only one speaker name div (the first one)
#  			HTMLSTR += '</table></div>'	
#  			NPARTS+=1
#  		
#  		################ From time to time say how much loading..
#  		compl=int(nDoneSents*100/totalSentences) # not exact, because NPARTS < totalSentences, we dont care
# 		if compl!=texte.statuscomplete and compl%5==0:
# 			texte.statuscomplete = compl
# 			texte.save()
# 	return HTMLSTR
# ####################################################################







# DEPRECATED : now, styling is made directly in the parsing, storing an html version
################################################ 
# deprecated Texte Model method to build stylized version of text
# 	def stylizeContent(self):
# 		self.status='3'
# 		self.save()
# #		try:
# 		if self.doctype=='CTX':
# 			# just building html based on existing Codes
# 			self.contenthtml = stylizeCaqdasToHtml(self)
# 		elif self.doctype=='TEI':
# 			# creating html based on Structure
# 			self.contenthtml = stylizeTeiToHtml(self)
# 		self.status='0'
# #		except:
# #			self.status='-1'
# 		self.save()
################################################ 








# DEPRECATED OLD way TO FETCH ALL TEXT
####################################################################
# return array of successive styled sentences (more styling made in template)
# the array is used in texte pagination in the view
# def makeArrayFromTextContent(texte):
# 	RESARRAY = []
# 	curTimePart = []
# 	curSentences = []
# 	
# 	sIdCur = texte.sentence_set.all().order_by('i','speaker','n')[0].speaker.id
# 	timeCur = 0
# 	onlyMargin = True
# 	
# 	for s in texte.sentence_set.all().order_by('i','speaker','n'):
# 		
# 		if s.i == timeCur: # SAME TIMEPART
# 			if s.speaker.id != sIdCur: # NEW SPEAKER
# 				curTimePart.append(curSentences)
# 				curSentences = []
# 			else: # SAME SPEAKER
# 				donothing=1
# 					
# 		else: # NEW TIMEPART
# 			curTimePart.append(curSentences)
# 			RESARRAY.append([onlyMargin,curTimePart])
# 			curTimePart = []
# 			curSentences = []
# 			onlyMargin = True
# 		
# 		timeCur = s.i 
# 		sIdCur = s.speaker.id
# 		if s.code.name != 'only_margin':
# 			onlyMargin = False
# 			
# 		curSentences.append(s)
# 	
# 	# flush last part
# 	curTimePart.append(curSentences)
# 	RESARRAY.append([onlyMargin,curTimePart])
# 	return RESARRAY
####################################################################














####################################################################
# DEPRECATED : Before, we were concatenating interventions
# def stylizeTeiToHtml(texte):
# 	htmlStr=""
# 	texte.statuscomplete=0
# 	texte.save()
# 	totalSentences=texte.sentence_set.count()
# 	# each-speaker-loop
# 	intCount=0
# 	for i in texte.intervention_set.all().order_by('i'):
# 		cId = i.speaker.id
# 		cName = i.speaker.name
# 		# COLOR is not here anymore, rather sent in the view as an array, styling speaker-class with javascript
# 		#cColor = getSpeakerColor(i.speaker)
# 		# style="background-color:'+cColor+';"
# 		speakNameDiv='<div class="text_speaker_name">'+cName+' <span class="text_speaker_namecount">.'+str(intCount)+'</span></div>'
# 		htmlStr+='<div class="text_speaker speaker_'+str(cId)+'" id="'+str(cId)+'_'+str(i.i)+'">'+speakNameDiv+stylizeTeiInterventionToHtml(i)+'</div>'
# 		intCount+=1
# 		compl=int(intCount*100/totalInterventions)
# 	 	# texte.save() is taking a lot of memory !!
# 		# MONITORING : print("MEMORY:"+str(psutil.phymem_usage()[3]))
# 		# saving texte only from time to time save A LOT of memory usage !!
# 		if compl!=texte.statuscomplete and compl%5==0:
# 			texte.statuscomplete = compl
# 			texte.save()
# 		#print("STATUS:"+str(texte.statuscomplete)+"/"+str(intCount)+":"+str(totalInterventions))
# 		#print("=========== (STYLING) MEMORY USAGE:"+str(psutil.phymem_usage()[3]))
#	return htmlStr
####################################################################




# ######## DEPRECATED !
# # old version, but keeped to style intervention in the search results !
# # todo: new version !
# def stylizeTeiInterventionToHtml(intervention):
# 	htmlStr=""
# 	for s in intervention.sentence_set.all().order_by('i'):
# 		typ = s.code.name
# 		try:
# 			endChar = SENTENCE_UTT_SYMBOLS[typ]
# 		except:
# 			# 'not_classified' was ".", now it's ""
# 			endChar = SENTENCE_UTT_SYMBOLS['not_classified']
# 		htmlStr+='<span class="'+typ+'">'+stylizeTeiSentenceToHtml(s)[1] + endChar + ' </span>'
# 	return htmlStr
# ####################################################################
# def stylizeTeiSentencesToHtml(sentList):
# 	res=""
# 	resOnlyMargin=True
# 	for s in sentList:
# 		onlyMargin,htmlMorc = stylizeTeiSentenceToHtml(s)
# 		res += htmlMorc + " "
# 		resOnlyMargin = resOnlyMargin and onlyMargin
# 	return [resOnlyMargin,res[:-1]]
# ####################################################################
# def stylizeTeiSentenceToHtml(sentence):
# 	htmlStr=""
# 	# flag to know if there is content to display or not, ie if we put it in "tex_part" div OR alone
# 	onlyMargin=True
# 	typ = sentence.code.name
# 	try:
# 		endChar = SENTENCE_UTT_SYMBOLS[typ]
# 	except:
# 		# 'not_classified' was ".", now it's ""
# 		endChar = SENTENCE_UTT_SYMBOLS['not_classified']
# 	for w in sentence.word_set.all().order_by('n'):
# 		we = w.wordentityspeaker.wordentity
# 		codetyp = we.code.codetype.name		# Ponctuation/Word
# 		code = we.code.name					# Silence/Incident/Comment/..
# 		val = we.content					# short,long pause/rire/changement de cassette
# 		if codetyp=='word':
# 			htmlStr+=val+' '
# 			onlyMargin=False
# 		elif codetyp=='ponctuation':
# 			htmlStr+=val+' '
# 		elif codetyp=='paraverbal':
# 			try:
# 				cssClass=CQDAS_CLASS[code]
# 			except:
# 				cssClass=CQDAS_CLASS['unknown']
# 			if code in ['silence','hesitation','interruption','inaudible']: # dont keep content			# A B C D
# 				htmlStr+='<div class="'+cssClass+'">&nbsp;</div>'
# 				onlyMargin=False
# 			elif code in ['comment','laugh','time','question','directed','incident']: # keep content	# E F G H I J
# 				incidentDescr = we.description
# 				htmlStr+='<a rel="text_tooltip" title="'+incidentDescr+'" class="'+cssClass+'"><div>&nbsp;</div></a>'
# 				if onlyMargin and code not in ['comment','time']:
# 					onlyMargin=False
# 			else: # unkown
# 				htmlStr+='<span class="'+cssClass+'">'+val+' </span>'
# 		else:
# 			htmlStr+=' [UNRECOGNIZED WORD] '
# 	return [onlyMargin,htmlStr+endChar]
# ####################################################################




















####################################################################
# def recursGetTeiContent(node,speakerDict):
# 	childs = node.getchildren()
# 	parts=[]
# 	#print "yuy"
# 	if len(childs)==0:
# 		#try:
# 		# keep pauses <pause/>
# 		if node.tag==XMLTEINMS+'pause':
# 			a='<div class="text_silence"> .. '
# 			b='</div>'
# 			parts += [a,node.text,node.tail,b]
# 		else:
# 			parts += [node.text,node.tail]
# 		#except:
# 			#parts=[]
# 	else:
# 		midpart = []
# 		for cnode in childs:
# 			midpart+=recursGetTeiContent(cnode,speakerDict)
# 
# 		########## keep '.' and '?' #<seg function="utterance" type="exclamative">
# #		if node.tag==XMLTEINMS+'seg': 
# #			typ=node.attrib['type']
# ##			if typ=='exclamative': # !
# ##			elif typ='declarative': # .
# ##			elif typ=='interrogative': # ?				
# ##			elif typ=='not_classified': # others
# #			a='<div class="text_utterance '+typ+'">'
# #			b='</div>'
# #			parts += [a]+[node.text]+midpart+[node.tail]+[b]
# 		########## keep turns of speech and identity of speakers
# 		if node.tag==XMLTEINMS+'u':
# 			speaker=node.attrib['who']
# 			#try:
# 			theid=speakerDict[speaker]['id']
# 			thecolor=speakerDict[speaker]['color']
# 			#except:
# 			#	theid="Unknown"
# 			a='<div class="text_speaker" id="'+theid+'" style="background-color:'+thecolor+';">'
# 			b='</div>'
# 			parts += [a]+[node.text]+midpart+[node.tail]+[b]
# 		########## keep paragraphs ?
# #		elif node.tag==XMLTEINMS+'div':
# #			a='<p>'
# #			b='</p>'
# #			parts += [a]+[node.text] + midpart + [node.tail]+[b]
# 		########## keep incidents
# 		elif node.tag==XMLTEINMS+'incident': #<incident><desc>blanc</desc></incident>
# 			descr=node.getchildren()[0].text
# 			parts += ['<span class="text_strong">['+descr+']</span>']
# 		########## normal case : we only keep text
# 		else:
# 			parts += [node.text] + midpart + [node.tail]
# 		# filter removes possible Nones in texts and tails
# 	#logger.info("STRINGIFY"+res)
# 	return parts
####################################################################










####################################################################
# tryout using djangotables
# DEPRECATED since we used jquery-datatables instead !
####################################################################
# for django_tables2
#class TextNameColumn(tables.Column):
#	def render(self, value):
#		return mark_safe('<a href="">%s</a>' % value)
####################################################################
# NB
# we do not use django tables anymore, cause we want more control over data
# so we use jquery datatables instead
####################################################################
# class TextTable(tables.Table):
# 	#name = TextNameColumn()
# 	name = tables.TemplateColumn('<a href="{% url reanalyse.reanalyseapp.views.edShow record.enquete.id record.id %}">{{ record.name }}</a>',verbose_name='Nom')
# 	
# 	# filesize
# 	size = tables.TemplateColumn('{{record.filesize}}'+' Ko')
# 	
# 	# status
# 	statcomplete = '{% if record.doctype == "TEI" and record.status != "0" %} {{record.statuscomplete}}%{% endif %}'
# 	status = tables.TemplateColumn('{{ record.get_status_display }}' + statcomplete, verbose_name='Status')
# 	
# 	#doctype = tables.Column(verbose_name='Type')
# 	doctype = tables.TemplateColumn( '{{ record.get_doctype_display }}', verbose_name='Type')
# 	speakerStr = '{% for p in record.speaker_set.all %}{% if forloop.counter < 99 %}<a href="{% url reanalyse.reanalyseapp.views.esShow record.enquete.id p.id %}">{{p.name}}</a>, {% endif %}{% endfor %}'
# 	speaker = tables.TemplateColumn('---')
# 	
# 	########## (txt/xml/html) Data Contents
# 	linkStr = '<a href="{% url reanalyse.reanalyseapp.views.ecShow c.enquete.id c.id %}">{{c.name}}</a>'
# 	codesStr= '{% for c in record.code_set.all %}{% if forloop.counter < 99 %}'+linkStr+', {% endif %}{% endfor %}'
# 	codes = tables.TemplateColumn('---')
# 	
# 	########## (txt/xml/html) Data Contents
# 	tStyle='<span style="color:red;">'
# 	dataStr='{% if record.content|length > 0 %}'+tStyle+'txt</span>&nbsp;{% endif %}{% if record.contenthtml|length > 0 %}'+tStyle+'html</span>&nbsp;{% endif %}{% if record.contentxml|length > 0 %}xml {% endif %}'
# 	parseStr='<a href="" onclick=\'doGetAtUrl("{% url reanalyse.reanalyseapp.views.edParseXml record.enquete.id record.id %}");return false;\'>parse </a>'
# 	refreshStr='<a href="" onclick=\'doGetAtUrl("{% url reanalyse.reanalyseapp.views.edStylizeContent record.enquete.id record.id %}");return false;\'>stylize </a>'
# 	contentavailable = tables.TemplateColumn( dataStr+'{% if record.doctype == "TEI" or record.doctype == "CTX" %}'+parseStr+refreshStr+'{% endif %}' , verbose_name='Data')
# 	
# 	########### description of document
# 	helpdescrimg ='<img src="{{ MEDIA_URL }}/images/helpcircle.png" alt="description"/>'
# 	description = tables.TemplateColumn('<a rel="tooltip" title="{{ record.description }}">'+helpdescrimg+'</a>')
# 	
# 	class Meta:
# 		# for css
# 		#attrs = {'id': 'enquetetexttable'}
# 		attrs = {'class': 'paleblue'}
# 		# order
# 		sequence = ("doctype","name","size","status","contentavailable","codes","speaker","description")
# ####################################################################
# # For speakers, we can also do it with django-tables...
# # or do it by hand, building a dictionnary in the view (let's try that for the moment)
# class SpeakerTable(tables.Table):
# 	name = tables.TemplateColumn('<a href="{% url reanalyse.reanalyseapp.views.esShow record.id %}">{{ record.name }}</a>',verbose_name='Participant')
# 	# todo : make it work
# 	attribute_set = tables.TemplateColumn('{% for a in record.attribute_set.all %}{{a.name}}{% endfor %}',verbose_name="Attributs")
# 	class Meta:
# 		# for css
# 		#attrs = {'id': 'enquetetexttable'}
# 		attrs = {'class': 'paleblue'}
# 		# order
# 		sequence = ("name","attribute_set")
# ####################################################################













####################################################################
# def stylizeTeiToHtmlDeprecated(texte):
# 	#
# 	#
# 	# !!!!!!!! Deprecated
# 	#
# 	#
# 	# easy solution: remove all tags except codes
# 	# only keeping
# 	# <incident><desc>descr of event</desc></incident>
# 	# <pause type="long/short" />
# 	
# # 	tree = etree.parse(texte.locationpath)
# # 	root = tree.getroot()
# # 	
# # 	persons = root.findall(XMLTEINMS+'teiHeader/'+XMLTEINMS+'profileDesc/'+XMLTEINMS+'particDesc/'+XMLTEINMS+'person')
# # 	speakerDict=dict()
# # 	for n,p in enumerate(persons):
# # 		pid=p.attrib[XMLNMS+'id']
# # 		name=p.findall(XMLTEINMS+'persName/'+XMLTEINMS+'abbr')[0].text
# # 		speakerDict['#'+pid]={'id':name,'color':HTML_COLORS[n%len(HTML_COLORS)]}
# # 	# todo: keep speakers identity in html
# # 	tnode = root.findall(XMLTEINMS+'text/'+XMLTEINMS+'body')[0]
# # 	arr = recursGetTeiContent(tnode,speakerDict)
# # 	return ' '.join(filter(None,arr))
####################################################################










####################################################################
## DEPRECATED ?
# def stylizeCaqdasToHtml(texte):
# 	
# 	alltxt = texte.content
# 	
# 	# get all Speaker and make color for each based on HTML_COLORS
# 	c=0
# 	thecolors=dict()
# 	for p in texte.speaker_set.all():
# 		thecolors[p.name]=HTML_COLORS[c%len(HTML_COLORS)]
# 		c+=1
# 	
# 	# get all offsets (in & out) and sort them as [offs,codename,codecat]
# 	vals=[]
# 	for quote in texte.quotation_set.all():
# 		parentCode=quote.code
# 		try:
# 			cat = parentCode.code.codetype
# 			val = 'unused'
# 		except:
# 			cat = 'speaker'
# 			val = parentCode.speaker.name # used to put id
# 		s = quote.offs.split(',')
# 		e = quote.offe.split(',')
# 		vals.append( [int(s[0]),int(s[1]), 's', cat, val] )
# 		vals.append( [int(e[0]),int(e[1]), 'e', cat, val] )
# 	#vals = [ [1,2,s,speaker] [1,5,e,speaker] [2,6,..] [8,12,..] ] > relative to line
# 	#print "VALS",vals
# 	
# 	# concatenate different lines of alltxt and make offsets global
# 	allStr=""
# 	allStrSplit=alltxt.split('\n')
# 	
# 	# from now on, we consider text as a single long string
# 	# keeping memory of "\n" locations, to replace them after with </br>
# 	alltxt='qqqq'.join(allStrSplit)
# 	
# 	nLines = [ len(l) for l in allStrSplit ]
# 	
# 	lineLen=[0] # no line-offset for first line
# 	globLen=0
# 	for l in allStrSplit:
# 		allStr+=l
# 		globLen+=len(l)+4 # +4 because we have "qqqq" to remember breaklines
# 		lineLen.append(globLen)
# 	nVals = [ [ lineLen[it[0]-1]+it[1]-1, it[2], it[3], it[4] ]  for it in vals ]
# 	#nVals = [ [2,s,speaker] [5,e,speaker] [152,..] ] > global
# 	nVals = sorted(nVals) # now that its global, sort it
# 
# #	for lem in lineLen:
# #		logger.info("len:"+str(lem))
# #	for val in nVals:
# #		logger.info("tablo:"+str(val[0])+" = "+val[1]+"/"+val[2])
# 			
# 	# stores classes to insert at each global offset
# 	classArr=range(len(nVals)) # may be smaller
# 	currentClasses=[]
# 	step=0
# 	currentPointeur=0
# 	for k in range(len(nVals)):
# 		flag = nVals[k][1]
# 		theCat = nVals[k][2]
# 		theVal = nVals[k][3]
# 		if theCat not in CQDAS_CLASS.keys():
# 			theCat="unknown"
# 		if flag=='s': # enter a class, adding style to the div
# 			currentClasses.append(CQDAS_CLASS[theCat])
# 		else: # out of class, removing style
# 			currentClasses.remove(CQDAS_CLASS[theCat])
# 		if theCat=='speaker':
# 			textToInsert= '<span class="'+' '.join(currentClasses)+'" id="'+theVal+'" style="background-color:'+thecolors[theVal]+';">'
# 		else:
# 			textToInsert= '<span class="'+' '.join(currentClasses)+'">'
# 		classArr[step]=textToInsert
# 		if nVals[k][0]!=currentPointeur: # advancing in txt
# 			currentPointeur=nVals[k][0]
# 			step+=1
# 		#print "OK:",currentPointeur,step,textToInsert
# 	#print "ARR CLASSES:",classArr
# 	
# 	# split the whole text by those offsets
# 	txtArr=[]
# 	
# 	# in case there is untagged text at the beginning of the file (without class)
# 	a=nVals[0][0]
# 	if a!=0:
# 		txtArr.append(alltxt[:a])
# 	else:
# 		txtArr.append("NOTHINGBEFORE")
# 	for k in range(len(nVals)-1):
# 		a=nVals[k][0]
# 		b=nVals[k+1][0]
# 		if a!=b:
# 			txtArr.append(alltxt[a:b])
# 	# in case there is untagged texte at the end
# 	if b<len(alltxt):
# 		txtArr.append(alltxt[b:])
# 	else:
# 		txtArr.append("NOTHINGAFTER")
# 	
# 	# reconstruct text with <div class=".."> to insert
# 	outStr=txtArr[0]
# 	for p in range(len(txtArr)-1):
# 		outStr += classArr[p] + txtArr[p+1] + '</span>'
# 	
# 	# Dealing with comments, allowing javascript to display them as tooltips
# 	# here we suppose that comments don't have divs in them
# 	# we replace all divs of "comment" class by a link
# #	tagpat = re.compile('(<div class="[\w _]*'+classTrans['comment']+'[\w _]*">)([^<]*)</div>')
# #	for u in tagpat.finditer(outStr):
# #		beg = u.group(1)
# #		thecomment = u.group(2)
# #		outStr = re.sub(tagpat,'<a class="tooltip" rel="tooltip" title="'+thecomment+'">'+beg+'[comment]</div></a>',outStr)
# 	
# 	#bringing back breaklines "from memory"
# 	outStr = re.sub(re.compile('qqqq'),'</br>',outStr)
# 	
# 	return outStr
####################################################################













#############			
# VERSION 1, deprecated soon..
#############
#class Moment(models.Model):
#	# for each enquete there is "moments" (ex. one interview one day)
#	enquete = models.ForeignKey(Enquete)
#	name = models.CharField(max_length=200)
#	description = models.CharField(max_length=200)
#	def __unicode__(self):
#		return self.name
#	def partsSortedList(self):
#		u=[p.partid for p in self.part_set.all]
##		al=self.part_set.all()
##		for p in al:
##			u.append([p.partid])
#		u = sorted(u)
#		logger.info("premier element de la liste:"+u[0])
#		return u
##############
#class Part(models.Model):
#	# for each text there is "parts" (ex. different parts/questions in the same interview)
#	moment = models.ForeignKey(Moment)
#	name = models.CharField(max_length=200)
#	description = models.CharField(max_length=200)
#	partid = models.CharField(max_length=200)
#	def getTextContent(self, tId):
#		splitted=content.split(';')
#		if k<len(splitted):
#			return splitted[k]
#		else:
#			return "no part for k:"+k
#	def __unicode__(self):
#		return self.name
##############
#class TextePart(models.Model):
#	texte = models.ForeignKey(Texte)
#	part = models.ForeignKey(Part)
#	partid = models.CharField(max_length=200)
#	content = models.TextField()
#	def __unicode__(self):
#		return self.partid
#################################################################










#################################################################
#def givesDictFromTwoTexts(t1, t2):
#	# takes 2 txts describing same "phase/moment"
#	# return an : array[i]=(phase_i in t1 , phase_i in t2)
#	return 0
#
#####################################################################
#def getAllSubNodesOnlyText(node):
#	return ''.join(filter(None, stringify_children(node)))
#def stringify_children(node):
#	childs = node.getchildren()
#	parts=[]
#	if len(childs)==0:
#		try:
#			parts += [node.text,node.tail]
#		except:
#			parts=[]
#	else:
#		# original:
#		#parts = ([node.text] + list( chain(*([c.text, tostring(c), c.tail] for c in childs)) ) + [node.tail])
#		midpart = []
#		for cnode in childs:
#			midpart+=stringify_children(cnode)
#		parts += [node.text] + midpart + [node.tail]
#		# filter removes possible Nones in texts and tails
#	#logger.info("STRINGIFY"+res)
#	return parts
#####################################################################









	##########
#	def parseXmlFileOld(self,localXmlPath):
#		# Creates Text Parts based on xml structure
#		#
#		#self.tree = ElementTree()
#		inFile = open(localXmlPath,'r')
#		self.tree = etree.parse(localXmlPath)
#		inFile.close()
#		self.root = self.tree.getroot()
#		
#		l = self.root.findall('link')
#		self.enqueteid = l[0].attrib['id']
#		self.name=localXmlPath.split("/")[-1]
#		#self.name="texte-"+localXmlPath+"-enq-"+self.enqueteid
#		t = self.root.findall('text')
#		self.texteid = t[0].attrib['id']
#		self.save()
#		for part in t[0].findall('div'):
#			partid = part.attrib['id']
#			#allcontent = getAllSubNodesOnlyText(part)
#			#allcontent = etree.tostring(part,pretty_print=True,encoding='utf-8')
#			allcontent = etree.tostring(part,encoding='utf-8')
#			# check if a PART exist to link it
#			try:
#				thepart = self.moment.part_set.get(partid=partid)
#			except: # create it
#				thepart = self.moment.part_set.create(partid=partid,name=partid)
#				
#			newtxtpart = TextePart(texte=self,part=thepart,content=allcontent,partid=partid)
#			newtxtpart.save()
#			# say hello to the new TEXTEPART
#			#logger.info("made NEW TEXTEPART:"+partid+"="+newtxtpart.content)
#		logger.info("made NEW TEXTE:"+self.texteid)
	##########
#	def getTextPart(self,partid):
#		try:
#			return stylizeXmltoHtml( self.textepart_set.get(partid=partid).content )
#			#return stylizeXmltoHtml( '<u who="#spksdq fdsq">  fdgsdfgds </u><strong> this<u>  fdgsdfgds </u> is stre</strong>dsfqfqs sdfqs' )
#		except:
#			return "no txtepart for this partid"





####################################################################################
#def stylizeXmltoHtml(inStr):
#	XMLHTML = dict()
#	XMLHTML['<u who="#blabla">']=['<div class="text_speaker">','</div>']
#	XMLHTML['<p>']=['<div class="text_p">','</div>']
#	#XMLHTML['<comment>']=['<span class="text_comment">','</span>']
#	XMLHTML['<strong>']=['<div class="text_strong">','</div>']
#	XMLHTML['<underline>']=['','']
#	for u in XMLHTML.keys():
#		tagpat = re.compile('<(\w+)( |>)')
#		ff = re.search(tagpat,u)
#		if ff!=None:
#			thetag = ff.group(1)
#			# replace start <tag>
#			if ff.group(2).startswith(' '): # with attributes
#				patt = re.compile('<'+thetag+' [^>^<]*>')
#			else:
#				patt = re.compile('<'+thetag+'>')
#			inStr = re.sub(patt,XMLHTML[u][0],inStr)
#			# replace end <tag>
#			patt = re.compile('</'+thetag+'>')
#			inStr = re.sub(patt,XMLHTML[u][1],inStr)
#	
#	# Dealing with silence
#	tagpat = re.compile('<silence>([^<^>]*)</silence>')
#	ff = re.search(tagpat,inStr)
#	if ff!=None:
#		thecomment = ff.group(1)
#		inStr = re.sub(tagpat,' <div class="text_silence"> (..) </div> ',inStr)
#			
#	# Dealing with comments, allowing javascript to display them as tooltips
#	tagpat = re.compile('<comment>([^<^>]*)</comment>')
#	ff = re.search(tagpat,inStr)
#	if ff!=None:
#		thecomment = ff.group(1)
#		inStr = re.sub(tagpat,'<a class="tooltip" rel="tooltip" title="'+thecomment+'">[comment]</a>',inStr)
#	
#	return inStr
###########################################################################







####################################################################
# first version - deprecated
#class Enquete(object):
#	def __init__(self,filepath):
#		logger.info("ENQUETE OBJECT CREATED with file:"+filepath)
#		self.tree = ElementTree()
#		self.tree.parse(filepath)
#		self.root = self.tree.getroot()
#	def getEnquete(self):
#		return self.root
#	def name(self):
#		return self.root.attrib['name']
#	def summary(self):
#		if self.root.attrib.has_key('summaryFile'):
#			return settings.REANALYSEESE_FILES+self.root.attrib['summaryFile']
#		else:
#			return False
#	def id(self):
#		return self.root.attrib['id']
#	
#	def chapters(self):
#		return [Chapter(chapter) for chapter in self.root.findall('chapter')]
#class Chapter(object):
#	def __init__(self,chapter):
#		self.el = chapter
#	def name(self):
#		return self.el.attrib['name']
#	def summary(self):
#		if self.el.attrib.has_key('summaryFile'):
#			return settings.REANALYSEESE_FILES+self.el.attrib['summaryFile']
#		else:
#			return False
#	def subChapters(self):
#		return [SubChapter(subChapter) for subChapter in self.el.findall('subchapter')]	
#class SubChapter(object):
#	def __init__(self,subChapter):
#		self.el = subChapter
#	def name(self):
#		return self.el.attrib['name']
#	def summary(self):
#		return self.el.attrib['summaryFile']
#	def mp3(self):
#		return self.el.attrib['mp3']
#	def ogg(self):
#		return self.el.attrib['ogg']
####################################################################










####################################################################################################################################
# DEPRECATED MODELS
####################################################################################################################################



# DEPRECATED, groups are People Attributes
#########################################
# class Group(models.Model):
#	enquete = models.ForeignKey(Enquete)
#	name = models.CharField(max_length=200) # Droite rigoriste, Divers, Gauche
#	attributes = models.ManyToManyField(Attribute)
#	def __unicode__(self):
#		return self.name
#########################################


# DEPRECATED NOW... to trash soon
#########################################
# class CodeType(models.Model):
# 	enquete = models.ForeignKey(Enquete)
# 	name = models.CharField(max_length=50)
# 	#description = models.TextField()
# 	def __unicode__(self):
# 		return self.name
#############
# class AbstractCode(models.Model):
# 	class Meta:
# 		abstract = True
# class CodeBase(AbstractCode):
# 	name = models.CharField(max_length=50)
# 	#status = models.CharField(max_length=?)
# 	def __unicode__(self):
# 		return self.name
#########################################







# Testing models on different databases ... à suivre
#################################
#class Poire(models.Model):
#	connection_name="default"
#	name = models.CharField(max_length=200)
#	description = models.TextField()
#	def __unicode__(self):
#		return self.name
#################################
#class Pomme(models.Model):
#	connection_name="enquetes"
#	name = models.CharField(max_length=200)
#	description = models.TextField()
#	def __unicode__(self):
#		return self.name
#	def save(self):
#		self.connection_name = "enquetes_"+self.name
#		settings.DATABASES[self.connection_name]= {'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#		'NAME': self.connection_name,
#		'USER': 'djgo',
#		'PASSWORD': 'ogjdogjd',
#		'HOST': '',
#		'PORT': '',
#	}
#		super(Pomme, self).save()
#################################
#class SousPomme(models.Model):
#	connection_name="enquetes"
#	pomme = models.ForeignKey(Pomme)
#	name = models.CharField(max_length=200)
#	def __unicode__(self):
#		return self.name
#################################






##############################################################################
# ATLASTI = we have raw text, we store every codes & his exact position
# This is DEPRECATED because too uncertain !
##############################################################################
# class Quotation(models.Model):
# 	texte = models.ForeignKey(Texte)	
# 	code = models.ForeignKey(CodeBase)
# 	# offsets locates code in the Text ("(START)line,offset,(END)line,offset")
# 	offs = models.CommaSeparatedIntegerField(max_length=50)
# 	offe = models.CommaSeparatedIntegerField(max_length=50)
# 	def __unicode__(self):
# 		return self.id
##############################################################################





##############################################################################
# OLDWAY : TEIXML = well coded : we store the text as a structure [Interventions > Sentences > Words]
##############################################################################
# DEPRECATED (unuseful!)
# class Intervention(models.Model):
# 	# Je ne le connais pas ! Enfin •• je crois ((rire)).
# 	enquete = models.ForeignKey(Enquete)
# 	texte = models.ForeignKey(Texte)
# 	speaker = models.ForeignKey(Speaker)
# 	#####
# 	contenttxt = models.TextField()
# 	contenthtml = models.TextField()
# 	##### time location
# 	i = models.BigIntegerField(default=0)
# 	o = models.BigIntegerField(default=0)
# 	######
# 	def __unicode__(self):
# 		return "Intervention"+str(self.i)+":"+self.speaker.name
##############################################################################