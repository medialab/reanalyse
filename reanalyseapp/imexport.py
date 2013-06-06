# -*- coding: utf-8 -*-
###########################################################################
import settings
import os,re

# for time measurement
from time import time
from datetime import timedelta

# for ese json
import simplejson

# csv.Dicteader
import csv

from reanalyseapp.models import *
from reanalyseapp.utils import *
from reanalyseapp.visualization import *

# for enquete permission
from django.contrib.auth.models import Group,Permission
from django.contrib.contenttypes.models import ContentType

from django.core import serializers

from xml.etree.ElementTree import ElementTree
from lxml import etree

# converting parsing rtf
#from pyth.plugins.rtf15.reader import Rtf15Reader
#from pyth.plugins.plaintext.writer import PlaintextWriter
#from pyth.plugins.xhtml.writer import XHTMLWriter

# to launch commandline apps (unrtf)
from subprocess import PIPE, Popen

from haystack.management.commands import update_index


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
def doFiestaToEnquete(e):
    logger.info("["+str(e.id)+"] enquete object made. now parsing docs, making viz, etc...")
    
    e.status='1'
    e.statuscomplete=0
    e.save()
    
    makeViz(e,'Overview')        # for left-menu-facets
    #
    #     Important NB:
    #    this  experimental 'Overview' viz, is aimed to be used as a left facet for different views
    #    note that the viz total count will increase by 1 (logical :)
    #    ... so that it may look like the vBrowse list is missing one :)
    #    ... we need to -1 manually in the displayed counts within the templates (cf tags.py)
    
    makeViz(e,'Attributes')        # with all speakers (since they should be defined in meta_speakers.csv table)
    
    ####### PARSE TEI and UPDATE INDEX (and save statuscomplete to know loading status)
    # we look at '5'='Waiting' TEI Documents...
    docsTotal = e.texte_set.filter(doctype='TEI',status='5').count()
    docsCur = 0
    for t in e.texte_set.filter(doctype='TEI',status='5').order_by('id'):
        if e.status != '1': # if not "loading", break
            logger.info("["+str(e.id)+"] EXCEPT enquete no more loading : breaking !")
            break
        t_start = time()
        # there is no try/except in the parseXml() function
        try:
            t.parseXml()
        except:
            t.status='-1'
            t.save()
            logger.info("["+str(e.id)+"] EXCEPT parsing texte: "+str(t.id))
        t_end = time()
        s = t_end-t_start
        m = s // 60
        diffstr = str(m)+" min "+str(int(s-60*m))+" s"
        logger.info("["+str(e.id)+"] parsing text "+str(t.id)+" took "+diffstr)
        if m>=5:
            logger.info("["+str(e.id)+"] EXCEPT please note that more than 5min is really bad !")
        docsCur+=1
        e.statuscomplete = int(docsCur*96/docsTotal)
        e.save()
        
        # let's make stream timeline viz for each text
        try:
            dontohing = 1
            makeViz(e,"TexteStreamTimeline",textes=[t])
        except:
            logger.info("["+str(e.id)+"] EXCEPT making streamtimeline viz: texteid="+str(t.id))
        
    logger.info("["+str(e.id)+"] all TEI files were sucessfully parsed")
    
    ####### UPDATE SOLR INDEX
    logger.info("["+str(e.id)+"] solr index updating ...")
    #update_index.Command().handle(verbosity=0)
    logger.info("["+str(e.id)+"] solr index updated")
        
    ####### UPDATE ALL TFIDF
    # ie fetch ngrams from solr and store them in django model (easier then to make viz using thoses objects rather than fetching ngrams everytime)
    logger.info("["+str(e.id)+"] fetching ngrams from solr ...")
    makeAllTfidf(e)
    logger.info("["+str(e.id)+"] fetching done")
    
    if e.speaker_set.count()>0:
        try:
            makeViz(e,'Cloud_SolrSpeakerTagCloud')
            e.statuscomplete = 97
            e.save()
            makeViz(e,'Graph_SpeakersSpeakers')
            e.statuscomplete = 98
            e.save()
            makeViz(e,'Graph_SpeakersWords')
            e.statuscomplete = 99
            e.save()
            makeViz(e,'Graph_SpeakersAttributes')
        except:
            logger.info("["+str(e.id)+"] EXCEPT making Cloud or Graphs")
        
    e.statuscomplete = 100        
    e.status='0'
    e.save()
    logger.info("["+str(e.id)+"] IMPORT PROCESS DONE SUCCESSFULLY !")
###########################################################################



