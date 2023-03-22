.. OpenClimate pyClient documentation master file, created by
   sphinx-quickstart on Tue Mar 21 11:04:56 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to OpenClimate Python Client Documentation!
======================================================

OpenClimate Python Client is a Python 3.6+ package that uses the
`OpenClimate API <https://github.com/Open-Earth-Foundation/OpenClimate/blob/develop/api/API.md>`_
to make emissions data and pledges easily accessible.

This is a work in progress, we strongly encourage you to open
`issues <https://github.com/Open-Earth-Foundation/OpenClimate-pyclient/issues>`_
on GitHub and contribute code.

Installation
------------

.. code-block:: bash

   # for latest release
   pip install openclimate

   # for bleeding-edge up-to-date commit
   pip install -e git+https://github.com/Open-Earth-Foundation/OpenClimate-pyclient.git

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   api

.. toctree::
   :maxdepth: 2
   :caption: Analyses:

   notebooks/cumulative_emissions
   notebooks/great_britain_emissions

.. toctree::
   :maxdepth: 2
   :caption: Help and Reference

   contributing
   authors
   GitHub Repo <https://github.com/Open-Earth-Foundation/OpenClimate-pyclient>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`