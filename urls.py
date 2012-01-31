# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
#from reanalyseapp.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('reanalyse',
	
	# set langage redirect view
	(r'^i18n/', include('django.conf.urls.i18n')),
	
	#(r'^test/', 'reanalyseapp.views.testMe'),
	
	(r'^$', 'reanalyseapp.views.home'),
	#(r'^home/$', 'reanalyseapp.views.home'),
	#(r'^$', 'reanalyseapp.views.eBrowse'),

	# url(r'^reanalyse/', include('reanalyseapp.foo.urls')),
	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	
	(r'^html/(?P<templateName>\w+)$', 'reanalyseapp.views.getHtml'),
	
	######################################################################################################
	########## ENQUETES SUR ENQUETE
	# deprecated ?
# 	(r'^ese/home$', 'reanalyseapp.views.eseHome'),
# 	
# 	(r'^ese$', 'reanalyseapp.views.eseBrowse'),
# 	(r'^ese/getjson$', 'reanalyseapp.views.getEseExhibitJson'),
# 	
# 	(r'^ese/a/(?P<eseid>\w+)/$', 'reanalyseapp.views.eseIntro'),
# 	(r'^ese/b/(?P<eseid>\w+)/$', 'reanalyseapp.views.eseContent'),
# 	(r'^ese/c/(?P<eseid>\w+)/$', 'reanalyseapp.views.eseOutro'),
	
	(r'^stream/(?P<eseid>\w+)/(?P<path>[-\._\w\d\/]+\.(mp3|ogg))+', 'reanalyseapp.views.stream'),
	(r'^pdf/(?P<eseid>\w+)', 'reanalyseapp.views.getfile'),
	
	(r'^graph/download/(?P<gid>\w+)', 'reanalyseapp.views.downloadGraph'),
	(r'^graph/serve/(?P<gid>\w+).gexf', 'reanalyseapp.views.serveGraph'),
	(r'^graph/serve/(?P<did>\w+).pdf', 'reanalyseapp.views.servePdf'),
	
	######################################################################################################
	########## ENQUETES
	(r'^e/$', 'reanalyseapp.views.eBrowse'),
	(r'^e/upload$', 'reanalyseapp.views.eUpload'),						# ADD ENQUETE PaGE
	(r'^e/add$', 'reanalyseapp.views.eAddAjax'),						# ajax-ADD (upload one file at a time)
	(r'^e/reset$', 'reanalyseapp.views.eReset'),						# ReaddSET (erase temp upload folder)
	(r'^e/parse$', 'reanalyseapp.views.eParse'),						# PARSE (once all files uploaded)
	(r'^e/(?P<eid>\d+)/delete$', 'reanalyseapp.views.eDelete'),			# DELETE
	
	(r'^e/(?P<eid>\d+)/makealltfidf$', 'reanalyseapp.views.resetAllTfidf'),		# TFIDF ngrams

	(r'^e/solrclear$', 'reanalyseapp.views.eSolrIndexClear'),	# clear whole solr index
	(r'^e/solrupdate$', 'reanalyseapp.views.eSolrIndexUpdate'),	# update whole solr index
	
	(r'^e/export$', 'reanalyseapp.views.exportEnquetes'),
	(r'^e/delete$', 'reanalyseapp.views.deleteEnquetes'),
	
	##### 1.Overview
	(r'^e/(?P<eid>\d+)/$', 'reanalyseapp.views.eShow'),					# SHOW ENQUETE MAIN OVERVIEW

	##### 2.Enquete sur Enquete
	(r'^e/(?P<eid>\d+)/ese/$', 'reanalyseapp.views.eseShow'),			# SHOW ENQUETE SUR ENQUETE
	
	##### 3.Documents
	(r'^e/(?P<eid>\d+)/$', 'reanalyseapp.views.edBrowse'),
	(r'^e/(?P<eid>\d+)/d/$', 'reanalyseapp.views.edBrowse'),
	(r'^e/(?P<eid>\d+)/d/(?P<did>\d+)/$', 'reanalyseapp.views.edShow'),				# DOC normal
	(r'^e/(?P<eid>\d+)/dx/(?P<did>\d+)/$', 'reanalyseapp.views.edXmlShow'),			# DOC html only using xslt
	(r'^e/(?P<eid>\d+)/d/(?P<did>\d+)/parse$', 'reanalyseapp.views.edParseXml'),			# TEI only : build objects from XML structure

	(r'^e/(?P<eid>\d+)/d/(?P<did>\d+)/get$', 'reanalyseapp.views.dGetHtmlContent'),			# TEI get html content SENTENCE
	(r'^e/(?P<eid>\d+)/d/(?P<sid>\d+)/around$', 'reanalyseapp.views.dGetHtmlAround'),		# TEI get html content AROUND INTERVENTION 

	##### 4.Speakers
	(r'^e/(?P<eid>\d+)/s/$', 'reanalyseapp.views.esBrowse'),
	(r'^e/(?P<eid>\d+)/s/(?P<sid>\d+)/$', 'reanalyseapp.views.esShow'),
	(r'^e/(?P<eid>\d+)/ss/make$', 'reanalyseapp.views.makeSpeakerSet'),						# MAKE 		SpeakerSet
	(r'^e/(?P<eid>\d+)/ss/(?P<ssid>\d+)$', 'reanalyseapp.views.getSpeakerSetSpeakers'),		# GET 		SpeakerSet
	(r'^e/(?P<eid>\d+)/ss/delete$', 'reanalyseapp.views.deleteSpeakerSets'),				# DELETE 	SpeakerSets
	(r'^e/(?P<eid>\d+)/setcolor$', 'reanalyseapp.views.setColor'),							# set speaker(s) color
	(r'^e/(?P<eid>\d+)/resetcolor$', 'reanalyseapp.views.resetColors'),						# set all random colors
	
	
	(r'^e/(?P<eid>\d+)/s/(?P<sid>\d+)/ngrams$', 'reanalyseapp.views.esGetSolrTermVector'),	# useful just to fetch solr ngrams for that speaker
	
	
	##### 5.Visualizations
	(r'^e/(?P<eid>\d+)/json/d/(?P<tid>\d+)/$', 'reanalyseapp.views.getLittleFriseJson'),	# little frise texte/speaker content d3 display
	
	(r'^e/(?P<eid>\d+)/v/gethtml$', 'reanalyseapp.views.getVizHtml'),						# fetch viz html
	
	(r'^e/(?P<eid>\d+)/v/$', 'reanalyseapp.views.evBrowse'),
	(r'^e/(?P<eid>\d+)/v/make$', 'reanalyseapp.views.makeVisualization'),					# MAKE VISUALIZATION
	(r'^e/(?P<eid>\d+)/v/(?P<vid>\d+)/public$', 'reanalyseapp.views.evSetPublic'),			# SWITCH PUBLIC FLAG
	(r'^e/(?P<eid>\d+)/v/(?P<vid>\d+)/delete$', 'reanalyseapp.views.evDelete'),				# DELETE
	(r'^e/(?P<eid>\d+)/v/(?P<vid>\d+)/json$', 'reanalyseapp.views.evGetJson'),				# GET JSON VALUES
	(r'^e/(?P<eid>\d+)/v/(?P<vid>\d+)/save$', 'reanalyseapp.views.evSaveHtml'),				# SAVE HTML of vizu in model
	
	##### 6.Search
	#(r'^search/', include('haystack.urls') ),
	(r'^e/(?P<eid>\d+)/search/', 'reanalyseapp.views.eSearch' ),
 	
 	# DEPRECATED
 	#(r'^e/(?P<eid>\d+)/i/(?P<iid>\d+)$', 'reanalyseapp.views.eiGetExtractHtml'),			# Get JSON with html of intervention (for extracts in search results)	
	
	
	################### DEPRECATED ???
