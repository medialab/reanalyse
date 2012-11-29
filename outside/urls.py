from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
	url(r'^$','outside.views.index', name='outside_index'),
	url(r'^login/$','outside.views.login_view', name='outside_login'),
	url(r'^logout/$','outside.views.logout_view', name='outside_logout'),
	
	url(r'^enquetes/$','outside.views.enquetes', name='outside_enquetes'),
	url(r'^enquete/(?P<enquete_id>\d+)/$','outside.views.enquete', name='outside_enquete'),
	url(r'^enquiry/(?P<enquete_id>\d+)/$','outside.views.enquiry', name='outside_enquiry'), # foreign key to enquete for model Oustide_Enquiry

	url(r'^enquete/(?P<enquete_id>\d+)/data/$','outside.api.enquete_data', name='outside_enquete_data'),

	url(r'^(?P<page_slug>[a-z0-9-]+)/$','outside.views.page', name='outside_page'),
)