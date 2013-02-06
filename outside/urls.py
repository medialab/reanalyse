from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
	url(r'^$','outside.views.index', name='outside_index'),
	url(r'^index/$','outside.views.index', name='outside_index'),
	url(r'^news/$','outside.views.news', name='outside_news'),
	url(r'^login/$','outside.views.login_view', name='outside_login'),
	url(r'^logout/$','outside.views.logout_view', name='outside_logout'),
	url(r'^contacts/$','outside.views.contacts', name='outside_contacts'),
	url(r'^signup/$','outside.views.signup', name='outside_signup'),
	url(r'^legal-notice/$','outside.views.legal', name='outside_legal'),
	
	url(r'^download/(?P<pin_slug>[a-z0-9-_]+)/$','outside.views.download_view', name='outside_download'),


	url(r'^enquetes/$','outside.views.enquetes', name='outside_enquetes'),
	url(r'^enquete/(?P<enquete_id>\d+)/$','outside.views.enquete', name='outside_enquete'),
	url(r'^enquete/(?P<enquete_id>\d+)/metadata$','outside.views.enquete_metadata', name='outside_enquete_metadata'),

	url(r'^enquiry/(?P<enquete_id>\d+)/$','outside.views.enquiry', name='outside_enquiry'), # foreign key to enquete for model Oustide_Enquiry
	url(r'^enquiries/$','outside.views.enquiries', name='outside_enquiries'),

	url(r'^api/enquete/(?P<enquete_id>\d+)/data/$','outside.api.enquete_data', name='outside_enquete_data'),

	# api
	url(r'^api/enquiry/$', 'outside.api.enquiries', name='outside_api_enquiries'), # get list, post single page
	url(r'^api/enquiry/(?P<enquiry_id>\d+)/$', 'outside.api.enquiry', name='outside_api_enquiry'), 
	
	url(r'^api/enquiry/(?P<enquiry_id>\d+)/(?P<pin_slug>[A-Za-z0-9-]+)/upload/$', 'outside.api.enquiry_upload_pin', name='outside_api_enquiry_upload_pin'),

	url(r'^api/enquiry/(?P<enquiry_slug>[A-Za-z0-9-]+)/pins/$','outside.api.enquiry_pins', name='outside_enquiry_pins'), # foreign key to enquete for model Oustide_Enquiry
	
	url(r'^api/signup/$', 'outside.api.signups', name='outside_api_signups'),
	url(r'^api/signup/(?P<subscriber_id>\d+)/$', 'outside.api.signup', name='outside_api_signup'),
	

	url(r'^api/subscriber/$', 'outside.api.subscribers', name='outside_api_subscribers'),
	url(r'^api/subscriber/(?P<subscriber_id>\d+)/$', 'outside.api.subscriber', name='outside_api_subscriber'),
	
	

	url(r'^(?P<page_slug>[A-Za-z0-9-]+)/$','outside.views.page', name='outside_page'),



)