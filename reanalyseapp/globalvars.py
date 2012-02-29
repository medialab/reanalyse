# -*- coding: utf-8 -*-
############################################################
# in edBrowse / esBrowse (height is set in css
LITTLEFRISEMAXWIDTH = 100
############################################################
STATUS_CHOICES = (
	('0', 'OK'),
	('-1', 'Failed'),
	('5', 'Waiting'),	
	('1', 'Loading'),
	('2','Parsing'),
	('3','Styling'),
	('4','**Internal use'),
	('77', '**You won something')
)

# categories in edbrowse (others won't show up)
DOCUMENT_CATEGORIES = ['verbatim','analyse','preparatory','publication']

DOCUMENT_TYPE_CHOICES = (
	('PDF', 'PDF'),
	('TEI', 'XML TEI'),
	('TXT', 'Text File'),
	('HTM', 'HTML File'),
	('RTF', 'RTF'),
	('CSV', 'CSV Table'),
	('ATL', 'XML Atlas.Ti'),
	('CTX', 'CAQDAS RTF'),
	('LNK', 'External link'),
)
# To know if we show/hide speaker attributes
ATTRIBUTE_PUBLICY_CHOICES = (
	('0', 'Private'),
	('1', 'Public'),
	('2', '**Unused'),	
)
# Speaker type translator for CSV
SPEAKER_TYPE_CSV_DICT = {
	'speaker':'SPK',
	'investigator':'INV',
	'protagonist':'PRO',
}
SPEAKER_TYPE_CHOICES = (
	('INV', 'Investigator'),
	('SPK', 'Speaker'),
	('PRO', 'Protagonist'),
	('OTH', 'Unknown'),
)
# COLORS for TYPES
SPK_COLORS={}
SPK_COLORS['INV']='#EFEDFC'
SPK_COLORS['SPK']='#E3FBE9'
SPK_COLORS['PRO']='#FFDC98'
SPK_COLORS['OTH']='#FFFFFF'

LANG_CHOICES = (
	('FR', 'Français'),
	('EN', 'English'),
)

################################################################################ VERBATIM
########## PONCTUATION
SENTENCE_UTT_SYMBOLS = dict()
SENTENCE_UTT_SYMBOLS['exclamative']='! '
SENTENCE_UTT_SYMBOLS['declarative']='. '
SENTENCE_UTT_SYMBOLS['interrogative']='? '
SENTENCE_UTT_SYMBOLS['not_classified']=' ' # and other keys

########## CODES ACTIVATED (every code need to be declared in DEFINITIONS below anyway)
# ACTIVATED CODES = those in TextStreamTimeline viz (in order) - nb: if there is not code in texte, it will not show on viz !
STREAMVIZCODES={}
STREAMVIZCODES['codes'] 	= ['question','silence','hesitation','laugh','inaudible','break','comment','time']
# deprecated colors, now set in reanalyse.css
#STREAMVIZCODES['colors'] 	= ['#66CCFF','#BFBD9F','#EC993B','#D9FF00','#ED5300','#ED5300','#517368','#66CCFF']

# ACTIVATED CODES = displayed IN edShow to show/hide
PARVBCODES={}
PARVBCODES['Transcription'] = 	['break','comment','inaudible','question','time']
PARVBCODES['Verbatim'] = 		['body','directed','hesitation','interruption','laugh','silence']

# THOSE YOU WANT TO PUT SPECIALLY on the margin (will add a css class)
PARVBMARGL = ['comment','break']
PARVBMARGR = ['time']

########## CODES DEFINITION
# SIMPLE IMAGE
CODES_IMAGE={}
CODES_IMAGE['hesitation']=				'hesitation'
CODES_IMAGE['inaudible']=				'inaudible'
CODES_IMAGE['interruption']=			'interruption'
CODES_IMAGE['part:echo']=				'interruption'
CODES_IMAGE['laugh']=					'laugh'
CODES_IMAGE['silence']=					'silence'
CODES_IMAGE['points de suspension']=	'silence'	# (soon deprecated) more mapping, because some verb of test-studies may contain thoses

