# a database router for gluish content.
# activate it on settings.py
# DATABASE_ROUTERS = ['path.to.glue.GlueRouter']
class GlueRouter(object):
	def db_for_read(self, model, **hints):
		if model._meta.app_label == 'glue':
			return 'glue'
		return None

	def db_for_write(self, model, **hints):
		if model._meta.app_label == 'glue':
			return 'glue'
		return None

	def allow_relation(self, obj1, obj2, **hints):
		if obj1._meta.app_label == 'glue' or \
			obj2._meta.app_label == 'glue':
			return True
		return None

	def allow_syncdb(self, db, model):
		if db == 'glue':
			return model._meta.app_label == 'glue'
		elif model._meta.app_label == 'glue':
			return False
		return None