# -*- coding: utf-8 -*-
###########################################################################
import settings
import logging
import os,re

from reanalyse.reanalyseapp.models import *
from reanalyse.reanalyseapp.utils import *

# for enquete permission
from django.contrib.auth.models import Group,Permission
from django.contrib.contenttypes.models import ContentType

from django.core import serializers
#from xml.etree.ElementTree import ElementTree
from lxml import etree

# converting parsing rtf
#from pyth.plugins.rtf15.reader import Rtf15Reader
#from pyth.plugins.plaintext.writer import PlaintextWriter
#from pyth.plugins.xhtml.writer import XHTMLWriter

# to launch commandline apps (unrtf)
from subprocess import PIPE, Popen


###########################################################################







###########################################################################
def exportEnquetesAsXML():
	filePath = settings.REANALYSEUPLOADPATH+"export_enquetes.xml"
	XMLSerializer = serializers.get_serializer("xml")
	xml_serializer = XMLSerializer()
	fileOut = open(filePath, "w")
	xml_serializer.serialize(Enquete.objects.all(), stream=fileOut)
	fileOut.close()
	logging.info("exporting all Enquetes to XML:"+filePath)
###########################################################################




###########################################################################
def updateDictWithMeta(dic,root,name,xmlpath):
	vals=[]
#	try:
	for elm in root.findall(xmlpath):
		vals.append(removeSpacesReturns(elm.text))
	dic.update({name:vals})
#	except:
#		dic.update({name:['error']})
	return dic
