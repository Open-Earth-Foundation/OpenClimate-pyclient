# OpenClimate-pyclient

[![Documentation Status](https://readthedocs.org/projects/openclimate-pyclient/badge/?version=latest)](https://openclimate-pyclient.readthedocs.io/en/latest/?badge=latest)
[![pypi](https://badgen.net/pypi/v/openclimate)](https://pypi.org/project/openclimate)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/Open-Earth-Foundation/OpenClimate-pyclient/issues)

A Python Client for the [OpenClimate API](https://github.com/Open-Earth-Foundation/OpenClimate/blob/develop/api/API.md)

Try out the client in [Binder](https://mybinder.org/v2/gh/Open-Earth-Foundation/OpenClimate-pyclient/HEAD?urlpath=lab/tree/notebooks/).
# Installation
```
pip install openclimate
```

# Usage
Import and create a `Client()` object
```python
from openclimate import Client
client = Client()
```

## Retrieving data

### Emissions
Retrieve all emissions data for a single actor. Here I am retrieving emissions data for Canada
```python
df = client.emissions(actor_id='CA')
```

Retrieve all emissions data for a list of actors. Here I am retrieving emission data for the United States, Canada, and Great Britain.
```python
df = client.emissions(actor_id=['US','CA','GB'])
```

Return the different datasets available for a particular actor:
```python
df = client.emissions_datasets(actor_id='US')
```

Only select data for a particular dataset
```python
df = client.emissions_datasets(actor_id='US', datasource_id='GCB2022:national_fossil_emissions:v1.0')
```

### Targets
Retrieve emissions targets for a particule actor
```python
df = client.targets(actor_id='US')
```

### Population
Retrieve population data.
```python
df = client.population(actor_id=['US','CA','GB'])
```

### GDP
Retrieve GDP data.
```python
df = client.gdp(actor_id=['US','CA','GB'])
```

## Searching for codes
use the following to list the actor_ids for countries:
```python
df = client.country_codes()
```

search for actor codes:
```python
df = client.search(query='Minnesota')
```

get all the parts of an actor. Here I am returning the actor_id for each US state.
```python
df = client.parts(actor_id='US',part_type='adm1')
```