def isMetaDocOK(folderPath,docPath):
   
    if os.path.exists(docPath):
       
        
        #mandatoryFields = ['*id','*name','*category','*description','*location','*date']
        logger.info("=========== PARSING META_DOCUMENTS.CSV TO CHECK IF A FILE IS MISSING IF TRUE IMPORT IS CANCELLED")
        ###### Parsing Documents
        doc = csv.DictReader(open(docPath),delimiter='\t')
        
        error = False
        error_dict = {}
                
        for counter, row in enumerate(doc):
            

            if row['\xef\xbb\xbf*id']!='*descr':
                

                file_location = '%s/%s'%( folderPath, str(row['*file']) )
                try:
                    open_file = open(file_location)
                    
                    
                    
                except IOError, e:
                    if(e.args[0] == 2):#no such file or directory
                        error = True
                        error_dict.update({file_location:e.args[1]})
                       # print({file_location:e.args[1]})
                       #print(file_location)
                        logger.info({file_location:e.args[1]})
                else:
                    logger.info(file_location+" exists")
                    print(file_location)
                
            
        if(error is True):
            return {'status':False, 'error_dict':error_dict}
        else:
            return True


###########################################################################
def importEnqueteUsingMeta(upPath,folderPath):
    logger.info( "import enquete from:'%s' folder:'%s'" % (upPath, folderPath))

    stdPath=folderPath+'_meta/meta_study.csv'
    docPath=folderPath+'_meta/meta_documents.csv'
    spkPath=folderPath+'_meta/meta_speakers.csv'
    codPath=folderPath+'_meta/meta_codes.csv'
    
    #Check if every files exists in meta_documents.csv
    check = isMetaDocOK(folderPath,docPath)
    
    """ if(check == True):
        pass
    else:
        logger.info("=========== PARSING META_DOCUMENT.CSV CANCELLED")
        return check
        """
    
    logger.info("=========== PARSING META_STUDY.CSV")
    ### Parsing Study metadatas (the only file mandatory!)
    

    std = csv.DictReader(open(stdPath),delimiter='\t',quotechar='"')
    headers = std.fieldnames
    allmeta={}
    allmeta['values']={}    # store metadata
    allmeta['labels']={}    # store labels (should become static.. for now (changing a lot), included in meta_study.csv)
    study_ddi_id     = 'no idno value found in meta_study.csv'
    study_name        = 'no titl value found in meta_study.csv'
    # we keep index 'i' to remember the order
    catcount=0
    count=0
    for row in std:
        
       
        if row['*field']!='*descr':
            try:
                field         = row['*field'].lower().replace(" ","").replace("*","")
                fieldcat     = row['*fieldcat'].lower().replace(" ","").replace("*","")
                #logger.info("found field: "+fieldcat+" / "+field)
            except:
                logger.info("EXCEPT no *field or *fieldcat column in meta_study.csv")
            try:
                allmeta['labels'][field]     = row['*fieldlabel']
                allmeta['labels'][fieldcat] = row['*fieldcatlabel']
            except:
                logger.info("EXCEPT no *fieldlabel or *fieldcatlabel column in meta_study.csv")
            value = row['*value']
            
            #### storing value for this line under fieldcat, keeping the order
            if fieldcat not in allmeta['values'].keys():
                allmeta['values'][fieldcat]={}
                allmeta['values'][fieldcat]['i'] = catcount
                catcount+=1
                count=0
            if field not in allmeta['values'][fieldcat].keys():
                allmeta['values'][fieldcat][field] = {}
                allmeta['values'][fieldcat][field]['i'] = count
                allmeta['values'][fieldcat][field]['value'] = [value]
                count+=1
            else:
                allmeta['values'][fieldcat][field]['value'] += [value]                
            
            if field=='idno':
                study_ddi_id = value
            if field=='titl':
                study_name = value

    ### create enquete object
    newEnquete = Enquete(name=study_name,uploadpath=upPath,locationpath=folderPath,ddi_id=study_ddi_id,status='1')
    newEnquete.metadata = simplejson.dumps(allmeta,indent=4,ensure_ascii=False)
    newEnquete.save()
    
    eidstr = "[#"+str(newEnquete.id)+"] " # for logger prefix
    logger.info("%s enquete '%s':%s created"  % ( eidstr, study_name, newEnquete.id ))
    ### create permission for this enquete
    content_type,isnew = ContentType.objects.get_or_create(app_label='reanalyseapp', model='Enquete')
    permname = 'EXPLORe_'+str(newEnquete.id)
    p,isnew = Permission.objects.get_or_create(codename='can_explore_'+str(newEnquete.id),name=permname,content_type=content_type)
    
    if os.path.exists(docPath):
        #mandatoryFields = ['*id','*name','*category','*description','*location','*date']
        logger.info(eidstr+"=========== PARSING META_DOCUMENTS.CSV")
        ###### Parsing Documents
        doc = csv.DictReader(open(docPath),delimiter='\t')
        
        logger.info(eidstr+" %s row found " % doc )

        for counter, row in enumerate(doc):
            #try:
            logger.info("%s fields : %s" % (eidstr, row ) ) 
            if row['\xef\xbb\xbf*id'] != '*descr':
                #try:
                file_location =     folderPath+row['*file']                        # if LINK > url , else REF > nothing
                file_extension =     file_location.split(".")[-1].upper()
                doc_name =             row['*name']
                doc_mimetype =         row['*mimetype'].lower().replace(" ","")
                doc_category1 =     row['*researchPhase'].lower().replace(" ","")
                doc_category2 =     row['*documentType'].lower().replace(" ","")
                doc_public =         True # ...could be based on categories...
                doc_description =     ''#row['*description']
                doc_location =         row['*location']
                try:
                    doc_location_geo =     row['*location_geo']
                except KeyError, e:
                    logger.info( "%s KeyError warning, location_geo field not found or invalid: %s" % (eidstr,e) )
                    doc_location_geo = ""

                # document date
                try:
                    doc_date = datetime.datetime.strptime(row['*date'], "%Y_%m_%d") #"31-12-12"
                except:
                    logger.info("%s line %s EXCEPT malformed or empty date : %s, supported format 'YYYY_MM_DD'" % ( eidstr, counter, row['*date']))
                    doc_date = datetime.datetime.today()


                
                ### very special for ese, don't create any texte() model, just parse ese.xml and fill enquete.ese with a json
                if doc_mimetype=='ese':
                    #try:
                    esedict = getEnqueteSurEnqueteJson(file_location,newEnquete)
                    newEnquete.ese = simplejson.dumps(esedict,indent=4,ensure_ascii=False)
                    newEnquete.save()
                    #except:
                        #logger.info(eidstr+"EXCEPT with ESE")
                        
                ### if cat(s) are listed in globalvars.py, create doc
                elif doc_category1 in DOC_CAT_1.keys() and doc_category2 in DOC_CAT_2.keys():
                    if doc_mimetype in DOCUMENT_MIMETYPES:
                        newDocument = Texte(enquete=newEnquete, name=doc_name, doccat1=doc_category1, doccat2=doc_category2, description=doc_description, locationpath=file_location, date=doc_date, location=doc_location, status='1', public=doc_public)
            

                        newDocument.doctype = doc_mimetype.upper()
                        if doc_mimetype in ['link','ref']:
                            newDocument.locationpath     = row['*file']
                            newDocument.filesize         = 0
                            newDocument.status            = '0'
                            newDocument.save()
                        else:
                            ### get file size
                            try:
                                newDocument.filesize = int(os.path.getsize(file_location)/1024)
                            except:
                                newDocument.filesize = -1
                                logger.info(eidstr+"EXCEPT file does not exist: "+doc_mimetype+" | "+doc_category1+" | "+doc_category2+" | "+file_location)
                            
                            if doc_mimetype=='tei':
                                newDocument.status    = '5' # 'waiting' status
                                newDocument.save()
                            elif doc_mimetype=='pdf' or doc_mimetype=='csv' or doc_mimetype=='img':
                                
                                newDocument.status    = '0'
                                newDocument.save()
                            elif doc_mimetype=='htm':
                                try:
                                    f = open(file_location,'r')
                                    v = f.read()
                                    f.close()
                                    enc = guess_encoding(v)
                                    newDocument.contenthtml = unicode(v,enc,"strict")
                                except:
                                    newDocument.contenthtml = 'error reading file'
                                    logger.info(eidstr+"EXCEPT error reading file: "+file_location)
                                newDocument.status='0'
                                newDocument.save()
                            else:
                                logger.info(eidstr+"EXCEPT unconsidered document: "+doc_mimetype+" | "+doc_category1+" | "+doc_category2)
    #                         elif file_extension=='RTF':
    #                              try:
    #                                 theDocContentHtml = Popen(['unrtf', doc.locationpath], stdout=PIPE).communicate()[0]
    #                                 doc.contenthtml = theDocContentHtml
    #                                 doc.contenttxt = convertUnrtfHtmlToTxt(theDocContentHtml)
    #                                 doc.status="0"
    #                             except:
    #                                 blabla
                    else:
                        logger.info(eidstr+"EXCEPT unconsidered or empty *mimetype: "+doc_mimetype)
                ### unknown cat
                else:
                    logger.warning( "%s at line : %s '*researchPhase':'%s' it is NOT in %s OR '*documentType':'%s' it is NOT in %s" % ( eidstr, counter, doc_category1, DOC_CAT_1.keys(), doc_category2, DOC_CAT_2.keys()  ))
                    break
            #except:
                #logger.info(eidstr+" EXCEPT on meta_document.csv line: "+row['*id'])
    else:
        logger.info(eidstr+"=========== PARSING: no doc meta found")
    
    if os.path.exists(spkPath):
        logger.info(eidstr+"=========== PARSING META_SPEAKERS.CSV")            
        ###### Parsing Speakers
        spk = csv.DictReader(open(spkPath),delimiter='\t',quotechar='"')
        headers = spk.fieldnames
        mandatories = ["*pseudo","*id","*type"]
        attributetypes=[]
        for catval in headers:
            if catval not in mandatories: # we create only "un-mandatory" attributetypes, since mandatories are stored in speaker model structure
                if catval.startswith("_") or catval.startswith("*"):
                    publicy = '0'
                else:
                    publicy = '1'
                newAttType,isnew = AttributeType.objects.get_or_create(enquete=newEnquete,publicy=publicy,name=catval)
                attributetypes.append(newAttType)
        for row in spk:
            #try:
            if row['*id']!='*descr':
                spk_id =     row['*id']
                spk_type =     SPEAKER_TYPE_CSV_DICT.get(row['*type'],'OTH')
                spk_name =     row['*pseudo']
                newSpeaker,isnew = Speaker.objects.get_or_create(enquete=newEnquete,ddi_id=spk_id,ddi_type=spk_type,name=spk_name)
                newSpeaker.public = (spk_type=='SPK' or spk_type=='PRO')
                for attype in attributetypes:
                    attval=row[attype.name]
                    if attval=='':
                        attval='[NC]'
                    newAttribute,isnew = Attribute.objects.get_or_create(enquete=newEnquete,attributetype=attype,name=attval)
                    newSpeaker.attributes.add(newAttribute)
                newSpeaker.save()
            #except:
            #    logger.info(eidstr+" EXCEPT on meta_speakers.csv line: "+row['*id'])
        setSpeakerColorsFromType(newEnquete)
    else:
        logger.info(eidstr+"=========== PARSING: no spk meta found")
    
    if os.path.exists(codPath):
        logger.info(eidstr+"=========== PARSING META_CODES.CSV")
        ###### Parsing Codes
        cod = csv.DictReader(open(codPath),delimiter='\t',quotechar='"')
        # to do later..
    else:
        logger.info(eidstr+"=========== PARSING: no cod meta found")
        
    newEnquete.status='0'
    newEnquete.save()
    return newEnquete
