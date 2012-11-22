from glue.models import Pin, Leaf
from glue.misc import Epoxy
from reanalyse.reanalyseapp.models import Enquete


#
#    API CUSTOM DECORATORS
#    =====================
#
def is_editor(user):
	if user:
		return user.groups.filter(name='CONTENT EDITOR').count() != 0
	return False


#
#    API AUTH VIEWS
#    ==============
#
API_ACCESS_DENIED_URL = "/elipss/panelmanager/api/access-restricted"


def studies( request ):
	return Epoxy( request ).queryset( Enquete.objects.filter() ).json()