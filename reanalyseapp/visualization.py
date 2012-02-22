# -*- coding: utf-8 -*-
###########################################################################
# build dictionary json data for viz based on params sent from view
###########################################################################
from django.conf import settings

from reanalyse.reanalyseapp.models import *
from reanalyse.reanalyseapp.utils import *

# to randomly sort an array : random.shuffle(arr)
import random

# for raw search to do tag cloud using haystack/solr
from haystack.query import SearchQuerySet,SQ

# to get termVectors tf/df/tfidf using raw_queries with pythonsolr
import pythonsolr

# for graphs
import networkx

# for simil
from pattern.vector import *

import logging
###########################################################################







###########################################################################
def makeVisualizationObject(e,typ,descr):
	newVizu = Visualization(enquete=e,status='1',viztype=typ,description=descr)
	newVizu.save()
	newVizu.name = 'viz' + str(newVizu.id)
	newVizu.save()
	return newVizu
###########################################################################
# BUILD VISUALIZATION
def makeViz(e,typ,speakers=[],textes=[],attributetypes=[],count=0):
	# todo:
	# 1) only do something if texte is TEI
	# 2) test if same sort of viz exists (eg. don't do another StreamTimeline if already there)
	# 3) be smart ! eg. create tag cloud of speakers involved when only textes are selected
	
	newVizu = None
	
	#descr = VIZTYPESDESCR[typ]	# we used to set a different one for each
	descr = VIZTYPESDESCR		# now just invite user to update it (see globalvars.py)
	
	logging.info("makeViz:"+typ)
	
	if typ in ['Graph_SpeakersAttributes','Graph_SpeakersWords','Graph_SpeakersSpeakers']:
		newVizu = makeVisualizationObject(e,typ,descr)
		if speakers!=[]:
			for s in speakers:
				newVizu.speakers.add(s)
		if textes!=[]:
			for t in textes:
				newVizu.textes.add(t)
		newVizu.save()
	
	# todo: launch threads, to avoid blocking ?
	# NB: json update is made in the visMakeGraph...() methods
	# NB: for graphs, we feed speakers&textes, at least one musn't be empty
	
	################################################### General or using all list
	if typ=='StudyOverview': # todo: timeline with docs ?
		newVizu = makeVisualizationObject(e,typ,descr)
		d = visMakeStudyOverview(e)
		newVizu.json = simplejson.dumps(d,indent=2,ensure_ascii=False)
		newVizu.status = '0'
		newVizu.save()	
	################################################### General or using all list
	elif typ=='Graph_SpeakersSpeakers':
		visMakeSpeakersSpeakersGraph(e,newVizu,{'method':'solr'})
	elif typ=='Graph_SpeakersAttributes':
		visMakeSpeakersAttributesGraph(e,newVizu,{'where':textes,'who':speakers,'whoatt':attributetypes})
	elif typ=='Graph_SpeakersWords':
		visMakeTermVectorGraph(e,newVizu,{'count':10,'who':speakers}) # NB: count means maxWordCount for each speaker
	###################################################
	elif typ=='Attributes':
		newVizu = makeVisualizationObject(e,typ,descr)
		if speakers==[]:
			if textes==[]:
				speakers = e.speaker_set.exclude(ddi_type='INV')
			else:
				speakers=[]
				for t in textes:
					for s in t.speaker_set.all():
						if s not in speakers:
							speakers.append(s)
		d = visMakeAttributes(e,{'where':textes,'who':speakers})
		for s in speakers:
			newVizu.speakers.add(s)
		for t in textes:
			for s in t.speaker_set.all():
				newVizu.speakers.add(s)
		newVizu.json = simplejson.dumps(d,indent=2,ensure_ascii=False)
		newVizu.status = '0'
		newVizu.save()		
	################################################### For every speaker in list or for all
	elif typ=='Cloud_SolrSpeakerTagCloud':
		###### one cloud for each text
		if speakers==[]:
			if textes==[]:
				textes = Texte.objects.filter(doctype='TEI')
			for t in textes:
				spks = t.speaker_set.all()
				newVizu = makeVisualizationObject(e,typ,descr)
				d = visMakeTagCloudFromTermVectors(e,{'count':count,'who':spks})
				for spk in spks:
					newVizu.speakers.add(spk)
				newVizu.json = simplejson.dumps(d,indent=2,ensure_ascii=False)
				newVizu.status = '0'
				newVizu.save()
		####### one cloud for group of speaker
		else:
			newVizu = makeVisualizationObject(e,typ,descr)
			#d = visMakeSolrTagCloud(e,{'count':MaxWords,'who':speakerIds,'what':'content_c_auto'})
			#d = visMakeSolrTagCloud(e,{'count':MaxWords,'who':speakerIds,'what':'text'})
			d = visMakeTagCloudFromTermVectors(e,{'count':count,'who':speakers})
			for s in speakers:
				newVizu.speakers.add(s)
			newVizu.json = simplejson.dumps(d,indent=2,ensure_ascii=False)
			newVizu.status = '0'
			newVizu.save()
	################################################### For every text in list
	elif typ=='TexteStreamTimeline':
		nViz={}
		# first create all viz objects (loading status...)
		for t in textes:
			nViz[t.id] = makeVisualizationObject(e,typ,descr)
			nViz[t.id].textes.add(t)
			for s in t.speaker_set.all():
				nViz[t.id].speakers.add(s)
		# then create json
		for t in textes:
			newVizu = nViz[t.id]
			d = visMakeStreamTimeline(e,{'where':t})
			newVizu.json = simplejson.dumps(d,indent=2,ensure_ascii=False)
			newVizu.status = '0'
			newVizu.save()
	###################################################
	elif typ=='Overview':
		newVizu = makeVisualizationObject(e,typ,descr)
		d = visMakeOverview(e)
		newVizu.json = simplejson.dumps(d,indent=2,ensure_ascii=False)
		newVizu.status = '0'
		newVizu.save()
	###################################################			
	
	
	# NB: if multiple viz are created, only the last one will be returned !
	return newVizu
###########################################################################










###########################################################################
# little stacked horizontal repartition of speakers in a text
# data is normalized
# used in Document Table View
def getDictLittleSpeakerSizesInText(t):
	res={}
	arrSpeakers=[] 	# list of speakers
	nCumulated=0
	nSentencesTotalGlobal=0
	for txt in Texte.objects.filter(enquete=t.enquete,doctype='TEI').all():
		nSentencesTotalGlobal = max(nSentencesTotalGlobal, Sentence.objects.filter(texte=txt).count())
	nSentencesTotalTexte = Sentence.objects.filter(texte=t).count()
	for s in t.speaker_set.all().order_by('ddi_type'):
		#Sentence.objects.filter(texte=t,speaker=s).annotate(longueur=Length('content')).aggregate(Sum('longueur'))
		nCur = Sentence.objects.filter(texte=t,speaker=s).count()
		arrSpeakers.append({'id':s.id,'from':nCumulated,'count':nCur,'name':s.name})
		nCumulated += nCur
	res['maxGlobal']=nSentencesTotalGlobal
	res['maxCurrent']=nSentencesTotalTexte
	res['speakers']=arrSpeakers	
	return res