###########################################################################




###########################################################################
# return json with all data from ese
def getEnqueteSurEnqueteJson(eseXmlPath,e):
    eidstr = "["+str(e.id)+"] "
    logger.info(eidstr+"=========== PARSING ESE XML: "+eseXmlPath)
    res={}
    
    tree = etree.parse(eseXmlPath)
    root = tree.getroot()
    
    baseEseXmlFolder = '/'+'/'.join(eseXmlPath.split('/')[:-1])+'/'
    
    out = {}
    out['audiopaths'] = {}
    apacount = 0
    for lan in ['fr','en']:
        res = {}
        
        # Fetching report
        rep = root.findall('Report')[0]
        res['reportpath'] = baseEseXmlFolder + rep.find('file[@lang="'+lan+'"]').attrib['location']
        
        # Fetching chapters
        thechapters = []
        for chapter in root.findall('Chapters/Chapter'):
            chapt = {}
            chapt['name'] = chapter.find('./title[@lang="'+lan+'"]').text
            chapt['html'] = chapter.find('./text[@lang="'+lan+'"]').text
            thesubchapters = []
            for subChapter in chapter.findall('SubChapter'):
                #try:
                subchapt = {}
                aud = subChapter.find('audio[@lang="'+lan+'"]')
                subchapt['name']         = aud.attrib['name']
                subchapt['audiopath']     = aud.attrib['location']
                # as the mp3 files may be located
                # either (good) in the _ese folder
                # either in the REANALYSEESE_FILES folder
                # we need to check availability, mmh..
                patharchive = baseEseXmlFolder+subchapt['audiopath']
                if os.path.exists( patharchive ):
                    subchapt['audiopath'] = patharchive
                else:
                    pathserver = settings.REANALYSEESE_FILES+'/'+e.ddi_id+'/'+ subchapt['audiopath']
                    if os.path.exists( pathserver ):
                        subchapt['audiopath'] = pathserver
                    else:
                        logger.info("["+str(e.id)+"] EXCEPT no audio file: "+patharchive)
                        logger.info("["+str(e.id)+"] EXCEPT no audio file: "+pathserver)
                    
                # rather store an id referencing real path in out['audiopaths']
                out['audiopaths'][str(apacount)] = subchapt['audiopath']
                subchapt['audioid'] = str(apacount)
                apacount+=1
                thesubchapters.append(subchapt)
                #except:
                    #logger.info("["+str(e.id)+"] EXCEPT with subchapter")
            chapt['subchapters'] = thesubchapters
            thechapters.append(chapt)
        res['chapters'] = thechapters
        out[lan] = res
    return out
