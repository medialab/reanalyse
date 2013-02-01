from django.contrib import admin
from outside.models import Enquiry, Subscriber, Message

class MessageAdmin( admin.ModelAdmin ):
    search_fields = ['content']

admin.site.register( Enquiry )
admin.site.register( Subscriber )
admin.site.register( Message, MessageAdmin )
