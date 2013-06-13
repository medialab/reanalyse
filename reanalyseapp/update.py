# -*- coding: utf-8 -*-
#
#   Import script for .csv files.
#    Note: manifest a strong printaholism.
#
import sys, os, csv, re
from optparse import OptionParser


# get path of the django project
path = ("/").join( sys.path[0].split("/")[:-1] )
ppath = ("/").join( sys.path[0].split("/")[:-2] )

if path not in sys.path:
    sys.path.append(path)
if ppath not in sys.path:
    sys.path.append(ppath)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


# django specific import
from django.conf import settings
from reanalyseapp.models import Enquete, Texte, Tag
from datetime import datetime

from reanalyseapp.views import *

def update( textes, enquete, csvdict ):

    print "        %s documents found in enquete: \"%s\", id:%s" % ( textes.count(), enquete.name, enquete.id )
    print

    for (counter, row) in enumerate(csvdict):
        # print row
        if counter == 0:
            print "        keys: %s" % row.keys()
            # normally, the second meta_documents csv file line is a field description header.
            continue
        print "        %s." % counter
        try:
            texte_url = row['*file']
            texte_name = row['*name']
            locationgeo = re.sub( r'[^0-9\.,-]', '', row['*locationgeo'])
            #researcher = row['*researcher']
            article =  row['*article']
            
            if('/' in row['*date']):
                dateFormat = "%d/%m/%y"
            elif('_' in row['*date']) :
                dateFormat = "%d_%m_%y"
            elif('-' in row['*date']) :
                dateFormat = "%d-%m-%y"
            
            #print(row['*date'])
            date = row['*date']#datetime.datetime.strptime(row['*date'], dateFormat) #"31-12-12"
            
            #date = datetime.datetime.strptime(row['*date'], '%d/%m/%y').strftime(dateFormat)       
           
        except KeyError, e:
            print "            Field format is not valid: %s " % ( e )
            break

        # print row['*name']doc_name =             row['*name']
        
        try:
            texte = Texte.objects.get( enquete=enquete, name=row['*name'], locationpath__regex=( ".?%s" % os.path.basename( texte_url ) ) )

        except Texte.DoesNotExist, e:
            print "            No texte found with : \"%s\", %s " % ( texte_name, e )
            
            foo=raw_input('\n            Skip this line and go on ? [ Y / N ] : ')
            
            if foo.upper() == 'N':
                print "            Script stopped !"
                break
            continue
        except Texte.MultipleObjectsReturned, e:
            print "            More than one texte found with : \"%s\", %s, %s " % ( texte_name, os.path.basename( texte_url ), e )
            foo=raw_input('\n            Skip this line and go on ? [ Y / N ] : ')
            
            if foo.upper() == 'N':
                print "            Script stopped !"
                break
            
        print "            %s \"%s\": %s" % ( texte.id, texte_name, locationgeo )
        
        # get or save tag
        print  "            %s \"%s\": %s" % ( texte.id, texte_name, article )

        try:
            t = Tag.objects.get( type=Tag.ARTICLE, slug=article )
        except Tag.DoesNotExist, e:
            print  "            %s \"%s\": creating tag [%s:%s]" % ( texte.id, texte_name, article, Tag.ARTICLE )
            t = Tag( type=Tag.ARTICLE, slug=article, name=article)
            t.save()

        # save location geo
        texte.locationgeo = locationgeo
        texte.tags.add( t )
        texte.date = date
        texte.save()
        #try


def install( upload_path, enquete_path ) :
    from imexport import importEnqueteUsingMeta
    print "        from upload path '%s'" % upload_path
    
    if not os.path.exists( upload_path ):
        print "        upload_path folder '%s' does not exists or it is not readable !" % upload_path
        print
        return
    
    print "        from upload path '%s'" % enquete_path
    if not os.path.exists( enquete_path ):
        print "        enquete_path folder '%s' does not exists or it is not readable !" % enquete_path
        print
        return

    print "        call importEnqueteUsingMeta (please follow up in log file)"
    importEnqueteUsingMeta( upload_path, enquete_path )
    print "        installation completed."


from reanalyseapp.models import *

def testTEIparse(texte_id):
    texte = Texte.objects.get(id=texte_id)
    parseXmlDocument(texte)
    

def testEnqueteImport(foldName):
   folname = foldName    
   upPath = settings.REANALYSEUPLOADPATH+folname+"/"
   enqueterootpath='' 
   for f in os.listdir(upPath+"extracted/"):
       if os.path.exists(upPath+"extracted/"+f+"/_meta/"):
           enqueterootpath = upPath+"extracted/"+f+"/"
   
   e = importEnqueteUsingMeta(upPath,enqueterootpath)
   
   if(e != None):
       doFiestaToEnquete(e)
   else:
        print('ok')


def deleteSpeakers(enquete_id):
  
   
    textes = Texte.objects.filter(enquete_id=enquete_id, doctype="TEI")

    for t in textes :
        speakers = t.speaker_set.filter()
        
        print(speakers)
        for s in speakers :
            s.delete()
           
