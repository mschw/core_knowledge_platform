*********
Overview
*********

Every interaction with the web service should be conducted through HTTP.
To allow the web service to respond with the appropriate data format HTTP-headers are used:
all queries to the web service *must* set the following headers:

ACCEPT:
    tells the web service which format to return.
CONTENT-TYPE:
    tells the web service which format was sent.

Currently *most* resources of the web service allow only one format: ``application/xml``.

.. _data_retrieval:

===============
Data retrieval
===============

To obtain data from the service issue a GET request to one of the following addresses:

``authors/``
    Retrieve a list of all authors.
``authors/{id}``
    Retrieve all information for a specific authors.
``comment/``
    Retrieve a list of all comments.
``comment/{id}``
    Retrieve a specific comment.
``comment/publication/{id}``
    Retrieve a list of all comments for a certain publication.
``esteem/{id}``
    Retrieve a specific esteem object.
``keyword/``
    Retrieve a list of all keywords.
``keyword/{id}``
    Retrieve a specific keyword.
``keyword/related/{id}``
    Retrieve a list of keywords related to the keyword with the provided id.
``papergroup/``
    Retrieve a list of papergroups.
``peerreviewtemplate/``
    Retrieve a list of available peer review templates.
``peerreviewtemplate/{id}``
    Retrieve a concrete peer review template.
``peerreview/publication/{id}``
    Retrieve all peer review for a specific publication.
``publication/``
    Retrieve a list of all publications.
``publication/{id}``
    Retrieve all information for a specific publication.
``publication/related/{id}``
    Retrieve a list of publications probably related to the one with the
    provided id.
``rating/``
    Retrieve a list of all ratings.
``rating/{id}``
    Retrieve a specific rating.
``referencematerial/{id}``
    Retrieve a specific reference material.
``researcharea/``
    Retrieve a list of all research areas.
``researcharea/{id}``
    Retrieve a specific research area.
``tag/``
    Retrieve a list of all tags.
``tag/{id}``
    Retrieve a specific tag.
``tag/related/{id}``
    Retrieve a list of tags probably related to the one with the provided id.
``user/``
    Retrieve a list of all registered users in the system.
``user/{id}``
    Retrieve a specific user.
``user/related/publication/{id}``
    Retrieve users that might be related to a given publication.
``user/login/``
    Log a user in.
``user/logout/``
    Log a user out.
``vote/``
    Retrieve a list of all votes.
``vote/{id}``
    Retrieve a specific vote object.

These resources can be accessed without being logged in.

.. note:: The following resources require a user to be logged in and maybe have special privileges.

``papergroup/{id}``
    Retrieve a specific papergroup.
.. note:: only available to editors and referees.
``peerreview/{id}``
    Retrieve a concrete peer review.
.. note:: during the review process only available to editors and the referee that added the review.

---------------------------
Using CiteSeerX Integration
---------------------------

It is possible to retrieve more information from CiteSeerX if the correct *DOI*
is set in a publication object.

To perform this retrieval issue a ``GET`` request for a specific publication
with the following url:

``publication/{id}/meta=True``

.. warning:: Using the CiteSeerX bridge is very slow due to the CiteSeerX servers response time.


---------------
Login & Logout
---------------

If a resource requires a login the client can login via a ``POST`` request to
the following address:
``user/login/``

To logout from the system a simple ``GET`` request to ``/user/logout/`` is
enough.

----------
Searching
----------

Searching authors and publications is possible:

^^^^^^^^^^^^^
Publications
^^^^^^^^^^^^^

Just append key-value-pairs to the url according to the following schema:

``/publication/{name=value&name2=value2}/author/{name=value&...}/keyword/{..}``

Sub-searches will be executed via *OR*:
all publications with name = value *OR* name2=value2

If you want to perform *AND* searches provide the following parameter:
``searchtype=and``

The results of the sub-searches will be concatenated using the AND operator:
all publications where AND where the authors is AND where the keyword is

^^^^^^^^
Authors
^^^^^^^^

Do not forget that in this case the search uses a query string.

``/authors/?{name=value}``

===============
Data Insertion
===============

When inserting data it is important to distinguish between an initial insertion
of a modification of data:

.. _initial_insert:

---------------
Initial insert
---------------

The initial insertion is performed via ``POST`` requests to the root urls of
a resource.

To insert a publication ``POST`` the appropriate data to:

``/publication/``

To insert an author ``POST`` the appropriate data to:

``/author/``

The other urls to post to are as follows:

``referencematerial/``

``comment/``

``keyword/``

``papergroup/``

``peerreviewtemplate/``

``rating/``

``researcharea/``

``tag/``

``user/``

``vote/``

This will insert a new object into the database and return the location the
object can be retrieved from.

--------------
Updating data
--------------

To update data the ``PUT`` request is used - it will be send to the specific
resource url.

To update an existing publication the ``PUT`` request needs to be sent to:

``/publication/{id}``

The urls for the other resources follow the same schema - see initial_insert_

-------------
Deleting data
-------------

To delete data the ``DELETE`` request is used - it will be sent to the same
resource urls as the ``PUT`` request.