###########################################################################

























# nb: before, we used to parse DDI.xml file
# the following is DEPRECATED, because it's cleaner/easier to parse meta_*.csv files

###########################################################################
# def updateDictWithMeta(dic,root,name,xmlpath):
#     vals=[]
# #    try:
#     for elm in root.findall(xmlpath):
#         vals.append(removeSpacesReturns(elm.text))
#     dic.update({name:vals})
# #    except:
# #        dic.update({name:['error']})
#     return dic
# ###########################################################################
# # ddi.xml parser
# def importEnqueteDDI2(inXmlPath):
#     tree = etree.parse(inXmlPath)
#     root = tree.getroot()
#     
#     #nodes = root.xpath('ns:docDscr/ns:citation/ns:titlStmt',namespaces={'XMLDDINMS':'http://www.icpsr.umich.edu/DDI'})
#     
#     # NB: we do removeAllSpacesReturns() to clean text value in xml tags
#     
#     ######### GENERAL META
#     name = root.findall(XMLDDINMS+'stdyDscr/'+XMLDDINMS+'citation/'+XMLDDINMS+'titlStmt/'+XMLDDINMS+'titl')[0].text
#     descr = root.findall(XMLDDINMS+'stdyDscr/'+XMLDDINMS+'stdyInfo/'+XMLDDINMS+'abstract')[0].text
#     study_ddi_id = root.findall(XMLDDINMS+'stdyDscr/'+XMLDDINMS+'citation/'+XMLDDINMS+'titlStmt/'+XMLDDINMS+'IDNo')[0].text
#     
#     study_ddi_id = removeAllSpacesReturns(study_ddi_id)
#     
#     name = removeSpacesReturns(name)
#     descr = makeHtmlFromText(descr)
#     shortdescr = descr.split('</p>')[0]+'</p>'
#     
#     ######### ALL OTHER META
#     allmeta={}
#     allmeta['description'] = descr
#     
#     updateDictWithMeta(allmeta,root,'abstract',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'stdyInfo/'+XMLDDINMS+'abstract')
#     
#     ######### Study Descr
#     updateDictWithMeta(allmeta,root,'titl',XMLDDINMS+'docDscr/'+XMLDDINMS+'citation/'+XMLDDINMS+'titlStmt/'+XMLDDINMS+'titl')
#     updateDictWithMeta(allmeta,root,'AuthEnty',XMLDDINMS+'docDscr/'+XMLDDINMS+'citation/'+XMLDDINMS+'rspStmt/'+XMLDDINMS+'AuthEnty')
#     updateDictWithMeta(allmeta,root,'copyright',XMLDDINMS+'docDscr/'+XMLDDINMS+'citation/'+XMLDDINMS+'prodStmt/'+XMLDDINMS+'copyright')
#     #updateDictWithMeta(allmeta,root,'docUsingSoftware',XMLDDINMS+'docDscr/'+XMLDDINMS+'citation/'+XMLDDINMS+'prodStmt/'+XMLDDINMS+'software')
#     
#     #updateDictWithMeta(allmeta,root,'AuthEnty',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'citation/'+XMLDDINMS+'rspStmt/'+XMLDDINMS+'AuthEnty')
#     updateDictWithMeta(allmeta,root,'fundAg',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'citation/'+XMLDDINMS+'prodStmt/'+XMLDDINMS+'fundAg')
#     updateDictWithMeta(allmeta,root,'grantNo',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'citation/'+XMLDDINMS+'prodStmt/'+XMLDDINMS+'grantNo')
#     updateDictWithMeta(allmeta,root,'distrbtr',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'citation/'+XMLDDINMS+'distStmt/'+XMLDDINMS+'distrbtr')
#     
#     ######### Study Info
#     updateDictWithMeta(allmeta,root,'nation',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'stdyInfo/'+XMLDDINMS+'sumDscr/'+XMLDDINMS+'nation')
#     updateDictWithMeta(allmeta,root,'geogCover',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'stdyInfo/'+XMLDDINMS+'sumDscr/'+XMLDDINMS+'geogCover')
#     updateDictWithMeta(allmeta,root,'anlyUnit',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'stdyInfo/'+XMLDDINMS+'sumDscr/'+XMLDDINMS+'anlyUnit')
#     
#     updateDictWithMeta(allmeta,root,'timeMeth',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'method/'+XMLDDINMS+'dataColl/'+XMLDDINMS+'timeMeth')
#     updateDictWithMeta(allmeta,root,'sampProc',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'method/'+XMLDDINMS+'dataColl/'+XMLDDINMS+'sampProc')        
#     updateDictWithMeta(allmeta,root,'collMode',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'method/'+XMLDDINMS+'dataColl/'+XMLDDINMS+'collMode')
#     updateDictWithMeta(allmeta,root,'collSitu',XMLDDINMS+'stdyDscr/'+XMLDDINMS+'method/'+XMLDDINMS+'dataColl/'+XMLDDINMS+'collSitu')
#     
#     ######### Related Publications
#     # relPubl is deprecated, since we now use .csv to describe documents : related publications are listed in the meta_documents.csv and appear in the edBrowse view
# #     relPubs = []
# #     for relPubNode in root.findall(XMLDDINMS+'stdyDscr/'+XMLDDINMS+'othrStdyMat/'+XMLDDINMS+'relPubl/'+XMLDDINMS+'citation'):
# #         title = relPubNode.findall(XMLDDINMS+'titlStmt/'+XMLDDINMS+'titl')[0].text
# #         relPubs.append(removeSpacesReturns(title))
# #     allmeta['relPubl']=relPubs
#     
#     logger.info("creating Enquete:"+name)
#     
#     # status=1 means object exists but not completely loaded yet
#     newEnquete = Enquete(name=name,ddi_id=study_ddi_id,description=shortdescr,status='1')
#     newEnquete.metadata = simplejson.dumps(allmeta,indent=4,ensure_ascii=False)
#     newEnquete.save()
#     
#     # create permission for this enquete
#     content_type,isnew = ContentType.objects.get_or_create(app_label='reanalyseapp', model='Enquete')
#     permname = 'EXPLORE e_'+str(newEnquete.id) + ' '+newEnquete.name
#     p,isnew = Permission.objects.get_or_create(codename='can_explore_'+str(newEnquete.id),name=permname,content_type=content_type)
#     
#     # nb: for the moment ese is not included in study, that's bad !
#     eseXmlPath = settings.REANALYSEESE_FILES + study_ddi_id +".xml"
#     ese = EnqueteSurEnquete(localxml=eseXmlPath,enquete=newEnquete)
#     ese.buildMe()
#     ese.save()
#     
#     ###################################################################### IMPORT DOCUMENTS REFERENCED IN XML
#     # documents paths are relative to the ddi.xml, let's get that path
#     enquetePath = '/'.join( inXmlPath.split('/')[:-1] )
#     
#     #extDocuments = root.xpath('otherStdyMat/relMat')
#     extDocuments = root.findall(XMLDDINMS+'stdyDscr/'+XMLDDINMS+'othrStdyMat/'+XMLDDINMS+'relMat')
#     for extDoc in extDocuments:
#         name = extDoc.findall(XMLDDINMS+'citation/'+XMLDDINMS+'titlStmt/'+XMLDDINMS+'titl')[0].text
# 
#         #### File info
#         holdings = extDoc.findall(XMLDDINMS+'citation/'+XMLDDINMS+'holdings')[0]
#         location = holdings.attrib['location']
#         cat = holdings.attrib['type']
#         typ = holdings.attrib['mimetype'].upper()
# 
#         #### Meta tag added for testing
#         try: # to support old ddi (soon deprecated)
#             meta = extDoc.findall(XMLDDINMS+'citation/'+XMLDDINMS+'meta')[0]
#             m_location = meta.attrib['location']
#             m_date = datetime.strptime(meta.attrib['date'], "%Y-%m-%d") #"2011-12-31"
#         except:
#             m_location = "Paris"
#             m_date = datetime.datetime.today()
#         
#         location = enquetePath + '/' + location
#         logger.info("Document: "+name+" "+location)
#         # status=1 means object exists but not completely loaded yet
#         newDocument = Texte(enquete=newEnquete,name=name,locationpath=location,date=m_date,location=m_location,status='1')
#         # get file size
#         try:
#             fsiz = int(os.path.getsize(location)/1024)
#             newDocument.filesize = fsiz
#             newDocument.save()
#             # object created, now we parse it if needed
#             # at the moment only looking at extension to guess type
#             ext = location.split(".")[-1].upper()
#             newDocument.doctype = ext
#             newDocument.doccat = cat
#             if ext=='PDF':
#                 # todo: parse it to be able to index it ?
#                 newDocument.description="nothing was done, actually, only the pdf location path was saved"
#                 newDocument.status='0'
#                 newDocument.save()
#             elif ext=='CSV':
#                 # NB: CSV is "\t" separated file !
#                 # parse CSV and create/update Codes and relationships
#                 newDocument.description="parsed tab separated table : speakers are added/updated with their attributes/attributeTypes"
#                 parseDocumentCSV(newDocument)
#             elif ext=='XML':
#                 if typ=='TEI':
#                     newDocument.description="xml doc was parsed into Interventions, Sentences, Words…"
#                     newDocument.status='5' # Waiting to be parsed...
#                     newDocument.doctype='TEI'
#                     newDocument.save()
#                     # assume this is a TEI XML document
#                     parseDocumentTEI(newDocument)
#                 # completely deprecated, forget now about CQDAS
#     #             elif typ=='CAQDAS':
#     #                 newDocument.description="xml atlasti project was parsed, then all referenced rtf file was converted in txt and codes are stored as Quotations with their position (offset) in the text"
#     #                 newDocument.doctype='ATL'
#     #                 newDocument.save()
#     #                 parseDocumentAtlasTi(newDocument)
#             elif ext=='RTF':
#                 newDocument.description="rtf content was converted to html"
#                 # store content (no codes) useful for indexing (better than PDF)
#                 parseDocumentRTF(newDocument)
#         except:
#             logger.info("error loading document node:"+name+":"+location)
#             newDocument.status='-1'
#             newDocument.save()
#     
#     # set speakers colors
#     #randomizeSpeakersColors(newEnquete)
#     setSpeakerColorsFromType(newEnquete)
#     
#     # even if documents are badly loaded, import is finished
#     newEnquete.status='0'
#     newEnquete.save()
#     return newEnquete
###########################################################################
# def parseDocumentRTF(doc):
#     try:
#         theDocContentHtml = Popen(['unrtf', doc.locationpath], stdout=PIPE).communicate()[0]
#         doc.contenthtml = theDocContentHtml
#         doc.contenttxt = convertUnrtfHtmlToTxt(theDocContentHtml)
#         doc.status="0"
#     except:
#         doc.contenthtml = "Problem parsing RTF Document"
#         doc.contenttxt = "Problem parsing RTF Document"
#         doc.status="-1"
#     doc.save()
###########################################################################
# def parseDocumentCSV(doc):
#     # supposing header where first column is id
#     # id_participant = PEOPLE
#     # other = ATTRIBUTE
#     e = doc.enquete
#     
#     reader = csv.DictReader(open(doc.locationpath),delimiter='\t',quotechar='"')
#     headers = reader.fieldnames
#     
#     mandatories = ["*pseudo","*id","*type"]
#     if not False in [m in headers for m in mandatories]:
#         newSpeaker=None
#         
#         attributetypes=[]
#         # create attributetypes (except for atts already in model: id,type,name)
#         for catval in headers:
#             if catval not in mandatories: # we create only "un-mandatory" attributetypes, since mandatories are stored in speaker model structure
#                 if catval.startswith("_") or catval.startswith("*"):
#                     publicy = '0'
#                 else:
#                     publicy = '1'
#                 newAttType,isnew = AttributeType.objects.get_or_create(enquete=e,publicy=publicy,name=catval)
#                 attributetypes.append(newAttType)
#                 #logger.info("Attributetype ("+doc.name+"): "+catval)
#         
#         for row in reader:
#             ####### COLUMN        *id
#             ####### COLUMN        *type                 (only 'speaker' is displayed in sBrowse)
#             ####### COLUMN        *pseudo (>name)
#             ####### OTHERS        _anyattributes         (not displayed in sBrowse)
#             ####### OTHERS        any attributes        (displayed in sBrowse)
#                         
#             pid = row['*id']
#             pty = SPEAKER_TYPE_CSV_DICT.get(row['*type'],'OTH')
#             pna = row['*pseudo']
#             if pna=="":
#                 pna="Speaker"
#             
#             newSpeaker,isnew = Speaker.objects.get_or_create(enquete=e,ddi_id=pid,ddi_type=pty,name=pna)
#             
#             for attype in attributetypes:
#                 attval=row[attype.name]
#                 if attval=='':
#                     attval='[NC]'
#                 newAttribute,isnew = Attribute.objects.get_or_create(enquete=e,attributetype=attype,name=attval)
#                 newSpeaker.attributes.add(newAttribute)
#             newSpeaker.save()
#     else:
#         # mandatory columns were not found, so what ?
#         praygod=1
#         #logger.info("csv file without mandatory fields:"+doc.name)
#         
#     doc.status='0'
#     doc.save()
###########################################################################    
# def parseDocumentTEI(doc):
#     e = doc.enquete
#     try:
#         # keep original xml in database
#         inDoc = open(doc.locationpath,'r')
#         # NB: HIAT syntax understand "/" as incident "repair" ! dirty workaround here ! (will disapear with other TEI editing technics)
#         # todo: do something
#         corrected = correctTeiPunctuation(''.join(inDoc.readlines()))
#         inDoc.close()
#          doc.contentxml = corrected
#          outDoc = open(doc.locationpath,'w')
#          outDoc.write(corrected)
#         outDoc.close()
#         doc.save()
#     except:
#         # file does not exist ?
#         doc.status='-1'
#         doc.save()
#         
#     # you may want to fetch the speaker list for that file (?)
# #     tree = etree.parse(doc.locationpath)
# #     root = tree.getroot()
# # 
# #     theCodeType,isnew = CodeType.objects.get_or_create(enquete=e,name='speaker')
# #     persons = root.findall(XMLTEINMS+'teiHeader/'+XMLTEINMS+'profileDesc/'+XMLTEINMS+'particDesc/'+XMLTEINMS+'person')
# #     for p in persons:
# #         name=p.findall(XMLTEINMS+'persName/'+XMLTEINMS+'abbr')[0].text
# #         newSpeaker,isnew = Speaker.objects.get_or_create(enquete=e,name=name,codetype=theCodeType)
# #         newSpeaker.textes.add(doc)
# #         newSpeaker.save()
###########################################################################
















