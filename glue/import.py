import os, sys, re, mimetypes, logging
from datetime import datetime

# get path of the django project
path = ("/").join( sys.path[0].split("/")[:-2] )
app_path = ("/").join( sys.path[0].split("/")[:-1] )
settings_module = ('.').join([ sys.path[0].split("/")[-2],'settings' ])

if path not in sys.path:
    sys.path.append(path)
if app_path not in sys.path:
    sys.path.append(app_path)

os.environ['DJANGO_SETTINGS_MODULE'] =  settings_module


from django.conf import settings
from django.core.files.base import ContentFile
from django.db.models.loading import get_model
from django.db.utils import IntegrityError
from glue.models import Pin

# @todo: configure logger
logger = logging.getLogger("glue")
logger.info("Start importing pins...")


# open upload folder
def main( argv ):
	try:
		upload_path = argv[0]

	except IndexError,e:
		print "Usage: python import.py /path/to/uploads"
		print "    Please provide a valid path!"
		logger.error("Pins uploads path not found!")
		return

	if not os.path.isdir( upload_path ):
		print "Usage: python import.py /path/to/uploads"
		print "    Path %s does not exists or is not readable!" % upload_path
		logger.error("Pins uploads path '%s' is not a valid path" % upload_path)
		return

	logger.info("Pins uploads dir: '%s'" % upload_path)
	
	# list files along with their mimetype
	files = os.listdir( upload_path )
	
	
	for f in files:
		print f

		# name, mimetype and binary content
		filepath = os.path.join( upload_path, f )
		filename = os.path.basename( filepath )
		slug = re.sub(r'[^a-zA-Z\d-]','', os.path.basename( filename ) )
		mimetype	=  mimetypes.guess_type( filepath )[0]
		content = open( filepath, 'rb').read()

		# save english
		try:
			p = Pin( slug=slug, title=filename, mimetype=mimetype, language='EN' )
			p.local.save( filename, ContentFile( content ) )
			p.save()

			# for each language, create a pin clone
			pc = Pin( slug=p.slug, title=p.title, mimetype=p.mimetype, language='FR', local=p.local )
			pc.save()

		except IntegrityError, e:
			print "Cannot save '%s'. Delete the file first, because an IntegrityError exception occurred: %s" % ( filename, e)
			continue

		

if __name__ == '__main__':
	# get corpus name
	main(sys.argv[1:])