###########################################################################
def importEnqueteDDI2(inXmlPath):
	tree = etree.parse(inXmlPath)
	root = tree.getroot()
	
	#nodes = root.xpath('ns:docDscr/ns:citation/ns:titlStmt',namespaces={'XMLDDINMS':'http://www.icpsr.umich.edu/DDI'})
	
	# NB: we do removeAllSpacesReturns() to clean text value of xml tags
	
	# GENERAL META
	name = root.findall(XMLDDINMS+'stdyDscr/'+XMLDDINMS+'citation/'+XMLDDINMS+'titlStmt/'+XMLDDINMS+'titl')[0].text
	descr = root.findall(XMLDDINMS+'stdyDscr/'+XMLDDINMS+'stdyInfo/'+XMLDDINMS+'abstract')[0].text
	study_ddi_id = root.findall(XMLDDINMS+'stdyDscr/'+XMLDDINMS+'citation/'+XMLDDINMS+'titlStmt/'+XMLDDINMS+'IDNo')[0].text
	
	study_ddi_id = removeAllSpacesReturns(study_ddi_id)
	
	name = removeSpacesReturns(name)
	descr = makeHtmlFromText(descr)
	shortdescr = descr.split('</p>')[0]+'</p>'
	
	# ALL OTHER META
	allmeta={}
	allmeta['description'] = descr
	
	# Study Descr
	updateDictWithMeta(allmeta,root,'docTitle',XMLDDINMS+'docDscr/'+XMLDDINMS+'citation/'+XMLDDINMS+'titlStmt/'+XMLDDINMS+'titl')
	updateDictWithMeta(allmeta,root,'docAuthEntry',XMLDDINMS+'docDscr/'+XMLDDINMS+'citation/'+XMLDDINMS+'rspStmt/'+XMLDDINMS+'AuthEnty')
	updateDictWithMeta(allmeta,root,'doccopyright',XMLDDINMS+'docDscr/'+XMLDDINMS+'citation/'+XMLDDINMS+'prodStmt/'+XMLDDINMS+'copyright')
	#updateDictWithMeta(allmeta,root,'docUsingSoftware',XMLDDINMS+'docDscr/'+XMLDDINMS+'citation/'+XMLDDINMS+'prodStmt/'+XMLDDINMS+'software')
	
	updateDictWithMeta(allmeta,root,'cAuthEnty',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'citation/'+XMLDDINMS+'rspStmt/'+XMLDDINMS+'AuthEnty')
	updateDictWithMeta(allmeta,root,'cfundAg',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'citation/'+XMLDDINMS+'prodStmt/'+XMLDDINMS+'fundAg')
	updateDictWithMeta(allmeta,root,'cgrantNo',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'citation/'+XMLDDINMS+'prodStmt/'+XMLDDINMS+'grantNo')
	updateDictWithMeta(allmeta,root,'cdistrbtr',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'citation/'+XMLDDINMS+'distStmt/'+XMLDDINMS+'distrbtr')
	
	# Study Info
	updateDictWithMeta(allmeta,root,'snation',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'stdyInfo/'+XMLDDINMS+'sumDscr/'+XMLDDINMS+'nation')
	updateDictWithMeta(allmeta,root,'sgeogCover',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'stdyInfo/'+XMLDDINMS+'sumDscr/'+XMLDDINMS+'geogCover')
	updateDictWithMeta(allmeta,root,'sanlyUnit',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'stdyInfo/'+XMLDDINMS+'sumDscr/'+XMLDDINMS+'anlyUnit')
	
	updateDictWithMeta(allmeta,root,'mtimeMeth',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'method/'+XMLDDINMS+'dataColl/'+XMLDDINMS+'timeMeth')
	updateDictWithMeta(allmeta,root,'msampProc',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'method/'+XMLDDINMS+'dataColl/'+XMLDDINMS+'sampProc')		
	updateDictWithMeta(allmeta,root,'mcollMode',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'method/'+XMLDDINMS+'dataColl/'+XMLDDINMS+'collMode')
	updateDictWithMeta(allmeta,root,'mcollSitu',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'method/'+XMLDDINMS+'dataColl/'+XMLDDINMS+'collSitu')
	
	# Related Publications
	relPubs = []
	for relPubNode in root.findall(XMLDDINMS+'stdyDscr/'+XMLDDINMS+'othrStdyMat/'+XMLDDINMS+'relPubl/'+XMLDDINMS+'citation'):
		title = relPubNode.findall(XMLDDINMS+'titlStmt/'+XMLDDINMS+'titl')[0].text
		relPubs.append(removeSpacesReturns(title))
	allmeta['relPubl']=relPubs
	
	
	logging.info("creating Enquete:"+name)
	
	# nb: for the moment ese is not included in study, that's bad !
	eseXmlPath = settings.REANALYSEESE_FILES + study_ddi_id +".xml"
	ese = EnqueteSurEnquete(localxml=eseXmlPath)
	ese.buildMe()
	ese.save()
	
	# status=1 means object exists but not completely loaded yet
	newEnquete = Enquete(name=name,ddi_id=study_ddi_id,ese=ese,description=shortdescr,status='1')
	newEnquete.metadata = simplejson.dumps(allmeta,indent=4,ensure_ascii=False)
	newEnquete.save()
	
	# create permission for this enquete
	content_type,isnew = ContentType.objects.get_or_create(app_label='reanalyseapp', model='Enquete')
	p,isnew = Permission.objects.get_or_create(codename='can_explore_'+str(newEnquete.id),name='EXPLORE enquete '+str(newEnquete.id),content_type=content_type)

	
	###################################################################### IMPORT DOCUMENTS REFERENCED IN XML
	# documents paths are relative to the ddi.xml, let's get that path
	enquetePath = '/'.join( inXmlPath.split('/')[:-1] )
	
	#extDocuments = root.xpath('otherStdyMat/relMat')
	extDocuments = root.findall(XMLDDINMS+'stdyDscr/'+XMLDDINMS+'othrStdyMat/'+XMLDDINMS+'relMat')
	for extDoc in extDocuments:
		name = extDoc.findall(XMLDDINMS+'citation/'+XMLDDINMS+'titlStmt/'+XMLDDINMS+'titl')[0].text

		#### File info
		holdings = extDoc.findall(XMLDDINMS+'citation/'+XMLDDINMS+'holdings')[0]
		location = holdings.attrib['location']
		cat = holdings.attrib['type']
		typ = holdings.attrib['mimetype'].upper()

		#### Meta tag added for testing
		try: # to support old ddi (soon deprecated)
			meta = extDoc.findall(XMLDDINMS+'citation/'+XMLDDINMS+'meta')[0]
			m_location = meta.attrib['location']
			m_date = datetime.strptime(meta.attrib['date'], "%Y-%m-%d") #"2011-12-31"
		except:
			m_location = "Paris"
			m_date = datetime.datetime.today()
		
		location = enquetePath + '/' + location
		logging.info("creating document from path:"+name+" "+location)
		# status=1 means object exists but not completely loaded yet
		newDocument = Texte(enquete=newEnquete,name=name,locationpath=location,date=m_date,location=m_location,status='1')
		# get file size
		try:
			fsiz = int(os.path.getsize(location)/1024)
			newDocument.filesize = fsiz
			newDocument.save()
			# object created, now we parse it if needed
			# at the moment only looking at extension to guess type
			ext = location.split(".")[-1].upper()
			newDocument.doctype = ext
			newDocument.doccat = cat
			if ext=='PDF':
				# todo: parse it to be able to index it ?
				newDocument.description="nothing was done, actually, only the pdf location path was saved"
				newDocument.status='0'
				newDocument.save()
			elif ext=='CSV':
				# NB: CSV is "\t" separated file !
				# parse CSV and create/update Codes and relationships
				newDocument.description="parsed tab separated table : speakers are added/updated with their attributes/attributeTypes"
				parseDocumentCSV(newDocument)
			elif ext=='XML':
				if typ=='TEI':
					newDocument.description="xml doc was parsed into Interventions, Sentences, Words…"
					newDocument.status='5' # Waiting to be parsed...
					newDocument.doctype='TEI'
					newDocument.save()
					# assume this is a TEI XML document
					parseDocumentTEI(newDocument)
	# 			elif typ=='CAQDAS':
	# 				newDocument.description="xml atlasti project was parsed, then all referenced rtf file was converted in txt and codes are stored as Quotations with their position (offset) in the text"
	# 				newDocument.doctype='ATL'
	# 				newDocument.save()
	# 				parseDocumentAtlasTi(newDocument)
			elif ext=='RTF':
				newDocument.description="rtf content was converted to html"
				# store content (no codes) useful for indexing (better than PDF)
				parseDocumentRTF(newDocument)
		except:
			logging.info("error loading document node:"+name+":"+location)
			newDocument.status='-1'
			newDocument.save()
	
	# set speakers colors
	#randomizeSpeakersColors(newEnquete)
	setSpeakerColorsFromType(newEnquete)
	
	# even if documents are badly loaded, import is finished
	newEnquete.status='0'
	newEnquete.save()
	return newEnquete
