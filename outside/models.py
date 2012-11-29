from django.db import models
from glue.models import PageAbstract, Pin
from reanalyseapp.models import Enquete

# Create your models here.
# Enquiry does not extends PAGE, which is actually an extension because of all stuff explaied here:
# http://charlesleifer.com/blog/django-patterns-model-inheritance/
# This model inherit an abstract class even it is a very different object.

class Enquiry( PageAbstract ):
	enquete = models.ForeignKey( Enquete )
	pins = models.ManyToManyField( Pin, null=True, blank=True, related_name="enquiry")

	class Meta( PageAbstract.Meta ):
		unique_together = ( "enquete", "language" )
	