###########################################################################












###########################################################################
###########################################################################
###########################################################################
# SIMILARITY BETWEEN SPEAKERS, different ways to do it...
###########################################################################
# SIMILARITY GRAPH 1
# use all the stored ngrams from Tfidf solr calculation
# BAD : very expensive !
# def getSimilOf(s1,s2):
# 	simil=0
# 	for ng in Ngram.objects.all():
# 		try:
# 			tf1=NgramSpeaker.objects.get(speaker=s1,ngram=ng).tfidf
# 		except:
# 			tf1=0
# 		try:
# 			tf2=NgramSpeaker.objects.get(speaker=s2,ngram=ng).tfidf
# 		except:
# 			tf2=0
# 		simil += tf1*tf2
# 	# todo: optimize like...?
# 	#sum(i*j for i, j in zip(v1, v2))
# 	return simil
# def makeSimilGraphUsingTfidf(e):
# 	k=1
# 	g=networkx.Graph()
# 	for s1 in e.speaker_set.all().order_by('id'):
# 		g.add_node(s1.name)
# 		for s2 in e.speaker_set.all().order_by('id')[k:]:
# 			simil = getSimilOf(s1,s2)
# 			g.add_edge(s1.name,s2.name,{'weight':simil})
# 		k+=1	
# 	outFilePath = settings.REANALYSEDOWNLOADPATH+"e" + str(e.id) + "similTfidfGraph" +".gexf"
# 	networkx.readwrite.gexf.write_gexf(g,outFilePath)
####################################################################
# SIMILARITY GRAPH 2
# use pattern OR solrqueries to fetch similar documents
def visMakeSpeakersSpeakersGraph(e,viz,param):
	method = param['method']
	
	if method=='pattern':
		#################### USING PATTERN (deprecated ? only english !)
		g=networkx.Graph()
		corpus=Corpus()
		for s in e.speaker_set.all():
			spker = Document(s.contenttxt,threshold=0,name=str(s.id)+":"+s.name)
			corpus.append(spker)
		for spk in corpus:
			g.add_node(spk.name)
		for spk in corpus:
			rels=corpus.related(spk)
			for r in rels:	
				g.add_edge(spk.name,r[1].name,{'weight':r[0]})
	
	else:
		##################### USING SOLR SIMILARITY BETWEEN DOCS (ie SPEAKERS)
		g=networkx.DiGraph()
		for s in e.speaker_set.all().order_by('id'):
			di={'label':s.name,'category':'Speaker','color':s.color}
			# add all attributes
			for atype in e.attributetype_set.all():
				for att in s.attributes.filter(attributetype=atype):
					di.update({'att_'+atype.name:att.name})
			g.add_node("Speaker_"+str(s.id),di)
			arr = getSolrSimilarArray(s,0)
			# return array of [score,sId,sName]
			for r in arr:
				g.add_edge("Speaker_"+str(s.id),"Speaker_"+str(r[1]),{'weight':r[0]*100.0})
	
	outFilePath = settings.REANALYSEDOWNLOADPATH+"e" + str(e.id) + viz.name +".gexf"
	networkx.readwrite.gexf.write_gexf(g,outFilePath)

	nN = str(g.number_of_nodes())
	nE = str(g.number_of_edges())
	viz.description='\
		Speakers-Speakers graph ('+nN+' nodes, '+nE+' edges)<br/>\
		- <b>Speakers</b> (all attributes)<br/>\
		edge weight = cosine-tfidf-similarity computed using solr queries'
		
	viz.name = viz.name + '_graph_spk-spk_'+nN+'n_'+nE+'e'
	viz.locationpath = outFilePath
	viz.status='0'
	viz.save()
########################################################################### MAKE GRAPH FROM ALL SPEAKERS + WORDS
def visMakeTermVectorGraph(e,viz,param):
	speakers = param['who']
	howmany = param['count']
	
	outFilePath = settings.REANALYSEDOWNLOADPATH +"e" + str(e.id) + viz.name +".gexf"
	g=networkx.DiGraph()
	
	termVectorDic={}

	if speakers==[]:
		speakers = e.speaker_set.all()
	
	# make spk nodes in any case
	for s in speakers:
		di={'label':s.name,'category':'Speaker','color':s.color}
		# add all attributes
		for atype in e.attributetype_set.all():
			for att in s.attributes.filter(attributetype=atype):
				di.update({'att_'+atype.name:att.name})
		g.add_node('Speaker_'+str(s.id),di)
		# deprecated : before we stored all the values, to be able to filter ngrams...
		#termVectorDic[s.id] = getSolrTermVectorsDict([s],'ngrams',count=howmany,mintn=3)

	############ USAGE A = keeping all ngrams(tf/df/tfidf) from Solr
# 	for s in speakers:
# 		logging.info("making speakers-words graph:looking at speaker:"+s.name)
# 		wdic = getSolrTermVectorsDict([s],'ngrams',count=howmany,mintn=3)
# 		for w in wdic.keys():
# 			edgedic = wdic[w]
# 			# ngram nodes are quite simple
# 			dic = {'label':w,'category':'Ngram','color':'#202020'}
# 			g.add_node('Word_'+w[:7],dic)
# 			# the edges store tfidf values
# 			edgedic.update({'weight':edgedic['tfidf']})
# 			g.add_edge('Speaker_'+str(s.id),'Word_'+w[:7],edgedic)			
	
	############ USAGE B = todo: keeping all ngrams from django stored models
	for s in speakers:
		for ngs in s.ngramspeaker_set.all():
			ng=ngs.ngram
			# ngram nodes are quite simple
			ngramdic = {'label':ng.content,'category':'Ngram','color':'#202020'}
			g.add_node('Word_'+str(ng.id),ngramdic)
			# the edges store tfidf values
			edgedic={'weight':float(ngs.tfidf),'tn':int(ngs.tn),'tf':float(ngs.tf),'tfidf':float(ngs.tfidf)} # float() cause long type > pb in gexf write
			g.add_edge('Speaker_'+str(s.id),'Word_'+str(ng.id),edgedic)				
	
	############ USAGE C = DEPRECATED ? filtering solr-fetched-ngrams to keep only ngrams within a 'seuil'