# IMAGE WITH TOOLTIP
CODES_IMAGE_TOOLTIP={}
CODES_IMAGE_TOOLTIP['break:']=			'break'
CODES_IMAGE_TOOLTIP['body:']=			'body'
CODES_IMAGE_TOOLTIP['comment:']=		'comment'
CODES_IMAGE_TOOLTIP['directed:']=		'directed'
CODES_IMAGE_TOOLTIP['question:']=		'question'
CODES_IMAGE_TOOLTIP['time:']=			'time'
CODES_IMAGE_TOOLTIP['to:']=				'directed'	# (soon deprecated) more mapping, because some verb of test-studies may contain thoses

# TEXT STYLING
CODES_TEXT={} # text styling (no image no tooltip)
CODES_TEXT['strong:']=			'strong'

# TEXT STYLING WITH TOOLTIP
CODES_TEXT_TOOLTIP={} # text styling (with tooltip)
CODES_TEXT_TOOLTIP['sic:']=				'sic'
CODES_TEXT_TOOLTIP['uncertain:']=		'uncertain'

########## ALL CODES TO CSS CLASSES
CODE_TO_CSS={}
ALLCODES={}
ALLCODES.update(CODES_IMAGE)
ALLCODES.update(CODES_IMAGE_TOOLTIP)
ALLCODES.update(CODES_TEXT)
ALLCODES.update(CODES_TEXT_TOOLTIP)
for k in ALLCODES.values():
	CODE_TO_CSS[k]='text_'+k


########## TREETAGGER CODES
# source:
# http://www.revue-texto.net/Corpus/Publications/Poudat_Taggers.html
CODES_TREETAGGER={}
CODES_TREETAGGER['MISC']={}
CODES_TREETAGGER['MISC']['ABR'] = "abréviations"
CODES_TREETAGGER['MISC']['ADJ'] = "adjectifs"
CODES_TREETAGGER['MISC']['ADV'] = "adverbes"
CODES_TREETAGGER['MISC']['INT'] = "interjections"
CODES_TREETAGGER['MISC']['CON'] = "conjonctions"
CODES_TREETAGGER['MISC']['NOM'] = "noms"
CODES_TREETAGGER['MISC']['NUM'] = "numéraux"
CODES_TREETAGGER['MISC']['NAM'] = "noms propres"
CODES_TREETAGGER['MISC']['PRP'] = "prépositions"
CODES_TREETAGGER['MISC']['PUN'] = "marques de ponctuation"
CODES_TREETAGGER['MISC']['PUN_cit'] = "marques de ponctuation marquant des citations"
CODES_TREETAGGER['MISC']['SENT'] = "phrases"
CODES_TREETAGGER['MISC']['SYM'] = "symboles"

CODES_TREETAGGER['PRONOMS']={}
CODES_TREETAGGER['PRONOMS']['PRO'] = "pronoms"
CODES_TREETAGGER['PRONOMS']['DET_ART'] = "articles"
CODES_TREETAGGER['PRONOMS']['DET_POS'] = "pronoms possessifs"
CODES_TREETAGGER['PRONOMS']['PRO_DEM'] = "pronoms démonstratifs"
CODES_TREETAGGER['PRONOMS']['PRO_IND'] = "pronoms indéfinis"
CODES_TREETAGGER['PRONOMS']['PRO_PER'] = "pronoms personnels"
CODES_TREETAGGER['PRONOMS']['PRO_POS'] = "pronoms possessifs"
CODES_TREETAGGER['PRONOMS']['PRO_REL'] = "pronoms relatifs"
CODES_TREETAGGER['PRONOMS']['PRP_det'] = "déterminants contractés (au,du,aux,des)"

