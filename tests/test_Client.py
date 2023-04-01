import openclimate
import pytest

def test_emissions():
    client = openclimate.Client()
    client.emissions(actor_id='US')
    client.emissions(actor_id=['US','CA'])
    client.emissions(actor_id=['US','CA'], datasource_id='not_a_datasource')
    assert client.emissions(actor_id='x') ==  None

def test_emissions_datasets():
    client = openclimate.Client()
    client.emissions_datasets(actor_id='US')

def test_targets():
    client = openclimate.Client()
    client.targets(actor_id='US')

def test_gdp():
    client = openclimate.Client()
    client.gdp(actor_id='US')

def test_population():
    client = openclimate.Client()
    client.population(actor_id='US')

def test_country_codes():
    client = openclimate.Client()
    client.country_codes()

def test_parts():
    client = openclimate.Client()
    client.parts(actor_id='US')

def test_search():
    client = openclimate.Client()
    client.search(name='Iran')
    client.search(name='Iran', language='en')

    client.search(identifier='US')
    client.search(identifier='US', namespace='ISO-3166-1 alpha-2')

    with pytest.raises(KeyError):
        client.search(name='NOT_A_NAME')

    client.search(query='Iran')