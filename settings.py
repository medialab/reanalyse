# -*- coding: utf-8 -*-
#####################################################################
# Django settings for reanalyse project.
# pierre.jdlf started working hardly !-!-!-!

import os
DEBUG = True
TEMPLATE_DEBUG = DEBUG

#REANALYSEURL
#REANALYSEPROJECTPATH
#REANALYSEESE_FILES
#REANALYSESAMPLE_STUDIES_FILES
#ALLOWED_INCLUDE_ROOTS = (REANALYSEESE_FILES)
#READB_NAME
#READB_USER
#READB_PASS
#STAFF_EMAIL
#EMAIL_HOST
#EMAIL_PORT
# .. are defined in :
from settingsprivate import * 


REANALYSELOGPATH 			= REANALYSEPROJECTPATH + 'logs/' 					# needs to be accessible by www-data
REANALYSELOGDJANGO				= REANALYSELOGPATH + 'reanalyse_django.log'
REANALYSELOGSOLR				= REANALYSELOGPATH + 'reanalyse_solr.log'
REANALYSEUPLOADPATH 		= REANALYSEPROJECTPATH + 'upload/'					# needs to be accessible by www-data
REANALYSEDOWNLOADPATH 		= REANALYSEPROJECTPATH + 'download/'				# needs to be accessible by www-data
REANALYSESITECONTENTPATH 	= REANALYSEPROJECTPATH + 'templates/content/'

BASE_URL = '/'+ROOT_DIRECTORY_NAME+'/'
LOGIN_REDIRECT_URL = BASE_URL
LOGIN_URL = BASE_URL+'?p=access&q=login'

######## SOLR
SOLR_JARFOLDER = REANALYSEPROJECTPATH + "solr/"
SOLR_JARNAME = "startreanalysesolr.jar"
# SOLR_PORT = was 8983 by default, defined in solr/et/jetty.xml
# from now on, we launch solr (in views.py) with -Djetty.port=SOLR_PORT to allow custom PORT
# (avoids conflicts between multiple reanalyse instances)
SOLR_PORT = 8986

######## HAYSTACK
# Required and specific to where you place the file.
HAYSTACK_SITECONF = 'reanalyse.search_sites'

# Optional Haystack settings.
# See `docs/settings.rst` for a complete list.
HAYSTACK_INCLUDE_SPELLING = True
# For Solr:
HAYSTACK_SEARCH_ENGINE = 'solr'
HAYSTACK_SOLR_URL = 'http://localhost:'+str(SOLR_PORT)+'/solr/'
HAYSTACK_SOLR_TIMEOUT = 60 * 5

# For admin page:
SOLR_URL = REANALYSEURL+":"+str(SOLR_PORT)


ADMINS = (
 	('pierre', STAFF_EMAIL),
)

MANAGERS = ADMINS

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2', 	# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': READB_NAME,  					# Or path to database file if using sqlite3.
		'USER': READB_USER,  					# Not used with sqlite3.
		'PASSWORD': READB_PASS,  				# Not used with sqlite3.
		'HOST': '',  					# Set to empty string for localhost. Not used with sqlite3.
		'PORT': '',  					# Set to empty string for default. Not used with sqlite3.
	},
	# TODO, maybe. 'glue': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': REANALYSEPROJECTPATH + "sqlite/glue.db"
    #}
# 	'default': {
# 		'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
# 		'NAME': '',  					# Or path to database file if using sqlite3.
# 		'USER': '',  					# Not used with sqlite3.
# 		'PASSWORD': '',  				# Not used with sqlite3.
# 		'HOST': '',  					# Set to empty string for localhost. Not used with sqlite3.
# 		'PORT': '',  					# Set to empty string for default. Not used with sqlite3.
# 	},
#	'enquetes': {
#		'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#		'NAME': '',  					# Or path to database file if using sqlite3.
#		'USER': '',  					# Not used with sqlite3.
#		'PASSWORD': '',  				# Not used with sqlite3.
#		'HOST': '',  					# Set to empty string for localhost. Not used with sqlite3.
#		'PORT': '',  					# Set to empty string for default. Not used with sqlite3.
#	}
}

# Added to allow multiple database routing
#DATABASE_ROUTERS = ['reanalyseapp.databases.ReanalyseRouter',]
# DATABASE_ROUTERS = ['glue.router.GlueRouter']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGES = (
	('en', 'English'),
	('fr', 'Français'),
)

LANGUAGE_CODE = 'en'

LOCALE_PATHS = (
	REANALYSEPROJECTPATH+'/locale',
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = REANALYSEPROJECTPATH +'media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = BASE_URL+'media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = REANALYSEPROJECTPATH +'static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = BASE_URL+'static/'

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
#ENQUETE_FILES = os.path.join(PROJECT_PATH, 'files/')

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = BASE_URL+'media/admin/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Additional locations of static files
STATICFILES_DIRS = (
	# Put strings here, like "/home/html/static" or "C:/www/django/static".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#	'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
# 	'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'reanalyse.urls'

TEMPLATE_DIRS = (
	os.path.join(REANALYSEPROJECTPATH, 'templates'),
	os.path.join(REANALYSEPROJECTPATH, 'outside/templates')
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	# Uncomment the next line to enable the admin:
	'django.contrib.admin',
	'reanalyseapp',
	'django_tables2',
	'haystack',
	'glue', # content management via json api
	'outside', # currently there is no model
	# Uncomment the next line to enable admin documentation:
	# 'django.contrib.admindocs',
)

# Needed by django-tables2
TEMPLATE_CONTEXT_PROCESSORS = (
	"django.contrib.auth.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
	"django.core.context_processors.static",
	"django.contrib.messages.context_processors.messages",
	"django.core.context_processors.request",
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'verbose': {
			#'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
			'format': '%(levelname)s %(asctime)s | %(module)s | %(message)s'
		},
		'simple': {
			'format': '%(levelname)s %(message)s'
		},
	},
	'handlers': {
		'null': {
			'level':'DEBUG',
			'class':'django.utils.log.NullHandler',
		},
		'console':{
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'simple'
		},
		'log_file':{
			'level': 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': REANALYSELOGDJANGO ,
			'maxBytes': '16777216', # 16megabytes
			'formatter': 'verbose'
		},
		'glue_log_file':{

			'level': 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': REANALYSELOGPATH + 'glue.log',
			'maxBytes': '16777216', # 16megabytes
			'formatter': 'verbose'
		},
		'mail_admins': {
			'level': 'ERROR',
			'class': 'django.utils.log.AdminEmailHandler',
			'include_html': True,
		}
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True,
		},
		'apps': { # I keep all my apps here, but you can also add them one by one
			'handlers': ['log_file'],
			'level': 'INFO',
			'propagate': True,
		},
		'glue':{ # glue content management app
			'handlers': ['glue_log_file'],
			'level': 'INFO',
			'propagate': True
		}
	}
}


#
#
#    Outside specific settings
#    =========================
#
OUTSIDE_SITE_NAME = "app"
OUTSIDE_THEME = "app"
OUTSIDE_TEMPLATE_DIR = "hub"
