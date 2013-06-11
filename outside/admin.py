from django.contrib import admin
from outside.models import Enquiry, Subscriber, Message, AccessRequest

class MessageAdmin( admin.ModelAdmin ):
    search_fields = ['content']
    
class AccessRequestAdmin( admin.ModelAdmin ):
   search_fields = ['user__username']
   list_display = ('user', 'enquete', 'date', 'activated')
    
admin.site.register(AccessRequest, AccessRequestAdmin )

admin.site.register( Enquiry )
admin.site.register( Subscriber )
admin.site.register( Message, MessageAdmin )
