
pyramid_cors
============


Provides small helpers to deal with CORS requests.


CORS view deriver
-----------------

Just use an additional option ```cors=True``` to add a wrapper around your
view. This wrapper adds CORS headers to the response after the view returns.


CORS preflight handler
----------------------

A catch all route and view for ```OPTIONS``` requests with specific CORS headers.
This view responds to CORS preflight requests. The config method ```config.add_cors_preflight_handler``` accepts an optional parameter which should be a callable to render the preflight response.


Configuration
=============

All configuration options are prefixed with ```cors.``` .
The actual keys, are camel cased CORS response header names.

.. code:: ini

    # if this is set to true, Access-Control-Allow-Origin will be set to Origin otherwise '*'
    cors.Access-Control-Allow-Credentials = true
    # allowed headers
    cors.Access-Control-Allow-Headers = Accept,Accept-Language,Content-Language,Content-Type,Cookie,Authorization
    # allowed methods
    #cors.Access-Control-Allow-Methods
    # max age to cache preflight requests
    #cors.Access-Control-Max-Age


Usage
=====

.. code:: python

    config.include('pyramid_cors')

    # install CORS preflight handler
    config.add_cors_preflight_handler()

    # add cors headers to view
    config.add_view(..., cors=True)
