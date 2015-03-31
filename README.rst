arbitrator
==========

Negotiates and handles Content-Type / Accept header negotiation for you.

|Version| |Downloads| |Status| |License|

Overview
---------

Too often we roll our own serialization middleware based on Content-Type
or Accept HTTP headers, and too often it's done incorrectly.  This library
aims to provide a very simple interface for handling this task for you
so you can spend your time elsewhere.

Installing
----------

.. code:: bash

    pip install arbitrator

Examples
--------

.. code:: python

    >>> import json
    >>> import msgpack
    >>> from tornado import web
    >>> class MyHandler(arbitrator.MediaTypeMixn, web.RequestHandler):
    ...
    ...     def initalize(self):
    ...         media_types = {
    ...             'application/json': json,
    ...             'application/msgpack': msgpack,
    ...             'application/x-msgpack': msgpack
    ...         }
    ...         super(MyHandler, self).initalize(supported_media_types=media_types)
    ...
    ...     def get(self, account_id):
    ...         payload = self.load_payload(
    ...             self.request.headers['Content-Type'],
    ...             self.request.content,
    ...         )
    ...         # ... do stuff with the payload dictionary
    ...         content_type, stringified = self.dump_payload(
    ...             self.request.headers['Accept'],
    ...             payload,
    ...         )
    ...         self.set_status(200)
    ...         self.set_header('Content-Type', content_type)
    ...         self.finish(stringified)


Contributing
------------

If you want to help make this project better you are officially an awesome
person.

Pull requests or Github issues are always welcome.  If you want to contribute
a patch please do the following.

1. Fork this repo and create a new branch
2. Do work
3. Add tests for your work (Mandatory)
4. Submit a pull request
5. Wait for Coveralls and Travis-CI to run through your PR
6. I'll review it and merge it

As a note, code without sufficient tests will not be merged.

General Info
------------

+---------------+-------------------------------------------------+
| Source        | https://github.com/djt5019/arbitrator           |
+---------------+-------------------------------------------------+
| Status        | https://travis-ci.org/djt5019/arbitrator        |
+---------------+-------------------------------------------------+
| Download      | https://pypi.python.org/pypi/arbitrator         |
+---------------+-------------------------------------------------+
| Documentation | http://arbitrator.readthedocs.org/en/latest     |
+---------------+-------------------------------------------------+
| Issues        | https://github.com/djt5019/arbitrator           |
+---------------+-------------------------------------------------+

.. |Version| image:: https://pypip.in/version/arbitrator/badge.svg
   :target: https://pypi.python.org/pypi/arbitrator

.. |Downloads| image:: https://pypip.in/d/arbitrator/badge.svg
   :target: https://pypi.python.org/pypi/arbitrator

.. |Status| image:: https://travis-ci.org/djt5019/arbitrator.svg
   :target: https://travis-ci.org/djt5019/arbitrator

.. |License| image:: https://pypip.in/license/arbitrator/badge.svg
   :target: https://arbitrator.readthedocs.org/