CODES_TREETAGGER['VERBES']={}
CODES_TREETAGGER['VERBES']['VER_cond'] = "verbes au conditionnel"
CODES_TREETAGGER['VERBES']['VER_futu'] = "verbes au futur"
CODES_TREETAGGER['VERBES']['VER_impe'] = "verbes à l'impératif"
CODES_TREETAGGER['VERBES']['VER_impf'] = "verbes à l'imparfait"
CODES_TREETAGGER['VERBES']['VER_infi'] = "verbes à l'infinitif"
CODES_TREETAGGER['VERBES']['VER_pper'] = "participes passés"
CODES_TREETAGGER['VERBES']['VER_ppre'] = "participes présents"
CODES_TREETAGGER['VERBES']['VER_pres'] = "verbes au présent"
CODES_TREETAGGER['VERBES']['VER_simp'] = "verbes au passé simple"
CODES_TREETAGGER['VERBES']['VER_subi'] = "verbes au subjonctif imparfait"
CODES_TREETAGGER['VERBES']['VER_subp'] = "verbes au subjonctif présent"





################################################################################ COLORS
########## COLORS FOR STYLING VERBATIMs (cyclic)
# me
HTML_COLORS=['#FADFCA','#E6F5F3','#FFFDD4','#DEF5DC','#E7E4EB','#c7e9c0','#dadaeb','#d9d9d9','#c6dbef','#fdd0a2']
# http://www.colorhunter.com/tag/pastel/
#removed from next line '#C05253','#D4A9A7','#EC993B','#CF756F'
HTML_COLORS+=['#FFC09D','#FF9987','#FFDC98','#ECC0AF','#F7DCBC','#F3D6CE','#CEA4B0','#F9C49A']
# http://www.hitmill.com/html/pastels.html (there is more)
HTML_COLORS+=['#FFECEC','#FFEEFB','#FFECF5','#FFEEFD','#FDF2FF','#FAECFF','#F1ECFF']
HTML_COLORS+=['#FFECFF','#F4D2F4','#F9EEFF','#F5EEFD','#EFEDFC','#EAF1FB','#DBF0F7']
HTML_COLORS+=['#EEEEFF','#ECF4FF','#F9FDFF','#E6FCFF','#F2FFFE','#CFFEF0','#EAFFEF']
HTML_COLORS+=['#E3FBE9','#F3F8F4','#F1FEED','#E7FFDF','#F2FFEA','#FFFFE3','#FCFCE9']

# Scale from d3.js d3.scale.category20()
#HTML_COLORS=['#aec7e8','#ffbb78','#98df8a','#ff9896','#c5b0d5','#c49c94','#f7b6d2','#c7c7c7','#dbdb8d','#9edae5']

################################################################################ XML
########## NAMESPACES to parse XML
# DDI
XMLDDINMS='{http://www.icpsr.umich.edu/DDI}'
# TEI
XMLTEINMS='{http://www.tei-c.org/ns/1.0}'
XMLNMS ='{http://www.w3.org/XML/1998/namespace}'
# XML TXM
XMLTXM = '{http://textometrie.org/1.0}'
############################################################





############################################################################################################## VISUALIZATIONS
########## ACTIVATED VIZ TYPES (show/hide in evBrowse)
GRAPHTYPES 	= ['Graph_SpeakersSpeakers','Graph_SpeakersWords','Graph_SpeakersAttributes']
VIZTYPES	= GRAPHTYPES + ['Cloud_SolrSpeakerTagCloud','TexteStreamTimeline','Attributes']

########## VIZ DESCRIPTION
# nb: viz description is used to document the viz, not to explain them technically
# to have informations about viz types, see Normalization page


VIZTYPESDESCR = 'Please clic me to update (html) description. If you need general technical information about that viz type, please clic the blue bubble above.'

