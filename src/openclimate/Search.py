from dataclasses import dataclass
import pandas as pd
import requests
from typing import List, Dict, Union, Tuple

from .Base import Base


@dataclass
class Search(Base):
    def _search_endpoint(
        self,
        name: str = None,
        identifier: str = None,
        query: str = None,
        language: str = None,
        namespace: str = None,
        *args,
        **kwargs,
    ) -> str:
        """retrieve search endpoint

        Args:
            query (str): full search of identifiers and names that include the search parameter
            name (str): searches for actors with exact name match (e.g. "Minnesota")
            language (str, optional): two letter language code [requires name to be set]
            identifier (str): searches for actors with exact identifier code match (e.g. "US")
            namespace (str, optional): actor namespace code [requires identifier to be be set]

        Returns:
            str : the full search endpoint
        """
        count = sum(1 for x in [query, identifier, name] if x is not None)
        if count != 1:
            raise ValueError(
                "Exactly one of 'query', 'identifier' or 'name' must be passed as input"
            )
        if query:
            return f"/search/actor?q=" + query
        elif identifier:
            endpoint = f"/search/actor?identifier=" + identifier
            if namespace:
                endpoint += "&namespace=" + namespace
            return endpoint
        else:
            endpoint = f"/search/actor?name=" + name
            if language:
                endpoint += "&language=" + language
            return endpoint

    def search(
        self,
        name: str = None,
        identifier: str = None,
        query: str = None,
        language: str = None,
        namespace: str = None,
        *args,
        **kwargs,
    ) -> pd.DataFrame:
        """search actors

        Args:
            query (str): full search of identifiers and names that include the search parameter
            name (str): searches for actors with exact name match (e.g. "Minnesota")
            language (str, optional): two letter language code [requires name to be set]
            identifier (str): searches for actors with exact identifier code match (e.g. "US")
            namespace (str, optional): actor namespace code [requires identifier to be be set]

        Returns:
            pd.DataFrame: dataframe with search results
        """
        endpoint = self._search_endpoint(
            name=name,
            query=query,
            identifier=identifier,
            language=language,
            namespace=namespace,
        )
        url = f"{self.server}{endpoint}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers)
        data_list = response.json()["data"]
        columns = [
            "actor_id",
            "name",
            "type",
            "is_part_of",
            "datasource_id",
            "root_path_geo",
            "names",
            "identifiers",
        ]
        return pd.DataFrame(data_list).loc[:, columns]
