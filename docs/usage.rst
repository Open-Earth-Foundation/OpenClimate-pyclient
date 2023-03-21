Usage
=====

.. _installation:

Installation
------------

To use the OpenClimate pyClient, first install it using pip:

.. code-block:: console

   pip install openclimate

Retrieving Emissions
----------------

Here is an example of retrieving Canadian emissions

>>> from openclimate import Client
>>> client = Client()
>>> df = client.emissions(actor_id="CA")
