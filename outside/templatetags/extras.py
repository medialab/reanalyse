from django import template
from datetime import datetime
import time
import hashlib

register = template.Library()

@register.filter
def gravatar( email ):
	
	host = "http://www.gravatar.com/avatar/"
	
	hash = hashlib.md5( email ).hexdigest()
   	
	return host + hash + "?s=32&d=retro"

  
@register.filter
def fromnow( date_a ):    
	delta = datetime.now() - date_a
	
	weeks = delta.days / 7
	days = delta.days % 7
	
	if weeks > 1:
		if days == 0:
			return str( weeks ) + ' weeks'
		if days == 1:
			return str( weeks ) + ' weeks, 1 day'
		return str( weeks ) + ' weeks, ' + str( days ) + ' days'
	
	hours	= delta.seconds / 3600 
	
	if days > 1:
		if hours == 0:
			return "exactly " + str( days ) + ' ago'
		if hours == 1:
			
			return str( days ) + ' days ' if days > 1 else '1 day ago'
	
	
	return "today, " + str( hours ) + " hours ago" if hours > 1 else 'less than 1 hour ago'


@register.filter
def age( date_a ):    
	today = datetime.now()
	if today.month > date_a.month or ( today.month == date_a.month and today.day >= date_a.day ):
		return today.year - date_a.year
	return today.year - date_a.year - 1


@register.filter
def delta( date_a, date_b ):

	# return days, and/or weeks
	delta = date_b - date_a
	weeks = delta.days / 7
	days = delta.days % 7
	
	if weeks > 1:
		if days == 0:
			return str( weeks ) + ' weeks'
		if days == 1:
			return str( weeks ) + ' weeks, 1 day'
		return str( weeks ) + ' weeks, ' + str( days ) + ' days'
	
	return str( days ) + ' days' if days > 1 else '1 day'

#TODO untested
#@register.filter
#def delta_datetime(datetime_a, datetime_b):
#	date_format = "%Y-%m-%dT%H:%M:%S"
#	nb_sec_min = 60
#
#	dta = datetime.strptime(date_format,datetime_a)
#	dtb = datetime.strptime(date_format,datetime_b)
#
#	nb_min=(dtb-dta).total_seconds() / nb_sec_min#
#	nb_h = nb_min / nb_sec_min
#
#	return str(nb_h) + 'h' + str(nb_min)

@register.filter
def percent( ratio ):
	# transform float values in range 0.0 - 1.0 to percentages
	return str( round( ratio * 1000 ) / 10 ) + "%"