###########################################################################
def parseDocumentRTF(doc):
	try:
		theDocContentHtml = Popen(['unrtf', doc.locationpath], stdout=PIPE).communicate()[0]
		doc.contenthtml = theDocContentHtml
		doc.contenttxt = convertUnrtfHtmlToTxt(theDocContentHtml)
		doc.status="0"
	except:
		doc.contenthtml = "Problem parsing RTF Document"
		doc.contenttxt = "Problem parsing RTF Document"
		doc.status="-1"
	doc.save()
###########################################################################
def parseDocumentCSV(doc):
	# supposing header where first column is id
	# id_participant = PEOPLE
	# DEPRECATED (id_type = GROUP)
	# other = ATTRIBUTE
	e=doc.enquete
	
	p = parseCsvFile(doc.locationpath)
	header = p['header']
	content = p['content']
	
	######################### now, create objects (only if csv is Table with "*id")
	if "*id" in p['header']:
		newSpeaker=None
		
		################## COLUMNS >3 : ATTRIBUTES CATEGORIES !
		attributetypes=[]
		for catval in header[3:]:
			if catval.startswith("_") or catval.startswith("*"):
				publicy = '0'
			else:
				publicy = '1'
			newAttType,isnew = AttributeType.objects.get_or_create(enquete=e,publicy=publicy,name=catval)
			attributetypes.append(newAttType)
			
		for line in content: 
			################### COLUMN 1		*id
			################### COLUMN 2		*type 				(only 'speaker' is displayed in sBrowse)
			################### COLUMN 3		*pseudo (>name)
	
			################### OTHERS			_anyattributes 		(not displayed in sBrowse)
			################### OTHERS			any attributes		(displayed in sBrowse)
			
			maintype=header[0]
			attval=line[maintype]
			
			# TRASH: newCodeType,isnew = CodeType.objects.get_or_create(enquete=e,name='speaker')
			
			pid = line['*id']
			try:
				pty = SPEAKER_TYPE_CSV_DICT[ line['*type'] ]
			except:
				pty = 'OTH'
			
			pna = line['*pseudo']
			
			if pna=="":
				pna="Speaker"
			
			newSpeaker,isnew = Speaker.objects.get_or_create(enquete=e,ddi_id=pid,ddi_type=pty,name=pna)
			
			for attype in attributetypes:
				attval=line[attype.name]
				if attval=='':
					attval='[NC]'
				newAttribute,isnew = Attribute.objects.get_or_create(enquete=e,attributetype=attype,name=attval)
				newSpeaker.attributes.add(newAttribute)
			newSpeaker.save()
			
	doc.status='0'
	doc.save()
