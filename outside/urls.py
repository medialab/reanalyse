from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
	url(r'^$','outside.views.index', name='outside_index'),
	url(r'^login/$','outside.views.login_view', name='outside_login'),
	url(r'^logout/$','outside.views.logout_view', name='outside_logout'),
	
	url(r'^enquetes/$','outside.views.enquetes', name='outside_enquetes'),
	url(r'^enquete/(?P<enquete_id>\d+)/$','outside.views.enquete', name='outside_enquete'),
	url(r'^enquiry/(?P<enquete_id>\d+)/$','outside.views.enquiry', name='outside_enquiry'), # foreign key to enquete for model Oustide_Enquiry

	url(r'^api/enquete/(?P<enquete_id>\d+)/data/$','outside.api.enquete_data', name='outside_enquete_data'),

	# api
	url(r'^api/enquiry/$', 'outside.api.enquiries', name='outside_api_enquiries'), # get list, post single page
	url(r'^api/enquiry/(?P<enquiry_id>\d+)/$', 'outside.api.enquiry', name='outside_api_enquiry'), 
	url(r'^api/enquiry/(?P<enquiry_id>\d+)/upload$', 'outside.api.enquiry_upload_pin', name='outside_api_enquiry_upload_pin'),

	url(r'^(?P<page_slug>[a-z0-9-]+)/$','outside.views.page', name='outside_page'),



)