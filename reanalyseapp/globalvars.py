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
	'adjuvant':'PRO',
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

########## VERBATIM Dict : TEI HIAT to CODES
# THOSE DISPLAYED IN edShow View toggle show/hide
PARVBCODES={}
PARVBCODES['transcription'] = 	['inaudible','break','comment','time','question']
PARVBCODES['verbatim'] = 		['hesitation','interruption','laugh','silence','body']

CODES_IMAGE_TOOLTIP={} # with content (tooltip!)
CODES_IMAGE_TOOLTIP['break:']=			'break'
CODES_IMAGE_TOOLTIP['body:']=			'body'
CODES_IMAGE_TOOLTIP['comment:']=		'comment'
CODES_IMAGE_TOOLTIP['time:']=			'time'
CODES_IMAGE_TOOLTIP['question:']=		'question'
CODES_IMAGE_TOOLTIP['to:']=				'directed'

CODES_IMAGE={} # without content (only image)
CODES_IMAGE['hesitation']=				'hesitation'
CODES_IMAGE['interruption']=			'interruption'
#CODES_IMAGE['part:echo:']=				'interruption'
CODES_IMAGE['part:echo']=				'interruption'
CODES_IMAGE['inaudible']=				'inaudible'
CODES_IMAGE['laugh']=					'laugh'
CODES_IMAGE['points de suspension']=	'silence'

CODES_TEXT_TOOLTIP={} # text styling (with tooltip)
CODES_TEXT_TOOLTIP['anonym:']=			'anonym'
CODES_TEXT_TOOLTIP['sic:']=				'sic'
CODES_TEXT_TOOLTIP['uncertain:']=		'uncertain'

CODES_TEXT={} # text styling (no image no tooltip)
CODES_TEXT['strong:']=			'strong'


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



############################################################
########## VERBATIM Dict : CODES to CSS CLASSES
CQDAS_CLASS={}
CQDAS_CLASS['speaker']='text_speaker'
CQDAS_CLASS['theme']='text_theme' # DEPRECATED ?

ALLCODES={}
ALLCODES.update(CODES_IMAGE)
ALLCODES.update(CODES_IMAGE_TOOLTIP)
ALLCODES.update(CODES_TEXT)
ALLCODES.update(CODES_TEXT_TOOLTIP)
for k in ALLCODES.values():
	CQDAS_CLASS[k]='text_'+k

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
VIZTYPES=['Cloud_SolrSpeakerTagCloud','Graph_SpeakersSpeakers','Graph_SpeakersWords','Graph_SpeakersAttributes','TexteStreamTimeline','Attributes']

VIZTYPESDESCR={}
########### D3
VIZTYPESDESCR['StudyOverview'] = 'aimed to be the main overview viz at study home page'
VIZTYPESDESCR['Overview'] = 'trying a simple graph overview for left menu facet'
VIZTYPESDESCR['Attributes'] =			'\
	Simple display of attributes.<br/>\
	Click to see the repartition of other attributes (label is then gray-scaled based on number of speakers).'
#VIZTYPESDESCR['SpeakersByText'] = 		'Showing all texts with color for each speaker'
#VIZTYPESDESCR['WordsBySpeaker'] = 		'For a text, showing all speakers and their amount of words'
#VIZTYPESDESCR['ParaverbalTimeline'] = 	'Timeline of speakers turns and paraverbal'
VIZTYPESDESCR['TexteStreamTimeline'] = 	'\
	Timeline of speakers interventions and paraverbal. Time(x) is based on number of sentences.<br/>\
	Change step value to change sentence-count-interval.'
########### TAG CLOUDS
VIZTYPESDESCR['Cloud_SolrSpeakerTagCloud'] = '\
	<b>Most freq n-grams with tfidf (fetched from solr indexing)</b><br/>\
	<b>DF</b> = (normalized) number of speakers using ngram<br/>\
	<b>TF</b> = (normalized) ngram count for that speaker >>> <b>GRAY-LEVEL</b><br/>\
	<b>TFIDF</b> = TF/DF = specificity of ngram for that speaker >>> <b>SIZE</b><br/>\
	NB: we exclude ngrams if [DF=TF=1] OR [included in other longer with same DF,TF]'

#VIZTYPESDESCR['Cloud_SolrWordSpeakerTagCloud'] = 	'(using solr facets) Most freq solr words'
#VIZTYPESDESCR['Cloud_SolrTermVectorsTagCloud'] = 	'(using termVector) Speaker terms with their tf-idf'
#VIZTYPESDESCR['Cloud_TeiSpeakerTagCloud'] = 		'Simple tag cloud using TEI words parsed in DB'
########### GRAPHS
VIZTYPESDESCR['Graph_SpeakersSpeakers'] = 		'Speakers Similarities Graph'
VIZTYPESDESCR['Graph_SpeakersWords'] = 			'Bipart Graph Speakers - Words'
VIZTYPESDESCR['Graph_SpeakersAttributes'] = 	'Bipart Graph Speakers - Attributes'
#VIZTYPESDESCR['Graph_SolrSpeakerWords'] = 		'Bipart Graph Speakers - Solr Words'
########################################################################################################################