# 	keptwords = []
# 	alledges = []
# 	for s in speakers:
# 		wdic = termVectorDic[s.id]
# 		for w in wdic.keys():
# 			edgedic = wdic[w]
# 			#curDn = edgedic['dn']
# 			#curTf = edgedic['tn']
# 			#curDf = edgedic['df']
# 			curTfidf = edgedic['tfidf']
# 			
# 			###### only keep
# 			keepword = curTfidf>=0.2	# only high tfidf (0.11 works well (~15 words per speaker)
# 			
# 			if keepword:
# 				# NB: add edges with other Speakers for that word, even if tfidf < minTfidf
# 				# NB: if there is none, just keep word as speaker attribute
# 				isMultipleLink = True in [ (s.id!=sid and w in thedic.keys()) for sid,thedic in termVectorDic.items()]
# 				if isMultipleLink:
# 					alledges = []
# 					for s2 in speakers:
# 						if w in termVectorDic[s2.id].keys():
# 							edgdic2 = termVectorDic[s2.id][w]
# 							edgdic2.update({'Weight':edgdic2['tfidf']})
# 							alledges.append( ['Speaker_'+str(s2.id),'Word_'+w, edgdic2] )
# 					d={}
# 					d['node'] = 'Word_'+w
# 					d['attributes'] = {'label':w,'category':'Word','color':'#202020'}
# 					d['edges'] = alledges
# 					keptwords.append(d)
# 				else:
# 					# just update speaker-node attribute with 'word' for information
# 					g.node['Speaker_'+str(s.id)]['otherwords'] += w+', '	
# 	for pac in keptwords:
# 		g.add_node(pac['node'], pac['attributes'])
# 		for epac in pac['edges']:
# 			g.add_edge(epac[0],epac[1],epac[2])
	
	networkx.readwrite.gexf.write_gexf(g,outFilePath)
	nN = str(g.number_of_nodes())
	nE = str(g.number_of_edges())
	viz.description='\
		Speakers-Ngrams(solr) graph ('+nN+' nodes, '+nE+' edges)<br/>\
		- <b>Speakers</b> (all attributes)<br/>\
		- <b>Ngrams</b> (content,df/tf/tfidf)'
		
	viz.name = viz.name + '_graph_spk-ngr_'+nN+'n_'+nE+'e'
	viz.locationpath = outFilePath
	
	
	############## also build json version of graph, (used by d3.js)
# 	d={}
# 	thenodes=[]
# 	theedges=[]
# 	labels = networkx.get_node_attributes(g,'label')
# 	categories = networkx.get_node_attributes(g,'category')
# 	colors = networkx.get_node_attributes(g,'color')
# 	weights = networkx.get_edge_attributes(g,'Weight')
# 	for n in g.nodes():
# 		thenodes.append({'label':labels[n], 'category':categories[n], 'color':colors[n]})
# 	for e in g.edges():
# 		theedges.append({'source':g.nodes().index(e[0]), 'target':g.nodes().index(e[1]), 'weight':weights[e]})
# 	d['nodes']=thenodes
# 	d['edges']=theedges
# 	viz.json = simplejson.dumps(d,indent=2,ensure_ascii=False)
	##############
	
	viz.status='0'
	viz.save()
###########################################################################
def visMakeSpeakersAttributesGraph(enquete,viz,param):
	speakers = param['who']
	textes = param['where']
	attributetypes = param['whoatt']
	
	if speakers==[]:
		if textes==[]:
			speakers = enquete.speaker_set.all()
		else:
			speakers=[]
			for t in textes:
				for s in t.speaker_set.all():
					if s not in speakers:
						speakers.append(s)

	if attributetypes==[]:
		attributetypes = enquete.attributetype_set.all()
		
	outFilePath = settings.REANALYSEDOWNLOADPATH+"e" + str(enquete.id) + viz.name +".gexf"
	g=networkx.DiGraph()
	# Speaker Nodes
	for s in speakers:
		colAr = htmlColorToRgb(s.color)
		# 'viz':{ 'color':{'r':colAr[0],'g':colAr[1],'b':colAr[2]} }
		di = {'label':s.name,'category':'Speaker','color':s.color}
		# add all attributes
		for atype in enquete.attributetype_set.all():
			for att in s.attributes.filter(attributetype=atype):
				di.update({'att_'+atype.name:att.name})
		g.add_node('Speaker_'+str(s.id),di)
		######r="239" g="173" b="66" a="0.6"
	# Attributes Nodes & Links
	for att in enquete.attribute_set.all():
		if att.attributetype in attributetypes: ## only keep listed attributeTypes
			di = {'label':att.name,'category':'Attribute','attributetype':att.attributetype.name,'color':'#202020'}
			g.add_node('Attribute_'+str(att.id),di)
			for s in att.speaker_set.all():
				if s in speakers: ## only keep listed speakers
					g.add_edge('Speaker_'+str(s.id),'Attribute_'+str(att.id),{'weight':1})
	networkx.readwrite.gexf.write_gexf(g,outFilePath)
	nN = str(g.number_of_nodes())
	nE = str(g.number_of_edges())
	viz.description='\
		Speakers-Attributes graph ('+nN+' nodes, '+nE+' edges)<br/>\
		- <b>Speakers</b> (all attributes)<br/>\
		- <b>Attributes</b> (name,type)'
		
	viz.name = viz.name + '_graph_spk_att_'+nN+'n_'+nE+'e'
	viz.locationpath = outFilePath
	
	############## also build json version of graph, (used by d3.js)
# 	d={}
# 	thenodes=[]
# 	theedges=[]
# 	thelegend=[]
# 	labels = networkx.get_node_attributes(g,'label')
# 	categories = networkx.get_node_attributes(g,'category')
# 	# ids = "spk_"speaker.id or "att_"attributetype.id (not unique!)
# 	# this is to help d3 make relation between legend & objects (show/hide)
# 	ids = networkx.get_node_attributes(g,'categoryid')
# 	colors = networkx.get_node_attributes(g,'color')
# 	for n in g.nodes():
# 		if categories[n]=='Speaker':
# 			thcat='spk_'
# 		else:
# 			thcat='att_' 
# 		thenodes.append({'catid':thcat+str(ids[n]), 'label':labels[n], 'category':categories[n], 'color':colors[n]})
# 	for e in g.edges():
# 		theedges.append({'source':g.nodes().index(e[0]), 'target':g.nodes().index(e[1])})
# 	# now fill legend
# 	for attype in attributetypes:
# 		#attliststr = "/".join([ at.name for at in attype.attribute_set.all() ])
# 		thelegend.append({'catid':"att_"+str(attype.id), 'label':attype.name, 'category':attype.name, 'color':'#202020'})
# 	for s in speakers:
# 		thelegend.append({'catid':"spk_"+str(s.id), 'label':s.name, 'category':'Speaker', 'color':s.color})
# 	d['nodes']=thenodes
# 	d['edges']=theedges
# 	d['legend']=thelegend
# 	d['nattributes']=len(attributetypes)
# 	viz.json = simplejson.dumps(d,indent=2,ensure_ascii=False)
	##############
	
	viz.status='0'
	viz.save()
###########################################################################






###########################################################################
def visMakeStudyOverview(e):
	res={}
	docs=[]
	for t in e.texte_set.all():
		dic={}
		dic['id']=t.id
		dic['name']=t.name
		dic['type']=t.doctype
		dic['cat']=t.doccat
		dic['date']=t.date.strftime("%d/%m/%y")
		dic['size']=t.filesize
		dic['nspeakers']=t.speaker_set.count()
		docs.append(dic)
	res['documents']=docs
	return res
