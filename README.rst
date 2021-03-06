==============
Nameko Webargs
==============

Nameko_ integration with Webargs_.

.. image:: https://img.shields.io/pypi/v/nameko_webargs.svg
        :target: https://pypi.python.org/pypi/nameko_webargs

.. image:: https://img.shields.io/travis/tyler46/nameko_webargs.svg
        :target: https://travis-ci.org/tyler46/nameko_webargs

.. image:: https://readthedocs.org/projects/nameko-webargs/badge/?version=latest
        :target: https://nameko-webargs.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/tyler46/nameko_webargs/shield.svg
     :target: https://pyup.io/repos/github/tyler46/nameko_webargs/
     :alt: Updates

Webargs_ is a Python library for parsing and validating HTTP requests arguments.
nameko-webargs allows you to use it for Nameko_ http entrypoints.


Installing
-----------

::
   
   pip install -U nameko-webargs


nameko-webargs supports Python >= 3.5


Usage
------

A real-world nameko example can be found at `examples` folder.
First create a `.env` file by copying `env.example` and then run the following command
from project root directory:

.. code-block:: bash

   env $(cat .env | grep "^[^#;]" | xargs) ./run.sh


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.
Inspired by webargs-sanic_ package.

.. _Nameko: https://www.nameko.io
.. _Webargs: https://github.com/sloria/webargs
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _webargs-sanic: https://github.com/EndurantDevs/webargs-sanic


