Reanalyse
=================================
## absent directories/files


## Installation RŽanalyse :
### installation de git
$ sudo aptitude install git

### installation du code source
$ cd /var/opt
$ mkdir reanalyse
$ git clone https://github.com/medialab/reanalyse.git reanalyse

### installation de java pour SOLR
$ sudo aptitute install default-jre


### installation du mode xsendfile https://tn123.org/mod_xsendfile/
$ sudo aptitude install apache2-threaded-dev
$ apxs2 -iac mod_xsendfile.c

### Installation de haystack
$ sudo pip install django-haystack

### installation de django_tables2 (not used anymore ?)
$ sudo pip install django-tables2

### installation de lxml
$ sudo aptitude install python-dev
$ sudo aptitude install python-lxml

### installation de pythonsolr
$ hg clone https://bitbucket.org/cogtree/python-solr
$ sudo pyton python-solr/setup.py install

### apache > django conf
$ vi /apache/reanalyse.conf
$ vi /apache/django.wsgi

### Ždition des paramtres de l'application
absent directories:

* ./settingsprivate.py
* ./download/
* ./logs/
* ./solrdataindex/
* ./upload/

$ vi settingsprivate.py
$ mkdir logs upload download solrdataindex
$ sudo chown -R www-data:www-data solr log upload download

### configuration de l'authentification dans Postgresql
$ sudo vi /etc/postgresql/8.4/main/pg_hba.conf

remplacer ident par md5 pour local dŽsactiver les autres host

### vŽrifier le port 5432 dans la conf postgresql
$ sudo vi /etc/postgresql/8.4/main/postgresql.conf

### crŽer la base dans postgresql et le user de la base :
$ sudo su - postgres
$ psql
$ postgres=# create user reanalyse with password 'password';
$ postgres=# CREATE DATABASE reanalyse WITH OWNER=reanalyse;
$ postgres=# grant all privileges on database reanalyse to reanalyse;
$ postgres=# \q

### peupler la base de donnŽe
$ python manage.py syncdb

### activation du site RŽanalyse dans apache
$ sudo ln -s /var/opt/reanalyse/apache/reanalyse.conf /etc/apache2/sites-available/
$ sudo a2ensite reanalyse.conf
$ sudo service apache2 reload


## Static Html Pages
files are stored within the template/content dir

## django Internationalization how-to
### within template
{% load i18n %}

{% comment %}Translators: Login page title{% endcomment %}

{% trans 'Login Page' %}
### within view
from django.utils.translation import ugettext as _

mystring = _('congratulations')

### translation
required: sudo apt-get install gettext
from django project root, do:
* > sudo django-admin.py makemessages --ignore ./upload --ignore ./media --ignore ./solr -a
* manually translate file /locale/fr/LC_MESSAGES/django.po
* > django-admin.py compilemessages

## solr is based on the default conf (from example), except for
* ./solr/solr/conf/schema.xml defining how models are indexed
* ./solr/solr/conf/solrconfig.xml
 * datadir = ./../solrdataindex/ (temp files)
 * < maxFieldLength >2147483647< /maxFieldLength > (in case of big files)
* ./solr/etc/jetty.xml : if you want to change webserver port
* ./solr/solr/conf/*_fr.txt : stopwords, synonyms, protwords, etc...

## normalisation
![Alt text](http://jiminy.medialab.sciences-po.fr/reanalyse/media/images/content_overview.png "Normalisation")

## django models & views
![Alt text](http://jiminy.medialab.sciences-po.fr/reanalyse/media/images/content_models.png "Django Models")