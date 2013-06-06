from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
	
		
	url(r'^$','outside.views.index', name='outside_index'),
	url(r'^index/$','outside.views.index', name='outside_index'),
	url(r'^news/$','outside.views.news', name='outside_news'),
	url(r'^login/$','outside.views.login_view', name='outside_login'),
	url(r'^logout/$','outside.views.logout_view', name='outside_logout'),
	
	url(r'^changePassword/$','outside.views.change_password', name='outside_change_password'),
	url(r'^reinitializePassword/$','outside.views.reinitialize_password', name='outside_reinitialize_password'),
	
	
	
	
	url(r'^contacts/$','outside.views.contacts', name='outside_contacts'),
	url(r'^signup/$','outside.views.signup', name='outside_signup_generic'),
	url(r'^signup/enquete/(?P<enquete_id>\d+)/$','outside.views.signup', name='outside_signup'),
	url(r'^accessRequest/enquete/(?P<enquete_id>\d+)/$','outside.views.access_request', name='outside_access_request'),
	url(r'^accessRequest/$','outside.views.access_request', name='outside_access_request'),
	url(r'^confirm/(?P<token>[a-zA-Z\d]+)/(?P<user_id>\d+)/(?P<action>[a-zA-Z\d]+)$','outside.views.confirm', name='outside_confirm'),
	
	
	url(r'^api/reinitializePassword/$','outside.api.reinitialize_password', name='outside_api_reinitialize_password'),
	url(r'^api/signup/$', 'outside.api.signups', name='outside_api_signups'),
	url(r'^api/signup/(?P<subscriber_id>\d+)/$', 'outside.api.signup', name='outside_api_signup'),	
	url(r'^api/accessRequest/$', 'outside.api.access_request', name='outside_api_access_request'),
	url(r'^api/changePassword/$','outside.api.change_password', name='outside_api_change_password'),
	url(r'^api/captcha/$', 'outside.api.captcha', name='outside_captcha'),
	
	url(r'^editProfile/$', 'outside.views.edit_profile', name='outside_edit_profile'),
	url(r'^createProfile/$', 'outside.views.create_profile', name='outside_create_profile'),
	
	
	url(r'^downloadPage/(?P<enquete_id>\d+)$', 'outside.views.download_page', name='outside_download_page'),
	
	#TEST DOWNLOAD
	url(r'^download/test_dl1/$', 'outside.views.test_dl1', name='outside_test_dl1'),
	url(r'^download/test_dl2/$', 'outside.views.test_dl2', name='outside_test_dl2'),

	
	url(r'^legal-notice/$','outside.views.legal', name='outside_legal'),
	
	url(r'^download/(?P<pin_slug>[a-z0-9-_]+)/$','outside.views.download_view', name='outside_download'),


	url(r'^enquetes/$','outside.views.enquetes', name='outside_enquetes'),
	url(r'^enquete/(?P<enquete_id>\d+)/$','outside.views.enquete', name='outside_enquete'),
	url(r'^enquete/(?P<enquete_id>\d+)/metadata/$','outside.views.enquete_metadata', name='outside_enquete_metadata'),
	url(r'^enquete/(?P<enquete_id>\d+)/download/$','outside.views.enquete_download', name='outside_enquete_download'),

	url(r'^document/(?P<document_id>\d+)/$','outside.views.document', name='outside_enquete_document'),
	url(r'^document/(?P<document_id>\d+)/download/$','outside.views.document_download', name='outside_enquete_document_download'),
	url(r'^document/(?P<document_id>\d+)/embed/$','outside.views.document_embed', name='outside_enquete_document_embed'),

	url(r'^enquiry/(?P<enquete_id>\d+)/$','outside.views.enquiry', name='outside_enquiry'), # foreign key to enquete for model Oustide_Enquiry
	url(r'^enquiries/$','outside.views.enquiries', name='outside_enquiries'),

	url(r'^api/enquete/(?P<enquete_id>\d+)/data/$','outside.api.enquete_data', name='outside_enquete_data'),

	# api
	url(r'^api/enquiry/$', 'outside.api.enquiries', name='outside_api_enquiries'), # get list, post single page
	url(r'^api/enquiry/(?P<enquiry_id>\d+)/$', 'outside.api.enquiry', name='outside_api_enquiry'), 
	
	url(r'^api/enquiry/(?P<enquiry_id>\d+)/(?P<pin_slug>[A-Za-z0-9-]+)/upload/$', 'outside.api.enquiry_upload_pin', name='outside_api_enquiry_upload_pin'),

	url(r'^api/enquiry/(?P<enquiry_slug>[A-Za-z0-9-]+)/pins/$','outside.api.enquiry_pins', name='outside_enquiry_pins'), # foreign key to enquete for model Oustide_Enquiry
	

	url(r'^api/subscriber/$', 'outside.api.subscribers', name='outside_api_subscribers'),
	url(r'^api/subscriber/(?P<subscriber_id>\d+)/$', 'outside.api.subscriber', name='outside_api_subscriber'),
	
	#Send message to admin
	url(r'^api/contacts/$', 'outside.api.contacts', name='outside_api_contacts'),
	
	
	
	url(r'^api/test/$','outside.api.test', name='outside_test'),

	url(r'^(?P<page_slug>[A-Za-z0-9-]+)/$','outside.views.page', name='outside_page'),
	
	url(r'^account/', include('django.contrib.auth.urls')),
	
	#url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': 'static'}),
				

	url(r'^e/(?P<eid>\d+)/d/(?P<did>\d+)/getHtmlContent$', 'outside.views.dGetHtmlContent', name="GetHtmlContent"),	

)