###########################################################################
# todo: each time we create object PEOPLE or GROUP
# test if already there (look at name) and update attributes
# do not creates clones (for example if a Participant is defined at different places…)
# DONE using "objects.get_or_create"
###########################################################################	
def parseDocumentTEI(doc):
	e = doc.enquete
	
	try:
		# keep original xml in database
		inDoc = open(doc.locationpath,'r')
		# NB: HIAT syntax understand "/" as incident "repair" ! dirty workaround here ! (will disapear with other TEI editing technics)
		# todo: do something
		corrected = correctTeiPunctuation(''.join(inDoc.readlines()))
		inDoc.close()
	 	doc.contentxml = corrected
	 	outDoc = open(doc.locationpath,'w')
	 	outDoc.write(corrected)
		outDoc.close()
		doc.save()
	except:
		# file does not exist ?
		doc.status='-1'
		doc.save()
		
	# you may want to get speakers-list here already (?)
# 	tree = etree.parse(doc.locationpath)
# 	root = tree.getroot()
# 
# 	theCodeType,isnew = CodeType.objects.get_or_create(enquete=e,name='speaker')
# 	persons = root.findall(XMLTEINMS+'teiHeader/'+XMLTEINMS+'profileDesc/'+XMLTEINMS+'particDesc/'+XMLTEINMS+'person')
# 	for p in persons:
# 		name=p.findall(XMLTEINMS+'persName/'+XMLTEINMS+'abbr')[0].text
# 		newSpeaker,isnew = Speaker.objects.get_or_create(enquete=e,name=name,codetype=theCodeType)
# 		newSpeaker.textes.add(doc)
# 		newSpeaker.save()
	

###########################################################################













