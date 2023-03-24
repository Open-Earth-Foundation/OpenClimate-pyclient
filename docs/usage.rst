Quickstart Guide
====================================================

Installation
----------------------------------------------------

Install `openclimate` using `pip`.

.. code-block:: bash

   # for latest release
   pip install openclimate

   # for bleeding-edge up-to-date commit
   pip install -e git+https://github.com/Open-Earth-Foundation/OpenClimate-pyclient.git

Once installed, import the package and create a `Client()` object.

.. code-block:: python

    from openclimate import Client
    client = Client()

    # if using jupyter or iPython
    client.jupyter

.. note::
    You need to run `client.jupyter` for the client package
    to work properly in Jupyter or iPython.


Emissions
----------------------------------------------------
Retrieve all emissions data for a single actor. Here I am retrieving emissions data for Canada

.. code-block:: python

    df = client.emissions(actor_id='CA')



Retrieve all emissions data for a list of actors. Here I am retrieving emission data for the United States, Canada, and Great Britain.

.. code-block:: python

        df = client.emissions(actor_id=['US','CA','GB'])


Return the different datasets available for a particular actor:

.. code-block:: python

    df = client.emissions_datasets(actor_id='US')


Only select data for a particular dataset

.. code-block:: python

    df = client.emissions_datasets(actor_id='US', datasource_id='GCB2022:national_fossil_emissions:v1.0')


Targets
----------------------------------------------------
Retrieve emissions targets for a particule actor

.. code-block:: python

    df = client.targets(actor_id='US')


Population
----------------------------------------------------
Retrieve population data.

.. code-block:: python

    df = client.population(actor_id=['US','CA','GB'])


GDP
----------------------------------------------------
Retrieve GDP data.

.. code-block:: python

    df = client.gdp(actor_id=['US','CA','GB'])


Searching for codes
----------------------------------------------------
use the following to list the actor_ids for countries:

.. code-block:: python

    df = client.country_codes()


search for actor codes:

.. code-block:: python

    df = client.search(query='Minnesota')


get all the parts of an actor. Here I am returning the actor_id for each US state.

.. code-block:: python

    df =client.parts(actor_id='US',part_type='adm1')