###########################################################################
# def exportEnquetesAsXML():
#     filePath = settings.REANALYSEUPLOADPATH+"export_enquetes.xml"
#     XMLSerializer = serializers.get_serializer("xml")
#     xml_serializer = XMLSerializer()
#     fileOut = open(filePath, "w")
#     xml_serializer.serialize(Enquete.objects.all(), stream=fileOut)
#     fileOut.close()
#     logger.info("exporting all Enquetes to XML:"+filePath)
###########################################################################









###########################################################################
# DEPRECATED NOW (we only use XML TEI)
# def parseDocumentAtlasTi(atlasdoc):
#     # creates Documents referenced in the Atlas.ti.xml project file
#     # creates all Speaker / Codes / Quotations
#     e = atlasdoc.enquete
#     
#     tree = etree.parse(atlasdoc.locationpath)
#     root = tree.getroot()
#     doclocs = root.xpath('dataSources/dataSource')
#     docs = root.xpath('primDocs/primDoc')
#     codes = root.xpath('codes/code')
#     families = root.xpath('families/codeFamilies/codeFamily')
#     links = root.xpath('links/objectSegmentLinks/codings/iLink')
#     
#     # creates dictionnary linking id of doc to doc file path
#     theDocs=dict()
#     for doc in doclocs:
#         theDocs[doc.attrib['id']] = doc.attrib['loc']
#     # creates dictionnary linking id of code to codefamily name
#     theCodeFamilies=dict()
#     for fam in families:
#         famName = fam.attrib['name']
#         for c in fam.xpath('item'):
#             codeId = c.attrib['id']
#             theCodeFamilies[codeId]=famName
#     # creates dictionnary linking [quotationId]>codeName & [quotationId]>familyName
#     theCodes=dict()
#     theFamilies=dict()
#     for link in links:
#         theQuotationId = link.attrib['qRef']
#         theCodeId = link.attrib['obj']
#         code = root.xpath('codes/code[@id="'+theCodeId+'"]')[0]
#         codeName = code.attrib["name"]
#         theCodes[theQuotationId]=codeName
#         theFamilies[theQuotationId]=theCodeFamilies[theCodeId]
#         #print "relation :",theQuotationId,codeName
#     
#     # loop for each text found in XML
#     for doc in docs :
#         docName = doc.attrib['name'] 
#         docLoc = theDocs[doc.attrib['loc']]
#         # we suppose it is already in the upload path
#         folderPath = '/'.join( atlasdoc.locationpath.split('/')[:-1] )
#         theDocPath = folderPath + '/' + docLoc
#         # create object, status=1 means "loading"
#         newDoc=Texte(status='1',name=docName,enquete=e,locationpath=theDocPath,doctype='CTX')
#         newDoc.description='convert to html+txt and code'
#         # get file size
#         newDoc.filesize=int(os.path.getsize(theDocPath)/1024)
#         newDoc.save()
#         theDocContent=""
#         dstatus='1'
#         #try:
#         logger.info("Creating document:"+theDocPath)
#         if os.path.isfile(theDocPath): # check if exist
#             # we fetch content of rtf file and put it in database
#             if docLoc.endswith('.rtf'):
#                 ##### A ##### old method with "Pyth" python lib
#                 """
#                 rtfdoc = Rtf15Reader.read(open(theDocPath, "rb"))
#                 fileOutTxt=open(theDocPathSinExt+".txt",'w')
#                 fileOutHtml=open(theDocPathSinExt+".htm",'w')
#                 PlaintextWriter.write(rtfdoc, target=fileOutTxt)
#                 XHTMLWriter.write(rtfdoc, target=fileOutHtml, pretty=True)
#                 fileOutTxt.close()
#                 #fileOutHtml.close()
#             # Reading simple txt file
#             inDoc = open(theDocPathSinExt+'.txt','r')
#             theDocContent = ''.join(inDoc.readlines())
#             inDoc.close()
#                 """
#                 ##### B ##### using command line app
#                 theDocContent = Popen(['unrtf', theDocPath], stdout=PIPE).communicate()[0]
#                 theDocContent = convertUnrtfHtmlToTxt( theDocContent )
#                 
#             if len(theDocContent)>0:
#                 dstatus='0'
#             else:
#                 dstatus='2'
#         else: # problem, file does not exist
#             theDocContent = "File "+theDocPath+" does not exist"
#             dstatus='-1'
#         #except:
#             #theDocContent = "Problem trying to parse "+theDocPath
#         newDoc.content=theDocContent
#         newDoc.status=dstatus
#         newDoc.save()
#         
#         # create all quotations
#         quotes = doc.xpath('quotations/q')
#         for q in quotes:
#             tid = q.attrib['id'] 
#             tloc = q.attrib['loc'] # "1 @ 5, 42 @ 5!"
#             try:
#                 tname = theCodes[tid]
#             except:
#                 tname = "unspecifiedCodeInXml"
#             try:
#                 tfam = theFamilies[tid]
#             except:
#                 tfam = "unspecifiedCodeFamilyInAtlasXml"
#             theCode=None
#             TheCodeType,isnew = CodeType.objects.get_or_create(enquete=e,name=tfam)
#             if tfam=='speaker':
#                 # get Speaker to associate quote to him
#                 theCode,isnew = Speaker.objects.get_or_create(enquete=e,name=tname,codetype=TheCodeType)
#             else:
#                 # get AttributeType
#                 #theAttType = AttributeType.objects.get_or_create(enquete=e,name=tfam)
#                 # get Attribute to associate quote to it
#                 #theAttrib = Attribute.objects.get_or_create(enquete=e,name=codeName, category=codeCat)
#                 theCode,isnew = Code.objects.get_or_create(enquete=e,name=tname,codetype=TheCodeType)
#                 # link that code to this text (manyToMany relationship)
#             # associate the current text with that Code/Speaker
#             theCode.textes.add(newDoc)
#             theCode.save()
#             
#             # now, create Quotation, as an instance that Code/Speaker
#             sp=re.compile('[,!]')
#             dec=re.split(sp,tloc)
#             ss=dec[0].split('@')
#             ss.reverse()
#             ee=dec[1].split('@')
#             ee.reverse()
#             offs=','.join( ss )
#             offe=','.join( ee )
#             offs = re.sub(' ','',offs)
#             offe = re.sub(' ','',offe)
#             newQuot = Quotation(code=theCode,texte=newDoc,offs=offs,offe=offe)
#             newQuot.save()
#     logger.info("Importing AtlasTiXML Completed")
#     atlasdoc.status='0'
#     atlasdoc.save()
###########################################################################











