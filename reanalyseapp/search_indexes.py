# -*- coding: utf-8 -*-
################################################
from haystack.indexes import *
from haystack import site
from reanalyseapp.models import *
################################################

# For the most basic usage, you can simply register a model with the `site`.
# It will get a `haystack.indexes.BasicSearchIndex` assigned to it, whose
# only requirement will be that you create a
# `search/indexes/bare_bones_app/cat_text.txt` data template for indexing.
################################################


# This is where fields for solr/lucene indexing are set
# note that you may need to modify schema.xml file anyway... cause haystack isn't so much "tunable"

################################################
# USED FOR FULL TEXT SEARCH
class SentenceIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	
	# to search only in a specific enquete
	enqueteid = IntegerField(model_attr='enquete__id')
	
	# needed to do facets filtering results
	texteid = IntegerField(model_attr='texte__id', faceted=True)
	speakerid = IntegerField(model_attr='speaker__id', faceted=True)
	
	# used to sort by name (texte/speaker)
	texte = CharField(model_attr='texte__name', faceted=True)
	speaker = CharField(model_attr='speaker__name', faceted=True)
	# PROBLEM: CharField should become a field_type="string" in the schema.xml, but.... no > "text"
	# so that there is some problems with sorting (only taking care of first chars, not full string)
	# ... so you can change it manually if you need to
	
	"""
	If youre working with standard text, EdgeNgramField tokenizes on whitespace.
	This prevents incorrect matches when part of two different words are mashed together as one n-gram. This is what most users should use.
	If youre working with Asian languages or want to be able to autocomplete across word boundaries, NgramField should be what you use.
	ie, for "youpi'
	EdgeNgram 	= youp, you, yo
	Ngram 		= yo, ou, up, pi
	"""
	# added for autocomplete... ? ...cause "yo" can return "youpi" occurrences !
	# todo: try it...
	#content_c_auto = EdgeNgramField(model_attr='contenttxt')
	#content_w_auto = NgramField(model_attr='contenttxt')
	
	# nb: to do real word ngrams : "youpi je mange" = youpi, youpi je, youpi je mange, je mange
	# .. you need to modify schema.xml file in the solr conf ..



################################################
# USED FOR TFIDF IN SPEAKER CORPUS
class SpeakerIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	
	# to search only in a specific enquete
	enqueteid = IntegerField(model_attr='enquete__id')
	
	# from the speaker
	speakerid = IntegerField(model_attr='id')
	
	# ngrams
	ngrams = EdgeNgramField(model_attr='contenttxt')
################################################


site.register(Sentence,SentenceIndex)
site.register(Speaker,SpeakerIndex)



















################################################
# class TexteIndex(RealTimeSearchIndex):
# 	text = CharField(document=True, use_template=True)
# 	name = CharField(model_attr='name')
# 	doctype = CharField(model_attr='doctype')
# 	description = CharField(model_attr='description')
# 	
# 	ints = MultiValueField()
# 		
# # 	def index_queryset(self): # to filtere results
# # 		#return Texte.objects.filter(public=True)
# # 		return Texte.objects.all()
# 		
# 	def prepare_ints(self, obj):
# 		return [iT.content for iT in obj.intervention_set.all()]
################################################



################################################

# class Note(models.Model):
# 	user = models.ForeignKey(User)
# 	pub_date = models.DateTimeField()
# 	title = models.CharField(max_length=200)
# 	body = models.TextField()
# 
# class NoteIndex(SearchIndex):
# 	text = CharField(document=True, use_template=True) # use_template allows using "templates/search/indexes/reanalyseapp/graph_text.txt"
# 	author = CharField(model_attr='user')
# 	pub_date = DateTimeField(model_attr='pub_date')
# 
# 	def index_queryset(self):
# 		"""Used when the entire index for model is updated."""
# 		return Note.objects.filter(pub_date__lte=datetime.datetime.now())
# 
# site.register(Note, NoteIndex)

################################################

# BUT YOU CAN ALSO DO :

# More typical usage involves creating a subclassed `SearchIndex`. This will
# provide more control over how data is indexed, generally resulting in better
# search.
#class DogIndex(RealTimeSearchIndex):
#	text = CharField(document=True, use_template=True)
#	 We can pull data straight out of the model via `model_attr`.
#	breed = CharField(model_attr='breed')
#	 Note that callables are also OK to use.
#	name = CharField(model_attr='full_name')
#	bio = CharField(model_attr='name')
#	birth_date = DateField(model_attr='birth_date')
#	 Note that we can't assign an attribute here. We'll manually prepare it instead.
#	toys = MultiValueField()
#	
#	def index_queryset(self):
#		return Dog.objects.filter(public=True)
#	
#	def prepare_toys(self, obj):
#		 Store a list of id's for filtering
#		return [toy.id for toy in obj.toys.all()]
#		
#		 Alternatively, you could store the names if searching for toy names
#		 is more useful.
#		 return [toy.name for toy in obj.toys.all()]
#
#
#site.register(Dog, DogIndex)