# 	# show code
# 	(r'^e/(?P<eid>\d+)/c/(?P<cid>\d+)/$', 'reanalyseapp.views.ecShow'),
# 	# show word
# 	(r'^e/(?P<eid>\d+)/w/(?P<wid>\d+)/$', 'reanalyseapp.views.ewShow'),
# 	# tfidf data in ew_show
# 	(r'^e/(?P<eid>\d+)/json/tfidf/(?P<wid>\d+)$', 'reanalyseapp.views.getWordStat'),
# 	# statenquete in e_browse
# 	(r'^e/(?P<eid>\d+)/json/(?P<data>\w+)/$', 'reanalyseapp.views.getJsonData'),
# 		
# 	(r'^e/(?P<eid>\d+)/action/(?P<cmd>\w+)$', 'reanalyseapp.views.makeAction'),				# ACTION : CAL(calculate TFIDFs) / GET(return jsonTFIDF) / GRAPH(make graph Words/Speakers)
# 	
# 	# styling deprecated ! (made in the parsing)
# 	#(r'^e/(?P<eid>\d+)/d/(?P<did>\d+)/refresh$', 'reanalyseapp.views.edStylizeContent'),	# TEI/CAQDAS : build html content from objects
# 	
# 	#(r'^e/(?P<eid>\d+)/d/(?P<did>\d+)/json$', 'reanalyseapp.views.edGetJson'),				# Get JSON with all Data for D3 - TEXTE
# 	#(r'^e/(?P<eid>\d+)/json$', 'reanalyseapp.views.eGetJson'),								# Get JSON with all Data for D3 - ENQUETE
# 	#(r'^e/(?P<eid>\d+)/tagcloud$', 'reanalyseapp.views.makeTagCloud'),						# Get JSON from GET (form) parameters (TAGCLOUD)
	
	
	
	######################################################################################################################################
	# TEMP TRY
	(r'^doc/$', 'reanalyseapp.views.docShow'),
	
	#(r'^account/login/$', 'reanalyseapp.views.home'), # deprecated : loginview is set in settings.py
	(r'^account/logout/$', 'reanalyseapp.views.logoutuser'),
	
	######################################################################################################################################
	
	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',

)