###########################################################################







###########################################################################
def visMakeOverview(e):
	res={}

	##### TRYOUT A : GRAPH
#	thenodes=[]
#	theedges=[]
# 	spkIdDic={}
# 	for s in e.speaker_set.all():
# 		thenodes.append({'id':'spk_'+str(s.id),'label':s.name,'category':'Speaker','color':s.color})
# 		spkIdDic[s.id]=len(thenodes)-1
# 	for t in e.texte_set.filter(doctype='TEI'):
# 		thenodes.append({'id':'doc_'+str(t.id),'label':t.name,'category':'Document','color':'lightgray'})
# 		for s in t.speaker_set.all():
# 			theedges.append({'source':len(thenodes)-1, 'target':spkIdDic[s.id]})
#	res['nodes']=thenodes
#	res['edges']=theedges	

	##### TRYOUT B : Simple left/right lists with paths
# 	links=[]
# 	for t in e.texte_set.filter(doctype='TEI').order_by('-id'):
# 		for s in t.speaker_set.exclude(ddi_type='INV'):
# 			#w=0
# 			#if s.name.endswith('H') and random()>0.2:
# 			#	w=50+50*random()
# 			tdic={'id':t.id,'label':t.name,'weight':0}
# 			sdic={'id':s.id,'label':s.name,'weight':0}
# 			ndoc=t.speaker_set.exclude(ddi_type='INV').count()
# 			links.append({'doc':tdic,'spk':sdic,'ndoc':ndoc})
# 	res['links']=links
	
	##### TRYOUT C : only speakers
	links=[]
	for s in e.speaker_set.exclude(ddi_type='INV'):
		links.append({'spk':{'id':s.id,'label':s.name,'weight':0}})
	res['links']=links
	return res
###########################################################################









###########################################################################
# attributes "chronogram", rollovable
def visMakeAttributes(e,param):
	speakers = param['who']
	textes = param['where']
	#attributeTypeIds = param['whoatt']
	
	res={}
	
	attributetypes = e.attributetype_set.exclude(name__startswith='_')
	
	attnames=[{'id':a.id,'name':a.name} for a in attributetypes]
	spknames=[]
	for s in speakers:
		attvalues=[ a.id for a in s.attributes.exclude(attributetype__name__startswith='_') ]
		spknames.append({'id':s.id,'name':s.name,'values':attvalues})

	attributes=[]
	for attype in attributetypes:
		attrow=[]
		#for attval in attype.attribute_set.annotate(nSpk=Count('speaker')).order_by('-nSpk'):
		for attval in attype.attribute_set.all():
			curspk=[]
			for s in speakers:
				if attval in s.attributes.all():
					curspk.append(s.id)
			if len(curspk)>0:
				attrow.append({'speakers':curspk,'id':attval.id,'name':attval.name})
		attributes.append(attrow)

	res['attnames']=attnames
	res['spknames']=spknames	
	res['attributes']=attributes
	
	return res
###########################################################################












###########################################################################
# streamed timeline with paraverbal
#
#		SPEAKERS
# 		thedata.data is an array [ forSpeaker1, forSpeaker2, forSpeaker3 ] :
# 		where forSpeaker1 = [ {x:0,y:nSentencesForPeriod0}, {x:1,y:nSentencesForPeriod1}, ... ]
# 		where forSpeaker2 = ...
#		PARAVERBAL
#		par each paraverbal, a simple array with successive values (simple chart, quoi)
#		
def visMakeStreamTimeline(e,param):
	# step = window width in which we count paraverbal/sentences occurences
	step = 3 						# ie. counting spk & paraverbal in a "window" of width "step" (3 sentences at a time)
	#factorParaverbal = 10*step		# height is managed in d3 (deprecated:y division factor for paraverbal (outvalue should be normalized in [0,1])
	res={}
	t = param['where']
	
	spk_layers=[]
	spk_ids=[]
	par_layers=[]
	par_ids=[]
	
	try:
		maxPeriods = t.sentence_set.all().aggregate(Max('i')).values()[0]
	except:
		maxPeriods = 0
	nSteps = 1+int(maxPeriods/step) # one more if nSentences undivisible by step
	
	paravList=['silence','laugh','hesitation','interruption','break']
	par_colors=['#BFBD9F','#D9FF00','#517368','#ED5300','#EC993B']
	
	speakers = t.speaker_set.order_by('-ddi_type')
		
	############# init
	for s in speakers:
		spk_layers.append([ {'x':k, 'y':0,'info':s.name} for k in range(nSteps) ])
		spk_ids.append([s.id,s.name])
	for i,p in enumerate(paravList):
		par_layers.append([ 0 for k in range(nSteps) ])
		par_ids.append([i,p])
	
	maxParavbCount = 0
	############# fill it
	#c=0
	#k=0 # k increment in each "window-step" (for ex. here every 3 sentence) 
	for sent in t.sentence_set.order_by('i'):
		# which step k ?
		k = int(sent.i/step)
		# number of sentences
		ns = t.sentence_set.filter(i__range=(k*step,(k+1)*step-1)).count()
		logging.info("FOR_k:"+str(k)+" : "+str(ns))
		# speakers
		spk = sent.speaker
		spk_layers[ spk_ids.index([spk.id,spk.name]) ][k]['y'] += 1.0/float(ns)
		# paraverbal
		for w in sent.word_set.all(): # assuming there is only paraverbal in words
			par = w.wordentityspeaker.wordentity.code.name
			if par in paravList:
				par_layers[ paravList.index(par) ][k] += 1/float(step)
				maxParavbCount = max(maxParavbCount,par_layers[ paravList.index(par) ][k])
	
	res['spk_layers']=spk_layers
	res['spk_ids']=spk_ids

	res['par_layers']=par_layers
	res['par_ids']=par_ids
	res['par_colors']=par_colors
	
	# we can send maximum prvb value(s) or let js do it...
	res['maxParavbCount']=maxParavbCount	# maximum y-value for parvb
	
	res['period']=step				# one value for each 'step' value of i		ex. 3
	res['maxPeriods']=maxPeriods 	# maximum i for all the i-o of sentences	ex. 15
	res['nPeriods']=nSteps			# number of values							ex. 5
	
	return res
###########################################################################
# simple d3 (rect)timeline with paraverbal
# deprecated, since we use now d3 stream graph
# def visMakeParaverbalTimeline(e,param):
# 	res={}
# 	t = param['where']
# 	
# 	# first get total count of words to scale
# 	totalWords = Word.objects.filter(sentence__intervention__texte=t).count()
# 	
# 	# then run through all text
# 	speakerArr=[]
# 	paravList=['silence','laugh','hesitation','interruption','time']
# 	paravArr=[]
# 	curWord=0
# 	for i in t.intervention_set.all().order_by('i'):
# 		lastWord=curWord
# 		lastId=i.speaker.id
# 		for s in i.sentence_set.all().order_by('i'):
# 			for w in s.word_set.all().order_by('n'):
# 				we = w.wordentityspeaker.wordentity
# 				descr = we.description
# 				codename = we.code.name
# 				codetyp = we.code.codetype.name
# 				if codetyp=='paraverbal' and codename in paravList:
# 					paravArr.append({'id':i.speaker.id,'paraverbal':paravList.index(codename),'count':curWord,'content':descr})
# 				curWord+=1
# 		speakerArr.append({'id':lastId,'in':lastWord,'out':curWord})
# 	res['totalwords']=totalWords
# 	res['lastword']=curWord
# 	res['speakers']=speakerArr
# 	res['paraverbaltypes']=paravList
# 	res['paraverbal']=paravArr
# 	return res
###########################################################################
