# VIZTYPESDESCR={}
# VIZTYPESDESCR['Graph_SpeakersSpeakers'] = 		'Speakers Similarities Graph'
# VIZTYPESDESCR['Graph_SpeakersWords'] = 			'Bipart Graph Speakers - Words'
# VIZTYPESDESCR['Graph_SpeakersAttributes'] = 	'Bipart Graph Speakers - Attributes'
# VIZTYPESDESCR['StudyOverview'] = 'aimed to be the main overview viz at study home page'
# VIZTYPESDESCR['Overview'] = 'trying a simple graph overview for left menu facet'
# VIZTYPESDESCR['Attributes'] = '\
# 	Simple display of attributes.<br/>\
# 	Click to see the repartition of other attributes (label is then gray-scaled based on number of speakers).'
# VIZTYPESDESCR['TexteStreamTimeline'] = 	'\
# 	Timeline of speakers interventions and paraverbal. Time(x) is based on number of sentences.<br/>\
# 	Change step value to change sentence-count-interval.'
# VIZTYPESDESCR['Cloud_SolrSpeakerTagCloud'] = '\
# 	<b>Most freq n-grams with tfidf (fetched from solr indexing)</b><br/>\
# 	<b>DF</b> = (normalized) number of speakers using ngram<br/>\
# 	<b>TF</b> = (normalized) ngram count for that speaker >>> <b>GRAY-LEVEL</b><br/>\
# 	<b>TFIDF</b> = TF/DF = specificity of ngram for that speaker >>> <b>SIZE</b><br/>\
# 	NB: we exclude ngrams if [DF=TF=1] OR [included in other longer with same DF,TF]'
########################################################################################################################


DDILABELS={}
DDICATEGORIES={}
DDILABELS["idno"]		="Identifiant unique"
DDILABELS["titl"]		="Titre"
DDILABELS["abstract"]	="Résumé"

DDILABELS["description"]		="Description"
DDILABELS["relpubl"]			="Publications"

DDILABELS["discipline"]	="Discipline"
DDILABELS["keywords"]	="Mots clefs"
DDILABELS["topicclassification"]	="Classification"
DDILABELS["timeperiodcovered"]	="Période couverte"
DDILABELS["country"]		="Pays couverts"

DDILABELS["authenty"]	="Auteur"
DDILABELS["fundag"]		="Agence de financement"
DDILABELS["grantno"]		="Bourses"
DDILABELS["distrbtr"]	="Distributeur des données"
DDILABELS["depositr"]	="Déposant"
DDILABELS["locationofunitsofobservation"]	="Niveau de comparatisme"
DDILABELS["geogcover"]		="Couverture géographique"
DDILABELS["spatialunits"]	="Unités spatialisées"
DDILABELS["observunits"]		="Unités d'observation"
DDILABELS["targetgroups"]	="Groupes de population ciblés"
DDILABELS["studydates"]		="Dates de l'enquête"
DDILABELS["colldate"]		="Dates de récolte des données"
DDILABELS["timedimension"]	="Périodicité"
DDILABELS["modedatacollection"]	="Accès aux observations"
DDILABELS["sampprocedure"]	="Echantillonnage "
DDILABELS["weighting"]		="Segmentation"
DDILABELS["methodofdatacollection"]	="Technique de collection"
DDILABELS["numberoffiles"]	="Nombre de documents"
DDILABELS["datakind"]		="Types de documents"
DDILABELS["numberofunits"]	="Nombre d'observations"
DDILABELS["collsitu"]		="Durée des observations"
DDILABELS["transcription"]	="Transcription"
DDILABELS["anonymization"]	="Anonymisation"
DDILABELS["analysis"]		="Analyse"
DDILABELS["langdata"]		="Language données"
DDILABELS["langdoc"]			="Langage documentation"
DDILABELS["accessconditions"]	="Conditions d'accès"
DDILABELS["locarch"]				="Localisation archives"
DDILABELS["contact"]				="Contact"
DDILABELS["firstedition"]	="Première version"
DDILABELS["latestedition"]	="Dernière version"
DDILABELS["copyright"]	="copyright"
DDILABELS["software"]	="Logiciel"
DDILABELS["authEnty"]	="Edition"

