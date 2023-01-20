# OpenClimate-pyclient

A Python client for the OpenClimate API

# Installation
This initial release is installable from GitHub using the following command:
```
pip install git+https://github.com/Open-Earth-Foundation/OpenClimate-pyclient.git#egg=oc_pyclient
```
We will soon make the package available on `PyPi` and `conda`.

# Usage
Retrieve all emissions data for the United States and save output to a Pandas DataFrame.
```python
from oc_pyclient import Client

client = Client()
df = client.emissions(actor_id='US')
```

Retrieve population data
```python
df = client.population(actor_id='US')
```

Retrieve GDP data
```python
df = client.gdp(actor_id='US')
```

For bleeding edge data updates, set `dev=True` to retrieve from the development server.
```python
client = Client(dev=True)
df = client.emissions(actor_id='US')
```
