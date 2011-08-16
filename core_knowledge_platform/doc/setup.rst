=================
Setup the service
=================

Follow the following steps to setup the service on Ubuntu 11.04:

Installation on Ubuntu 11.04:

1. Install Apache:
------------------

``sudo apt-get install apache2 apache2-dev``

2. Install Python-Dev packages:
-------------------------------

``sudo apt-get install python-dev``

3. Download and install mod_wsgi:
---------------------------------

http://code.google.com/p/modwsgi/

- Just follow the instructions in the wiki to install mod_wsgi:
``./configure``

``make``

``sudo make install``

4. Download and install the MySQL server:
-----------------------------------------

``sudo apt-get install mysql-server-5.1``

Setup necessary users for the application.

5. Setup easy_install and PIP for python:
-----------------------------------------

A lot easier to install python packages when these tools are installed:

http://pypi.python.org/pypi/setuptools

Make sure to download the right one for the python version (Ubuntu 10.04 comes with Python 2.6):

``sudo sh setuptools-<version>.egg``

Install PIP with easy_install:

``sudo easy_install pip``

6. Install the requirements of the system:
------------------------------------------

First install the dev packages for lxml (needed for pyoai):

``sudo apt-get install libxml-devl libxslt1-dev``

``sudo pip install <package>==<version>`` with the following packages:

``Django==1.3``

``MySQL-python==1.2.3``

``South==0.7.3``

``pyoai==2.4.4``

``pyparsing==1.5.6``

7. Setup mod_wsgi according to the django docs:
-----------------------------------------------

https://docs.djangoproject.com/en/dev/howto/deployment/modwsgi/

8. Django database user
-----------------------

Create a new user for the MySQL database and change the appropriate values in
the ``settings.py`` file.

9. Adjust paths
---------------

Adjust the template paths in the settings.py file to point to the directory of the templates.

Setup the staticfiles module and the web server to serve static files:

https://docs.djangoproject.com/en/dev/howto/static-files/

