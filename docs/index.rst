Arbitrator
==========

Tornado mix-in to simplify HTTP Content Type negotation and serilization.

|Version| |Downloads| |Status| |Coverage| |License|

Installation
------------
``Arbitrator`` is available on the
`Python Package Index <https://pypi.python.org/pypi/Arbitrator>`_
and can be installed via ``pip`` or ``easy_install``:

.. code:: bash

  pip install arbitrator

Requirements
------------

* ``tornado``

Simple Example
--------------

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

API Documentation
-----------------
.. toctree::
   :maxdepth: 2

   api
   history

Version History
---------------
See :doc:`history`

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

Issues
------
Please report any issues to the Github project at `https://github.com/djt5019/arbitrator/issues <https://github.com/djt5019/arbitrator/issues>`_

Source
------
``Arbitrator`` source is available on Github at `https://github.com/djt5019/arbitrator <https://github.com/djt5019/arbitrator>`_

License
-------
``Arbitrator`` is released under the `MIT license <https://github.com/djt5019/arbitrator/blob/master/LICENSE>`_.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |Version| image:: https://badge.fury.io/py/Arbitrator.svg?
   :target: http://badge.fury.io/py/Arbitrator

.. |Status| image:: https://travis-ci.org/djt5019/arbitrator.svg?branch=master
   :target: https://travis-ci.org/djt5019/arbitrator

.. |Coverage| image:: https://img.shields.io/coveralls/djt5019/Arbitrator.svg?
   :target: https://coveralls.io/r/djt5019/arbitrator

.. |Downloads| image:: https://pypip.in/d/arbitrator/badge.svg?
   :target: https://pypi.python.org/pypi/arbitrator

.. |License| image:: https://pypip.in/license/arbitrator/badge.svg?
   :target: https://arbitrator.readthedocs.org
