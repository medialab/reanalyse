# -*- coding: utf-8 -*-
############################################################
#from django.db import models
#from django.conf import settings

# Testing multiple database routing..

"""
############################################################
class ReanalyseRouter(object):
	"""A router to control all database operations on models in
	the myapp application"""
	def db_for_read(self, model, **hints):
		if hasattr(model,'connection_name'):
			return model.connection_name
		if hasattr(model,'pomme'):
			return model.pomme.connection_name
#		"Point all operations on myapp models to 'other'"
#		if model._meta.app_label == 'reanalyse':
#			return 'enquetes'
		return None
		
	def db_for_write(self, model, **hints):
		"Point all operations on myapp models to 'other'"
		if hasattr(model,'connection_name'):
			return model.connection_name
		if hasattr(model,'pomme'):
			instance = hints.get('instance')
			return instance.pomme.connection_name
#		if model._meta.app_label == 'reanalyse':
#			return 'enquetes'
		return None
		
	def allow_relation(self, obj1, obj2, **hints):
		"Allow any relation if a model in myapp is involved"
		if hasattr(model,'connection_name'):
			return model.connection_name
		if hasattr(model,'pomme'):
			return model.pomme.connection_name
#		if obj1._meta.app_label == 'reanalyse' or obj2._meta.app_label == 'reanalyse':
#			return True
		return None
		
	def allow_syncdb(self, db, model):
		"Make sure the myapp app only appears on the 'other' db"
		if hasattr(model,'connection_name'):
			return model.connection_name == db
		if hasattr(model,'pomme'):
			return True
#		if db == 'enquetes':
#			return model._meta.app_label == 'reanalyse'
#		elif model._meta.app_label == 'reanalyse':
#			return False
		return None
############################################################
"""