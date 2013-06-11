#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from glue.models import PageAbstract, Pin
from reanalyseapp.models import Enquete, Tag
from django.dispatch import receiver
from django.db.models.signals import pre_save

# Create your models here.

class Message( models.Model ):
	date = models.DateField( auto_now=True )
	content = models.CharField( max_length = 1000 )

	def __unicode__(self):
		return "%s : %s" % ( self.date, self.content )

	def json( self ):
		return {
			'id': self.id,
			'content':self.content,
			'date' : self.date.isoformat()
		}


# Enquiry extends PAGEAbstract, cfr
# http://charlesleifer.com/blog/django-patterns-model-inheritance/
# This model inherit an abstract class even it is a very different object.
class Enquiry( PageAbstract ):
	enquete = models.ForeignKey( Enquete, related_name="enquiry" )
	pins = models.ManyToManyField( Pin, null=True, blank=True )
	tags = models.ManyToManyField( Tag, null=True, blank=True )

	class Meta( PageAbstract.Meta ):
		unique_together = ( "enquete", "language" )

	def __unicode__(self):
		return "%s (%s) a.k.a. %s" % (self.slug, self.language, self.title)
	def json( self ):
		return{
			'id': self.id,
			'slug':self.slug,
			'title': self.title,
			'abstract': self.abstract,
			'content': self.content,
			'language': self.language,
			'enquete': self.enquete.id
		}


# class Message( models.Model ):




# a profile for the given user
class Subscriber( models.Model ):

	RESEARCHER = 'RES'
	PHD_STUDENT = 'PHD'
	MS_STUDENT = 'MSS'
	PROFESSOR = 'PRO'

	ENGINEEER = 'ENG'
	POST_DOC = 'POD'
	OTHER = 'OTH'

	STATUS_CHOICES = (
		(RESEARCHER, 'Chercheur Statutaire'),
		(PHD_STUDENT, 'Doctorant'),
		(MS_STUDENT, 'Étudiant - Master'),
		(PROFESSOR, 'Enseignant-Chercheur'),

		(ENGINEEER, 'Ingénieur'),
		(POST_DOC, 'Post Doc'),
		(OTHER, 'Autre'),
	)


	user = models.OneToOneField( User, null=True, blank=True )
	first_name = models.CharField( max_length = 64 ) # longest than standard field
	last_name = models.CharField( max_length = 64 ) # longest than standard field
	email = models.EmailField( unique=False )
	email_confirmed = models.BooleanField( default=False )

	affiliation = models.CharField( max_length = 128 )
	status =     models.CharField( max_length = 3, choices=STATUS_CHOICES )
	accepted_terms = models.BooleanField()
	description = models.TextField() # personal description
	messages = models.ManyToManyField( Message )
	confirmation_code = models.CharField( max_length = 64, null=True, blank=True )


	def __unicode__(self):
		return "%s %s <%s>" % (self.last_name.upper(), self.first_name, self.email )

	def json( self ):
		return {
			'id': self.id,
			'user':self.user,
			'first_name' : self.first_name,
			'last_name':self.last_name,
			'email' : self.email,
			'affiliation' : self.affiliation,
			'accepted_terms' : self.accepted_terms,
			'description' : self.description,

			'user':{'id':self.user.id, 'username':self.user.username} if self.user is not None else None
		}
		

class Confirmation_code( models.Model ):
	code = models.CharField( max_length = 64, null=True, blank=True )
	action = models.CharField( max_length = 64, null=True, blank=True )
	date = models.DateField( auto_now=True )
	activated = models.BooleanField( default=False )


#Store every access request from clients
class AccessRequest(models.Model):
	user = models.ForeignKey( User )
	enquete = models.ForeignKey( Enquete, related_name="access_requests" )
	description = models.TextField()
	date = models.DateTimeField( auto_now_add=True )
	activated = models.BooleanField( default=False )
	
	class Meta:
		unique_together = ('user', 'enquete')
	
	def __unicode__(self):
		return "%s %s" % ( self.enquete.id, self.user.username )





@receiver(pre_save, sender=AccessRequest)
def email_if_access_true(sender, instance, **kwargs):
	try:
		access_request = AccessRequest.objects.get(pk=instance.pk)
	except AccessRequest.DoesNotExist:
		pass # Object is new, so field hasn't technically changed, but you may want to do something else here.
	else:
		if access_request.is_activated == False and instance.is_activated == True: # if is_activated becomes true
			from django.contrib.sites.models import Site
			
			enquete_view = reverse('outside.views.enquete', kwargs={'enquete_id':access_request.enquete.id})
			url = '%s%s' % (settings.REANALYSEURL, enquete_view )
			
			subject, from_email, to = _('Bequali : Research request granted'),"L'equipe Bequali <admin@bequali.fr>", access_request.user.email
			html_content = render_to_string('email/access_request.html', {'action':'access_granted', 'enquete':access_request.enquete,'url':url})
			text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
			
			# create the email, and attach the HTML version as well.
			msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()