#
#CheckMetaDocuments
#Check if every file exists in MetaDocuments
#return False with error dictionnary or True
#
def isMetaDocOK(upload_path, enquete_path):
    
    from imexport import importEnqueteUsingMeta
    
    if os.path.exists(enquete_path):
        #mandatoryFields = ['*id','*name','*category','*description','*location','*date']
        print("=========== PARSING META_DOCUMENTS.CSV TO CHECK IF A FILE IS MISSING IF TRUE IMPORT IS CANCELLED")
        ###### Parsing Documents
        doc = csv.DictReader(open(enquete_path+'_meta/meta_documents.csv'),delimiter='\t')
        
        error = False
        error_dict = {}
        
        for counter, row in enumerate(doc):
            if row['*id']!='*descr':
                file_location = upload_path+row['*file']
                try:
                    open(file_location)                        
                except IOError, e:
                    if(e.args[0] == 2):#no such file or directory
                        error = True
                        error_dict.update({file_location:e.args[1]})
			print file_location

        if(error is True):
            return {'status':False, 'error_dict':error_dict}
        else:
            return True









def main( argv ):
    print """
        
    WELCOME TO APP UPDATER

    -------------------------------

    """
    parser = OptionParser( usage="\n\n%prog --enquete=34 --csv=/home/dgu/meta_documents.csv" )

    parser.add_option("-c", "--csv", dest="csvfile", help="csv file absolute path", default="" )
    parser.add_option("-e", "--enquete", dest="enquete_id", help="enquete identifier", default=0 )
    parser.add_option("-p", "--upload_path", dest="upload_path", help="enquete upload path", default="" ) #use with --func=install
    parser.add_option("-x", "--enquete_path", dest="enquete_path", help="enquete extracted path", default="" ) #use with --func=install
    parser.add_option("-f", "--function", dest="func", help="update function", default="update" )
    parser.add_option("-d", "--document_id", dest="document_id", help="document id (Texte)", default="" )

    ( options, argv ) = parser.parse_args()

    if options.func == "isMetaDocOK" :
        print(options.func)
        # install the enquete
        return isMetaDocOK( options.upload_path, options.enquete_path )

    if options.func == "install" :
        if options.csvfile is None:
            error("csvfile arg was not found!", parser)
        else:
            # install the enquete
            return install( options.upload_path, options.enquete_path )
        
    if options.func == "testTEIparse" :
        print(options.func)
        # install the enquete
        return testTEIparse( options.document_id )
    
    
    if options.func == "testDownload" :
        print(options.func)
        # install the enquete
        return testDownload( options.enquete_id )
    
    if options.func == "testEnqueteImport" :
        print(options.func)
        # install the enquete
        return testEnqueteImport( 'up_1371112674.63')

    if options.func == "parseAllTeis" :
       print(options.func)
       # reparseAllteis file of an enquete
       return parseAllTeis( options.enquete_id )

   
    if options.func == "deleteSpeakers" :
        print(options.func)
        # reparseAllteis file of an enquete
        return deleteSpeakers( options.enquete_id )

    if options.enquete_id is None:
        error("enquete_id arg not found!", parser)

    
   

    if not os.path.exists( options.csvfile ):
        error( message="csv file was not found.", parser=parser )

    try:
        enquete = Enquete.objects.get( id=options.enquete_id )
        textes = Texte.objects.filter( enquete=enquete )
    except Enquete.DoesNotExist, e:
        error("noo %s" % e, parser )

    if textes.count() == 0:
        error("no Texte is attached ...? Is that possible ?", parser )

    # parse csv file !
    f = open( options.csvfile, 'rb' )
    csvdict = csv.DictReader( f, delimiter="\t" )
    for t in textes:
       pass# print(textes.count())#print t.name #, t.locationpath
    update( textes, enquete, csvdict )

    print """

    -------------------------------

    THANK YOU FOR USING APP UPDATER
    Task completed. Bye!

    """


def parseAllTeis(enquete_id):
    
    textes = Texte.objects.filter(enquete_id=enquete_id, doctype="TEI")

    for t in textes :
        parseXmlDocument(t)
    
    
def testDownload(enquete_id):
    import zipfile, zlib
    
    """
    zippath = os.path.join( "/tmp/", "enquete_%s.zip" % enquete_id )

    zf = zipfile.ZipFile( zippath, mode='w' )
    
    
    
    """ 
    for t in Texte.objects.filter( enquete_id=enquete_id ):
        
        if('é'.decode('utf-8') in t.locationpath):
            
            t.locationpath= t.locationpath.replace('é'.decode('utf-8'), 'e')
           
        if os.path.isfile(t.locationpath.decode('utf-8')):
            
            if( t.locationpath.find('_ol') or t.locationpath.find('_dl') ):
                print(t.locationpath.split('/', 7)[7])
               
                """
                zf.write( t.locationpath, compress_type=zipfile.ZIP_DEFLATED, 
                            arcname= t.locationpath.split('/', 5)[5])"""
                            

def error( message="generic error", parser=None):
    print 
    print "   ",message
    print
    print
    if parser is not None:
        parser.print_help()
    exit(-1)


# execute srcipt
if __name__ == '__main__':
    main(sys.argv[1:])
