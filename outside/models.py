#!/usr/bin/python
# -*- coding: utf8 -*-

from django.db import models
from django.contrib.auth.models import User
from glue.models import PageAbstract, Pin
from reanalyseapp.models import Enquete, Tag

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
	email = models.EmailField( unique=True )
	affiliation = models.CharField( max_length = 128 )
	status =     models.CharField( max_length = 3, choices=STATUS_CHOICES )
	accepted_terms = models.BooleanField()
	description = models.TextField() # personal description
	messages = models.ManyToManyField( Message )
	
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