###########################################################################
###########################################################################
###########################################################################
# SOLR RAW QUERIES
########################################################################### SOLR RAW QUERIES DO GET SIMILAR SPEAKERS
def getSolrSimilarArray(speaker,maxcount):
	if maxcount==0:
		maxcount = speaker.enquete.speaker_set.count()
	p = {'fq':'django_ct:(reanalyseapp.speaker)','mlt':'true','mlt.fl':'ngrams','mlt.mindf':1,'mlt.mintf':1,'fl':'score','mlt.count':maxcount}
	q = 'speakerid:'+str(speaker.id)
	conn = pythonsolr.Solr( settings.HAYSTACK_SOLR_URL )
	r = conn.search(q,**p)
	array=[]
	speakerkey = r.result['moreLikeThis'].keys()[0]
	for res in r.result['moreLikeThis'][speakerkey]['docs']:
		try:
			sId = int(res['speakerid'])
			speaker = Speaker.objects.get(id=sId)
			array.append( [res['score'],speaker.id,speaker.name] )
		except:
			logging.info("epic fail in getSolrSimilarArray (compairing speakers from different enquete!) from speaker:"+str(speaker.id))
	return array
########################################################################### SOLR RAW QUERIES DO GET WORD LIST (graph,tagcloud,...)
def getSolrTermVectorsDict(speakers,field,count,mintn): # field = 'text'/'ngrams'
	# USING PYSOLR or PYTHONSOLR : same syntax
	# http://jiminy-dev.medialab.sciences-po.fr:8983/solr/select?q=speakerid:36&fq=django_ct:(reanalyseapp.speaker)&qt=tvrh&fl=text&tv.fl=ngrams&tv.all=true
	p = {'fq':'django_ct:(reanalyseapp.speaker)','qt':'tvrh','fl':'text','tv.fl':field,'tv.all':'true','wt':'json'}
	
	q=None
	for s in speakers:
		if q==None:
			q='(speakerid:'+str(s.id)
		else:
			q=q+' OR speakerid:'+str(s.id)
	q=q+')'
	
	conn = pythonsolr.Solr( settings.HAYSTACK_SOLR_URL )
	r = conn.search(q,**p)

	# !!!!! r.result['termVector'] only available in pythonsolr
	# looking at: https://bitbucket.org/cogtree/python-solr/src/dc20a25f7ca9/pythonsolr/pysolr.py
	
	# decoding results
	tv = r.result['termVectors'][0]
	if tv=='warnings':
		tv = r.result['termVectors'][3]
	else:
		tv = r.result['termVectors'][1]
		
	tv = list2dict(tv)
	
	# "parse" results manually
	
	# NB: For SOLR : TF=nTermOccurences, DF=nDocumentOcurrences, TFIDF=TF/DF
	# We need frequency, not nOccurrences !!
	# so:
	totalDocuments=0
	totalTerms=0
	
	for t in Texte.objects.filter(doctype='TEI').all():
		if t.contenttxt!="":
			totalDocuments+=1
	
	try:
		totalTerms = len(tv[field])
		res = list2dict(tv[field])
		
		# first transform all data in dict
		alldic={}
		for k,v in res.iteritems():
			d = list2dict(v)
			alldic.update({k:d})
		
		# then keep words wanted
		out={}
		for w,d in alldic.items():
			keepw = len(w)>2
			###### RULE 1 : dont keep ngrams which appear only 1 time for that speaker and never else (df=tf=1)
			keepw = keepw and d['df']+d['tf']!=2
			###### RULE 1 bis: keep ngrams that appears at least mintn
			keepw = keepw and d['tf']>=mintn
			###### RULE 2 : dont keep ngrams included in other-longer-word (if same df/tf)
			keepw = keepw and not True in [(w in otherw and w!=otherw and d['df']==alldic[otherw]['df'] and d['tf']==alldic[otherw]['tf']) for otherw in alldic.keys()]
			
			if keepw:
				df = d['df']/float(totalDocuments)
				tf = d['tf']/float(totalTerms)
				tfidf = 1000*tf/df
				newd = {'dn':d['df'],'tn':d['tf'], 'df':df, 'tf':tf, 'tfidf':tfidf}
				out[w] = newd
		if len(out)==0:
			return {'nongramsfoundwith_mintn='+str(mintn)+"_spk="+"_".join([str(s.id) for s in speakers]):{'df':0,'tf':0,'dn':0,'tn':0,'tfidf':0}}
		# todo: only keep 'n' top wanted based on tfidf (can we do it in solr query rather than python ?)
		# we can do it here, or later when making graph/tagcloud
		 
		# 1. get all words with tfidf and sort
	# 	wtfs = [ [v['tfidf'],k] for k,v in out.items() ]
	# 	wtfs = sorted(wtfs, key=lambda a: -a[0])
	# 	
	# 	# 2.
	# 	outF={}
	# 	for w in wtfs[:maxcount]:
	# 		outF[w[1]]=out[w[1]]
		
		return out
		# 'text': {'df': 24, 'tf': 4, 'tf-idf': 0.16666666666666666 }
		# 'tout': {'df': 464, 'tf': 1, 'tf-idf': 0.0021551724137931034 }
	except:
		return {'nosolrtermvectordict_spk='+"_".join([str(s.id) for s in speakers]):{'df':0,'tf':0,'dn':0,'tn':0,'tfidf':0}}
####################################################################
# to avoid querying solr everyday, we store ngrams in DB
def makeAllTfidf(e):
	for s in e.speaker_set.all():
		logging.info("now reseting tfidf ngrams for speaker:"+str(s.id))
		s.ngramspeaker_set.all().delete()
		termd = getSolrTermVectorsDict([s],'ngrams',count=0,mintn=3)
		for w in termd.keys():
			d=termd[w]
			newNgram,isnew = Ngram.objects.get_or_create(enquete=e,content=w,df=d['df'])	
			newNgramSpeaker,isnew = NgramSpeaker.objects.get_or_create(enquete=e,ngram=newNgram,speaker=s,tf=d['tf'],tn=d['tn'],tfidf=d['tfidf'])
####################################################################













