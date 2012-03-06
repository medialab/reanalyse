Reanalyse
=================================
## absent directories/files
* ./settingsprivate.py
* ./download/
* ./logs/
* ./solrdataindex/
* ./upload/

## Django Internationalization how-to
### within template
{% load i18n %}

{% comment %}Translators: Login page title{% endcomment %}

{% trans 'Login Page' %}
### within view
from django.utils.translation import ugettext as _

mystring = _('congratulations')
### translation
* > sudo django-admin.py makemessages --ignore ./upload/ -a
* translate file /locale/fr/LC_MESSAGES/django.po
* > django-admin.py compilemessages

## Solr default conf, except for
* ./solr/solr/conf/schema.xml defining how models are indexed
* ./solr/solr/conf/solrconfig.xml
 * datadir = ./../solrdataindex/ (temp files)
 * < maxFieldLength >2147483647< /maxFieldLength > (in case of big files)
* ./solr/etc/jetty.xml : if you want to change webserver port
* ./solr/solr/conf/*_fr.txt : stopwords, synonyms, protwords, etc...

## Normalisation
![Alt text](http://jiminy.medialab.sciences-po.fr/reanalyse/media/images/content_overview.png "Normalisation")

## Django Models
![Alt text](http://jiminy.medialab.sciences-po.fr/reanalyse/media/images/content_models.png "Django Models")