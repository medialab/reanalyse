#
#   Import script for .csv files.
#	Note: manifest a strong printaholism.
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

def update( textes, enquete, csvdict ):
	print """

	WELCOME TO APP UPDATER

	-------------------------------

	"""


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
			locationgeo = re.sub( r'[^0-9\.,]', '', row['*locationgeo'])
			researcher = row['*researcher']
			article =  row['*article']
		except KeyError, e:
			print "            Field format is not valid: %s " % ( e )
			break

		# print row['*name']doc_name = 			row['*name']
		
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
		texte.save()
		#try


def main( argv ):
	parser = OptionParser( usage="\n\n%prog --enquete=34 --csv=/home/dgu/meta_documents.csv" )

	parser.add_option("-c", "--csv", dest="csvfile", help="csv file absolute path")
	parser.add_option("-e", "--enquete", dest="enquete_id", help="enquete identifier")

	( options, argv ) = parser.parse_args()

	if options.enquete_id is None:
		error("enquete_id arg not found!", parser)

	
	if options.csvfile is None:
		error("csvfile arg was not found!", parser)

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
		print t.name #, t.locationpath
	update( textes, enquete, csvdict )

	print """

	-------------------------------

	THANK YOU FOR USING APP UPDATER
	Task completed. Bye!

	"""


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