###########################################################################
def visMakeTagCloudFromTermVectors(e,param):
	speakers = param['who']
	howmany = int(param['count'])
	if howmany==0:
		howmany=200
	#similcount = param['similcount']

	wordsArr=[]
  	
  	############################################# SOLR QUERY !
  	#if len(speakers)>1:
	d = getSolrTermVectorsDict(speakers,'ngrams',count=howmany,mintn=3)
	for w in d.keys():
		dic = {'word':w,'count':d[w]['tfidf']}
		dic.update(d[w])
		wordsArr.append(dic)
	wordsArr = sorted(wordsArr, key=lambda k: -k['count'])
	wordsArr = wordsArr[:howmany]
	
  	############################################# Old (NEW) WAY: look at stored model (works only for only ONE speaker)
# 	else:
# 		s=speakers[0]
# 		if howmany==0:
# 			thengs = s.ngramspeaker_set.order_by("-tfidf")
# 		else:
# 			thengs = s.ngramspeaker_set.order_by("-tfidf")[:howmany]
# 			
# 		for ngs in thengs:
# 	  		ng = ngs.ngram
# 	  		spkArray=[]
	  		
	  	##################################################### deprecated ? FETCH SIMILAR SPEAKERS
	#		similSpeakersArray = getSolrSimilarArray(s,similcount) # return sorted array of [score,sId,sName]
	  		####### OLD WAY : fetching all speakers
	#   		for ongs in ng.ngramspeaker_set.all():
	#   			if ongs!=ngs: # only OTHER speakers !
	# 	  			os = ongs.speaker
	# 	  			similspeakers[os.id] = os.name
	# 	  			spkArray.append({'id':os.id,'tfidf':ongs.tfidf,'tf':ongs.tf,'tn':ongs.tn})
	
	  		####### NEW WAY : fetch spkers based on solr-similarity
	#   		for similIdName in similSpeakersArray:
	#   			try:
	#   				ongs = NgramSpeaker.objects.get(speaker__id=int(similIdName[1]),ngram=ng)
	#   				spkArray.append({'id':similIdName[1],'tfidf':ongs.tfidf,'tf':ongs.tf,'tn':ongs.tn})
	#   			except:
	#   				donothing=1
	#   				#spkArray.append({'id':0,'tfidf':0,'tf':0,'tn':0})
	  			
	  			
# 	  		wordsArr.append({'word':ng.content,'speakers':spkArray,'count':ngs.tfidf,'tfidf':ngs.tfidf,'df':ng.df,'dn':ng.ngramspeaker_set.count(),'tf':ngs.tf,'tn':ngs.tn})
  		#############################################
  	
  	res={}
	res['words']=wordsArr
	res['speakers']=[]
	return res
###########################################################################









###########################################################################
# DEPRECATED, but useful to see raw queries
# TagCloud using Solr index (using haystack raw_query)
# def visMakeSolrTagCloud(e,param):
# 	count = param['count']
# 	speakerIds = param['who']
# 	facetField = param['what'] # like 'text' or 'content_c_auto'
# 	
# 	###### GOAL : to do something like :
# 	# FIRST SOLUTION : SEARCH ONLY SPEAKERID AND LOOK AT FACETS 	(on the Intervention Model)
# 	# (ie: repartition of other fields for one query)
# 	# /solr/select?q=speakerid:8&rows=0&facet=true&facet.limit=20&facet.field=content_c_auto
# 	# ie, get, for a speaker, the most used content_c_auto words
# 	#
# 	# SECOND SOLUTION : RAW_QUERY looking at tf-idf 				(on the Speaker Model)
# 	# /solr/select/?fq=django_ct:(reanalyseapp.speaker)&qt=tvrh&q=semble&fl=enqueteid&tv.fl=text&tv.all=true
# 	# p={'q':'semble','fq':'django_ct:(reanalyseapp.speaker)','qt':'tvrh','fl':'enqueteid','tv.fl':'text','tv.all':'true'}
# 	
# 	# /solr/select/?fq=django_ct:(reanalyseapp.speaker)&qt=tvrh&q=speakerid:69&fl=text&tv.fl=text&tv.all=true
# 	# p={'q':'speakerid:69','fq':'django_ct:(reanalyseapp.speaker)','qt':'tvrh','fl':'text','tv.fl':'text','tv.all':'true'}
# 	
# 	
# #	to test from ./manage.py shell
# # 	from haystack.query import SearchQuerySet
# # 	from reanalyse.reanalyseapp.models import *
# #	sqs = SearchQuerySet().raw_search(p['q'],**p)
# 
# 
# 	##################### RAW QUERY
# 	# looking at: https://github.com/toastdriven/django-haystack/blob/master/haystack/backends/solr_backend.py
# # 	p={}
# # 	p['q']='speakerid:'+str(speakerId)
# # 	p['facet']='true'
# # 	p['facet.limit']=str(count)
# # 	p['rows']=0
# # 	p['facet.field']='content_c_auto'
# # 	p['fl']='*'	# fields to return
# # 	p['fq']='django_ct:(reanalyseapp.intervention)' # restrict the set
# # 	sqs = SearchQuerySet().raw_search(p['q'],facets='content_c_auto',**p)
# 
# 	# ... trying before to do it raw (just above)
# 	# but it seems that there isn't the facet results in the json received by haystack
# 	# seems that we have to do it using haystack "official facets" ...
# 	
# 	##################### USING HAYSTACK FACETS
# 	sqs = SearchQuerySet().models(Speaker).filter(enqueteid=e.id)
# 	#sqs.query_facet('speakerid',str(speakerId)) DOES NOT WORK
# 	if len(speakerIds)==0:
# 		return {}
# 	else:
# 		spOr_query = None
# 		for sid in speakerIds:
# 			if spOr_query is None:
# 				spOr_query = SQ(speakerid=sid)
# 			else:
# 				spOr_query = spOr_query | SQ(speakerid=sid)
# 	sqs = sqs.filter(spOr_query).facet(facetField)
# 	
# 	res={}
# 	wordsArr=[]
# 	# then get facet counts results
# 	for tup in sqs.facet_counts()['fields'][facetField][:count]:
# 		nWords=tup[1]
# 		wordsArr.append({'word':tup[0],'count':nWords})
# 	res['words']=wordsArr
# 	return res
###########################################################################


















