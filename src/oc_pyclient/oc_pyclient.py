from dataclasses import dataclass
from functools import lru_cache
import itertools
import json
import pandas as pd
import requests

@dataclass
class Client:
    """OpenClimate API Python Client
    base_url = "https://openclimate.openearth.dev" or "https://openclimate.network"
    """
    version: str = '/api/v1'
    base_url: str = "https://openclimate.network"
    server: str = f"{base_url}{version}"

    def __repr__(self):
        return f"OpenClimate({self.server})"

    def __str__(self):
        return f"OpenClimate({self.server})"

    @lru_cache(maxsize=10)
    def _actor_overview(self, actor_id: str = None, *args, **kwargs):
        """retreive actor emissions

        Args:
            actor_id (str): code for actor your want to retrieve

        Returns:
            DataFrame: data for each emissions dataset
        """
        endpoint = f"/actor/{actor_id}"
        url = f"{self.server}{endpoint}"
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers=headers)

        try:
            data_list = response.json()['data']
            return data_list
        except KeyError as err:
            print(f"ActorIdError: actor_id of '{actor_id}' is not found")
            raise err

    def _search_endpoint(self,
                         name: str = None,
                         identifier: str = None,
                         query: str = None,
                         language: str = None,
                         namespace: str = None, *args, **kwargs):
        """retrieve search endpoint

        Args:
            query (str): full search of identifiers and names that include the search parameter
            name (str): searches for actors with exact name match (e.g. "Minnesota")
            language (str, optional): two letter language code [requires name to be set]
            identifier (str): searches for actors with exact identifier code match (e.g. "US")
            namespace (str, optional): actor namespace code [requires identifier to be be set]

        Returns:
            Str : the full search endpoint
        """
        count = sum(1 for x in [query, identifier, name] if x is not None)
        if count != 1:
            raise ValueError(
                "Exactly one of 'query', 'identifier' or 'name' must be passed as input")
        if query:
            return f'/search/actor?q=' + query
        elif identifier:
            endpoint = f'/search/actor?identifier=' + identifier
            if namespace:
                endpoint += '&namespace=' + namespace
            return endpoint
        else:
            endpoint = f'/search/actor?name=' + name
            if language:
                endpoint += '&language=' + language
            return endpoint

    def targets(self, actor_id: str = None, *args, **kwargs):
        """retreive actor targets

        Args:
            actor_id (str): code for actor your want to retrieve

        Returns:
            DataFrame: data for each emissions dataset
        """
        try:
            data_list = self._actor_overview(actor_id=actor_id)
        except Exception:
            print(f"Something went wrong, check that {actor_id} is an actor")
        else:
            data = data_list['targets']
            df = pd.DataFrame(data).sort_values(by=['target_year'])
            return df

    def emissions(self, actor_id: str = None, *args, **kwargs):
        """retreive actor emissions

        Args:
            actor_id (str): code for actor your want to retrieve

        Returns:
            DataFrame: data for each emissions dataset
        """
        try:
            data_list = self._actor_overview(actor_id=actor_id)
        except Exception:
            print(f"Something went wrong, check that {actor_id} is an actor")
        else:
            # reads all emissions data, concats together
            data = [data_list['emissions'][dataset]['data']
                    for dataset in data_list['emissions']]
            merged = list(itertools.chain(*data))
            df = pd.DataFrame(merged).sort_values(by=['emissions_id'])
            df["dataset"] = df["emissions_id"].str.split(":").str[0]
            return df

    def population(self, actor_id: str = None, *args, **kwargs):
        """retreive actor population

        Args:
            actor_id (str): code for actor your want to retrieve

        Returns:
            DataFrame: data for each emissions dataset
        """
        try:
            data_list = self._actor_overview(actor_id=actor_id)
        except Exception:
            print(f"Something went wrong, check that {actor_id} is an actor")
        else:
            # reads all emissions data, concats together
            data = data_list['population']
            df = pd.DataFrame(data).sort_values(by=['year'])
            return df

    def gdp(self, actor_id: str = None, *args, **kwargs):
        """retreive actor GDP

        Args:
            actor_id (str): code for actor your want to retrieve

        Returns:
            DataFrame: data for each emissions dataset
        """
        try:
            data_list = self._actor_overview(actor_id=actor_id)
        except Exception:
            print(f"Something went wrong, check that {actor_id} is an actor")
        else:
            # reads all emissions data, concats together
            data = data_list['gdp']
            df = pd.DataFrame(data).sort_values(by=['year'])
            return df

    @lru_cache(maxsize=10)
    def parts(self, actor_id: str = None, part_type: str = None, *args, **kwargs):
        """retreive actor parts

        Args:
            actor_id (str): code for actor your want to retrieve
            part_type (str, optional): administrative level

        Returns:
            DataFrame: data for each emissions dataset
        """
        endpoint = f"/actor/{actor_id}/parts"
        if part_type:
            part_type = part_type.lower()
            types = ['planet', 'country', 'adm1',
                     'adm2', 'city', 'organization', 'site']
            if part_type not in types:
                print(part_type)
                raise Exception(
                    f"PartTypeError: part type of {part_type} not in {types}")

            endpoint += f"?type={part_type}"

        url = f"{self.server}{endpoint}"
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers=headers)

        try:
            data_list = response.json()['data']
        except KeyError as err:
            print(f"ActorIdError: actor_id of '{actor_id}' is not found")
        except Exception:
            print(f"Error: something went wrong")
        else:
            df = pd.DataFrame(data_list).sort_values(by=['type', 'actor_id'])
            return df

    @lru_cache(maxsize=10)
    def search(self,
               name: str = None,
               identifier: str = None,
               query: str = None,
               language: str = None,
               namespace: str = None, *args, **kwargs):
        """search actors

        Args:
            query (str): full search of identifiers and names that include the search parameter
            name (str): searches for actors with exact name match (e.g. "Minnesota")
            language (str, optional): two letter language code [requires name to be set]
            identifier (str): searches for actors with exact identifier code match (e.g. "US")
            namespace (str, optional): actor namespace code [requires identifier to be be set]

        Returns:
            List: list of JSON documents
        """
        endpoint = self._search_endpoint(name=name,
                                         query=query,
                                         identifier=identifier,
                                         language=language,
                                         namespace=namespace)
        url = f"{self.server}{endpoint}"
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers=headers)
        data_list = response.json()['data']
        return data_list