###########################################################################
# DEPRECATED NOW (we only use XML TEI)
# def parseDocumentAtlasTi(atlasdoc):
# 	# creates Documents referenced in the Atlas.ti.xml project file
# 	# creates all Speaker / Codes / Quotations
# 	e = atlasdoc.enquete
# 	
# 	tree = etree.parse(atlasdoc.locationpath)
# 	root = tree.getroot()
# 	doclocs = root.xpath('dataSources/dataSource')
# 	docs = root.xpath('primDocs/primDoc')
# 	codes = root.xpath('codes/code')
# 	families = root.xpath('families/codeFamilies/codeFamily')
# 	links = root.xpath('links/objectSegmentLinks/codings/iLink')
# 	
# 	# creates dictionnary linking id of doc to doc file path
# 	theDocs=dict()
# 	for doc in doclocs:
# 		theDocs[doc.attrib['id']] = doc.attrib['loc']
# 	# creates dictionnary linking id of code to codefamily name
# 	theCodeFamilies=dict()
# 	for fam in families:
# 		famName = fam.attrib['name']
# 		for c in fam.xpath('item'):
# 			codeId = c.attrib['id']
# 			theCodeFamilies[codeId]=famName
# 	# creates dictionnary linking [quotationId]>codeName & [quotationId]>familyName
# 	theCodes=dict()
# 	theFamilies=dict()
# 	for link in links:
# 		theQuotationId = link.attrib['qRef']
# 		theCodeId = link.attrib['obj']
# 		code = root.xpath('codes/code[@id="'+theCodeId+'"]')[0]
# 		codeName = code.attrib["name"]
# 		theCodes[theQuotationId]=codeName
# 		theFamilies[theQuotationId]=theCodeFamilies[theCodeId]
# 		#print "relation :",theQuotationId,codeName
# 	
# 	# loop for each text found in XML
# 	for doc in docs :
# 		docName = doc.attrib['name'] 
# 		docLoc = theDocs[doc.attrib['loc']]
# 		# we suppose it is already in the upload path
# 		folderPath = '/'.join( atlasdoc.locationpath.split('/')[:-1] )
# 		theDocPath = folderPath + '/' + docLoc
# 		# create object, status=1 means "loading"
# 		newDoc=Texte(status='1',name=docName,enquete=e,locationpath=theDocPath,doctype='CTX')
# 		newDoc.description='convert to html+txt and code'
# 		# get file size
# 		newDoc.filesize=int(os.path.getsize(theDocPath)/1024)
# 		newDoc.save()
# 		theDocContent=""
# 		dstatus='1'
# 		#try:
# 		logging.info("Creating document:"+theDocPath)
# 		if os.path.isfile(theDocPath): # check if exist
# 			# we fetch content of rtf file and put it in database
# 			if docLoc.endswith('.rtf'):
# 				##### A ##### old method with "Pyth" python lib
# 				"""
# 				rtfdoc = Rtf15Reader.read(open(theDocPath, "rb"))
# 				fileOutTxt=open(theDocPathSinExt+".txt",'w')
# 				fileOutHtml=open(theDocPathSinExt+".htm",'w')
# 				PlaintextWriter.write(rtfdoc, target=fileOutTxt)
# 				XHTMLWriter.write(rtfdoc, target=fileOutHtml, pretty=True)
# 				fileOutTxt.close()
# 				#fileOutHtml.close()
# 			# Reading simple txt file
# 			inDoc = open(theDocPathSinExt+'.txt','r')
# 			theDocContent = ''.join(inDoc.readlines())
# 			inDoc.close()
# 				"""
# 				##### B ##### using command line app
# 				theDocContent = Popen(['unrtf', theDocPath], stdout=PIPE).communicate()[0]
# 				theDocContent = convertUnrtfHtmlToTxt( theDocContent )
# 				
# 			if len(theDocContent)>0:
# 				dstatus='0'
# 			else:
# 				dstatus='2'
# 		else: # problem, file does not exist
# 			theDocContent = "File "+theDocPath+" does not exist"
# 			dstatus='-1'
# 		#except:
# 			#theDocContent = "Problem trying to parse "+theDocPath
# 		newDoc.content=theDocContent
# 		newDoc.status=dstatus
# 		newDoc.save()
# 		
# 		# create all quotations
# 		quotes = doc.xpath('quotations/q')
# 		for q in quotes:
# 			tid = q.attrib['id'] 
# 			tloc = q.attrib['loc'] # "1 @ 5, 42 @ 5!"
# 			try:
# 				tname = theCodes[tid]
# 			except:
# 				tname = "unspecifiedCodeInXml"
# 			try:
# 				tfam = theFamilies[tid]
# 			except:
# 				tfam = "unspecifiedCodeFamilyInAtlasXml"
# 			theCode=None
# 			TheCodeType,isnew = CodeType.objects.get_or_create(enquete=e,name=tfam)
# 			if tfam=='speaker':
# 				# get Speaker to associate quote to him
# 				theCode,isnew = Speaker.objects.get_or_create(enquete=e,name=tname,codetype=TheCodeType)
# 			else:
# 				# get AttributeType
# 				#theAttType = AttributeType.objects.get_or_create(enquete=e,name=tfam)
# 				# get Attribute to associate quote to it
# 				#theAttrib = Attribute.objects.get_or_create(enquete=e,name=codeName, category=codeCat)
# 				theCode,isnew = Code.objects.get_or_create(enquete=e,name=tname,codetype=TheCodeType)
# 				# link that code to this text (manyToMany relationship)
# 			# associate the current text with that Code/Speaker
# 			theCode.textes.add(newDoc)
# 			theCode.save()
# 			
# 			# now, create Quotation, as an instance that Code/Speaker
# 			sp=re.compile('[,!]')
# 			dec=re.split(sp,tloc)
# 			ss=dec[0].split('@')
# 			ss.reverse()
# 			ee=dec[1].split('@')
# 			ee.reverse()
# 			offs=','.join( ss )
# 			offe=','.join( ee )
# 			offs = re.sub(' ','',offs)
# 			offe = re.sub(' ','',offe)
# 			newQuot = Quotation(code=theCode,texte=newDoc,offs=offs,offe=offe)
# 			newQuot.save()
# 	logging.info("Importing AtlasTiXML Completed")
# 	atlasdoc.status='0'
# 	atlasdoc.save()
###########################################################################