# DEPRECATED Tag Cloud from words models in DB
###########################################################################
# # JSON tagcloud from FORM-PARAMETERS, using words from TEI
# # todo: allow multi selection of speakers/texts in an array, using queries Q(speaker__id=i) | Q(speaker__id=j) ..
# def visMakeTeiTagCloudFrom(e,param):
# 	res={}
# 	N=int(param['count'])
# 	
# 	############################ WHERE : source (all? only one text?)
# 	try: 	# if texte_id is defined, search only in that text
# 		allTexts=False
# 		theT=Texte.objects.get(id=param['where'])
# 	except:	# else, search in all texts
# 		allTexts=True
# 	############################ WHO :
# 	try:
# 		allSpeakers=False
# 		theS=Speaker.objects.get(id=param['who'])
# 	except:
# 		allSpeakers=True
# 			
# 	# INIT : we will store min and max values
# 	cMin=9999
# 	cMax=0
# 	# list of words
# 	arr=[]
# 	################################
# 	if allSpeakers: # WHO : dont care about speakers, just take all speakers words
# 		################
# 		if param['how']=='tfidf': # WHAT : sort all words by maxtfidf - color = color(maxtfidf-speaker)
# 			# we want N words, so lets allow some words for each speaker
# 			N = 1 + int( N/e.speaker_set.count() );
# 			for s in e.speaker_set.all():
# 				spColor = getSpeakerColor(s)
# 				if allTexts:
# 					wESs = WordEntitySpeaker.objects.filter(wordentity__enquete=e,wordentity__code__codetype__name='Word',speaker=s).order_by('-tfidf')[:N]
# 				else:
# 					wESs = WordEntitySpeaker.objects.filter(wordentity__enquete=e,wordentity__code__codetype__name='Word',speaker=s,textes=theT).order_by('-tfidf')[:N]
# 				for wes in wESs:
# 					arr.append({'word':wes.wordentity.content,'count':wes.tfidf,'color':spColor,'tip':'TFIDF:'+'%.4f'%wes.tfidf})
# 					#'color':getSpeakerColor(s)
# 					cMin=min(wes.tfidf,cMin)
# 					cMax=max(wes.tfidf,cMax)
# 		################
# 		elif param['how']=='freq': # WHAT : just look over word-count
# 			if allTexts:
# 				wEs = WordEntity.objects.filter(enquete=e,code__codetype__name='Word').annotate(nE=Count('wordentityspeaker__word')).order_by('-nE')[:N]
# 			else:
# 				wEs = WordEntity.objects.filter(enquete=e,code__codetype__name='Word',textes=theT).annotate(nE=Count('wordentityspeaker__word')).order_by('-nE')[:N]
# 			for we in wEs:
# 				if allTexts:
# 					nWords = Word.objects.filter(enquete=e,wordentityspeaker__wordentity=we).count()					
# 				else:
# 					nWords = Word.objects.filter(enquete=e,sentence__intervention__texte=theT,wordentityspeaker__wordentity=we).count()
# 				# color is based on the speaker who represent the max tfidf for that wordentity
# 				try:
# 					spColor = getSpeakerColor( Speaker.objects.get(id=we.maxspeakerid) )
# 				except:
# 					spColor = getSpeakerColor( Speaker.objects.all()[0] )
# 				arr.append({'word':we.content,'count':nWords,'color':spColor,'tip':str(nWords)+' WordInstances'})
# 				cMin=min(nWords,cMin)
# 				cMax=max(nWords,cMax)
# 	################################
# 	else: # WHO : (if not 'all' then its the speaker id) we process only words from specific speaker (theS)
# 		spColor = getSpeakerColor(theS)
# 		################
# 		if param['how']=='tfidf': # WHAT : sort wEntitiesSpeakers by tfidf
# 			if allTexts:
# 				wESs = WordEntitySpeaker.objects.filter(wordentity__enquete=e,wordentity__code__codetype__name='Word',speaker=theS).order_by('-tfidf')[:N]
# 			else:
# 				wESs = WordEntitySpeaker.objects.filter(wordentity__enquete=e,wordentity__code__codetype__name='Word',speaker=theS,textes=theT).order_by('-tfidf')[:N]
# 			for wes in wESs:
# 				arr.append({'word':wes.wordentity.content,'count':wes.tfidf,'color':spColor,'tip':'TFIDF:'+'%.4f'%wes.tfidf})
# 				#'color':getSpeakerColor(s)
# 				cMin=min(wes.tfidf,cMin)
# 				cMax=max(wes.tfidf,cMax)
# 		################
# 		elif param['how']=='freq': # WHAT : sort wEntities by word count
# 			if allTexts:
# 				wEs = WordEntity.objects.filter(enquete=e,code__codetype__name='Word',wordentityspeaker__speaker=theS).annotate(nE=Count('wordentityspeaker__word')).order_by('-nE')[:N]
# 			else:
# 				wEs = WordEntity.objects.filter(enquete=e,code__codetype__name='Word',wordentityspeaker__speaker=theS,textes=theT).annotate(nE=Count('wordentityspeaker__word')).order_by('-nE')[:N]
# 			for we in wEs:
# 				if allTexts:
# 					nWords = Word.objects.filter(enquete=e, wordentityspeaker__wordentity=we, wordentityspeaker__speaker=theS).count()
# 				else:
# 					nWords = Word.objects.filter(enquete=e, sentence__intervention__texte=theT, wordentityspeaker__wordentity=we, wordentityspeaker__speaker=theS).count()
# 				arr.append({'word':we.content,'count':nWords,'color':spColor,'tip':str(nWords)+' WordInstances'})
# 				cMin=min(nWords,cMin)
# 				cMax=max(nWords,cMax)
# 	################################
# 	# RANDOM SORT ?
# 	#random.shuffle(arr)
# 	# in case of different speakers, sort by speakers
# 	if allSpeakers:
# 		arr = sorted(arr, key=lambda k: k['color']) 
# 	res['words']=arr
# 	res['min']=cMin
# 	res['max']=cMax
# 	return res
###########################################################################







# DEPRECATED ?
########################################################################### SIMPLE GRAPH VISUALIZATIONS
# def visMakeSpeakerWordsGraph(enquete,viz):
# 	outFilePath = settings.REANALYSEDOWNLOADPATH+"e" + str(enquete.id) + viz.name +".gexf"
# 	g=networkx.DiGraph()
# 	# Speaker Nodes
# 	for s in enquete.speaker_set.all():
# 		g.add_node('Speaker_'+str(s.id),{'label':s.name,'category':'Speaker','WordCount':s.wordentityspeaker_set.count(),'MaxTfIdfx100':0})
# 	# WordEntities Nodes & Links
# 	for we in enquete.wordentity_set.all():
# 		g.add_node('WordEntity_'+str(we.id),{'label':we.content,'category':'WordEntity','WordCount':0,'MaxTfIdfx100':'%.4f'%(100*we.maxtfidf)})
# 		for wes in we.wordentityspeaker_set.all():
# 			g.add_edge('Speaker_'+str(wes.speaker.id),'WordEntity_'+str(we.id),{'weight':wes.word_set.count()})
# 	networkx.readwrite.gexf.write_gexf(g,outFilePath)
# 	nN = str(g.number_of_nodes())
# 	nE = str(g.number_of_edges())
# 	viz.description='Speakers-Words graph: '+nN+' nodes & '+nE+' edges'
# 	viz.name = viz.name + '_graph_'+nN+'n_'+nE+'e'
# 	viz.locationpath = outFilePath
# 	viz.save()
###########################################################################





# DEPRECATED ?
###########################################################################
# # D3 JSON DICT FOR ENQUETE
# def visGetEnqueteWordsStatDict(enquete):
# 	res=dict()
# 	#nSpeakers = Speaker.objects.count()
# 	nSpeakers = 10
# 	
# 	# the grid for regroupment for TFIDFs
# 	nSteps = 40
# 	# get min and max of ALL TFIDF
# 	d = WordEntitySpeaker.objects.filter(speaker__enquete=enquete).aggregate(mi=Min('tfidf'),ma=Max('tfidf'))
# 	globalMinTfidf = d['mi']
# 	globalMaxTfidf = d['ma']
# 	outDict['ymin']=globalMinTfidf
# 	outDict['ymax']=globalMaxTfidf
# 	outDict['xstep']=nSpeakers
# 	outDict['ystep']=nSteps
# 	# We look at WordEntities that are in each given [nCommonSpeaker] Speakers 
# 	for nCommonSpeaker in range(nSpeakers):
# 		key = 'docs_'+str(nCommonSpeaker)
# 		# in each data['k'], we are going to store an array of [maxTFIDF,WordEntitySample]
# 		# initiate grid array
# 		steps = range(nSteps)
# 		# get WordEntities that have instances in [nCommonSpeaker] Speakers
# 		wordEnts = WordEntity.objects.annotate(num_speakers=Count('wordentityspeaker')).filter(num_speakers=nCommonSpeaker)
# 		for we in wordEnts:
# 			# for each WordEntity, get only the TFIDF of the WordEntitySpeaker that has the max TFIDF
# 			# regroup and store thoses WordEntities in packages
# 			# ( in a grid [globalMinTfidf,globalMaxTfidf] )
# 			
# 			# get step in which the WordEntity has to be
# 			theMaxTfidf = we.maxtfidf
# 			theMaxWes = WordEntitySpeaker.objects.get(enquete=enquete,id=we.maxspeakerid)
# 			st = int( (theMaxTfidf-globalMinTfidf) * (nSteps-1) / float(globalMaxTfidf-globalMinTfidf))
# 			# we store [maxTFIDF,WordEntitySample]
# 			steps[st] = {'tfidf':theMaxTfidf,'word':we.content}
# 		outDict[key] = steps
# 	
# 	# Total count of words
# #	totalWords=0
# #	for i in texte.intervention_set.all():
# #		for s in i.sentence_set.all():
# #			totalWords+=s.word_set.count()
# #	outDict['totalWords']=totalWords
# #	outDict['totalWordEntities']=len(wordEntities)
# 	
# #	values=[]
# #	texte.intervention_set
# #	for word in Word.objects.get(sentence=s):
# #		wordentity=word.wordentity
# #		nocc=wordentity.word_set.count
# 	
# 	#outDict['topusedwords']=1
# 	#outDict['length']=1
# 	#outDict['differentwords']=1
# 
# 	return res
###########################################################################




# DEPRECATED ?
###########################################################################
# D3 JSON DICT FOR ENQUETE
# return size of speaker interventions (word count) for all TEI textes
# used, in 'SpeakersByText' viz
# def visGetEnqueteTextsStatDict(enquete):
# 	res=dict()
# 	arrSpeakers=[] 	# list of speakers
# 	arrTexts=[]		# list of texts
# 	arrData=[]
# 	maxWords=0
# 	teiTexts = enquete.texte_set.filter(doctype='TEI')
# 	for t in teiTexts:
# 		arrTexts.append( {'name':t.name,'id':t.id} )
# 	for s in enquete.speaker_set.filter(textes__doctype='TEI').distinct():
# 		arrSpeakers.append( {'name':s.name,'id':s.id} )
# 		spData=[] # words for each text
# 		for i,t in enumerate(teiTexts):
# 			count=Word.objects.filter(speaker=s,sentence__intervention__texte=t).count()
# 			spData.append( {'x':i,'y':count,'id':s.id} )
# 			if count>maxWords:
# 				maxWords=count
# 		arrData.append( spData )
# 	res['texts']=arrTexts
# 	res['maxWords']=maxWords
# 	res['speakers']=arrSpeakers
# 	res['data']=arrData
# 	return res
###########################################################################





# DEPRECATED ?
####################################################################
# # JSON DICT FOR a TEXTE
# def visGetStatDict(texte):
# 	# number ofwords we want for each speaker
# 	N=30
# 	res=dict()
# 	speakerarray=[]
# 	wordarray=[]
# 	for s in texte.speaker_set.all():
# 		# stats for each speaker
# 		d=dict()
# 		d['id'] = s.id
# 		d['name'] = s.name
# 		d['wordentitycount'] = texte.wordentityspeaker_set.filter(speaker=s).count()
# 		d['wordcount'] = Word.objects.filter(enquete=texte.enquete,speaker=s,sentence__intervention__texte=texte).count()
# 		speakerarray.append(d)
# 		# all words
# 		for wes in texte.wordentityspeaker_set.filter(speaker=s).order_by('tfidf')[:N]:
# 			wordarray.append({'name':s.name,'tfidf':'%.5f'%wes.tfidf,'word':wes.wordentity.content })
# 		#for wes in texte.wordentityspeaker_set.filter(speaker=s).order_by('-tfidf')[:N]:
# 		#	wordarray.append({'name':s.name,'tfidf':'%.5f'%wes.tfidf,'word':wes.wordentity.content })
# 	res['speakers']=speakerarray
# 	res['words']=wordarray	
# 	return res
###########################################################################







# ###########################################################################
# # SAVED from esShow-view : could be useful for a future visualisation
# def makeSpeakerWordsDict():
# 	stats={}
# 	# SPEAKER WORDS
# 	stats['diffcount']=speaker.wordentityspeaker_set.count()
# 	stats['count']=speaker.word_set.count()
# 	stats['words']=[]
# 	N=17
# 	mins=speaker.wordentityspeaker_set.all().order_by('tfidf')[:N]
# 	maxs=speaker.wordentityspeaker_set.all().order_by('-tfidf')[:N]
# 	for i,wes in enumerate(mins):
# 		a={'id':wes.wordentity.id,'word':wes.wordentity.content,'tfidf':'%.4f'%wes.tfidf}
# 		b={'id':maxs[i].wordentity.id,'word':maxs[i].wordentity.content,'tfidf':'%.4f'%maxs[i].tfidf}
# 		stats['words'].append([a,b])
# 	return stats
# ###########################################################################
# # SAVED from esShow-view : could be useful for a future visualisation
# def makeSpeakerAttributesDict():
# 	# PEOPLE ATTRIBUTES
# 	speakeratt=[]
# 	maxAttsPerRow=8
# 	nAttsPerRow=-1
# 	countAttsPerRow=999
# 	for u in speaker.attributes.all():
# 		countAttsPerRow += 1
# 		if countAttsPerRow>maxAttsPerRow:
# 			countAttsPerRow = 0
# 			nAttsPerRow += 1
# 			theAtt=dict()
# 			theAtt['type']=[]
# 			theAtt['value']=[]
# 			speakeratt.append(theAtt)
# 		speakeratt[nAttsPerRow]['type'].append(u.attributetype.name)
# 		speakeratt[nAttsPerRow]['value'].append( {'name':u.name,'description':u.description } )
# ###########################################################################












