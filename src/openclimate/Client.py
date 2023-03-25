from dataclasses import dataclass
import pandas as pd
from typing import List, Dict, Union, Tuple

from .ActorOverview import ActorOverview
from .Base import Base
from .Emissions import Emissions
from .GDP import GDP
from .Population import Population
from .Search import Search
from .Targets import Targets


@dataclass
class Client(Base):
    """OpenClimate API Python Client

    *If you are using Jupyter*

    either run
    ```python
    client = Client()
    client.jupyter
    ```

    or manually add the following lines of code
    ```python
    import nest_asyncio
    nest_asyncio.apply()
    ```
    """

    @property
    def jupyter(self):
        import nest_asyncio

        nest_asyncio.apply()

    def emissions(
        self, actor_id: str = None, datasource_id: str = None, ignore_warnings: bool = False
    ) -> pd.DataFrame:
        """retreive actor emissions

        Args:
            actor_id (str|List[str]): code for actor your want to retrieve
            datasource_id (str): code emissions dataset
            ignore_warnings (bool): ignore warning messages

        Returns:
            DataFrame: data for each emissions dataset
        """
        return Emissions().emissions(actor_id=actor_id, datasource_id=datasource_id, ignore_warnings=ignore_warnings)

    def emissions_datasets(self, actor_id: str = None, ignore_warnings: bool = False) -> pd.DataFrame:
        """retreive actor emissions datasets

        Args:
            actor_id (str): code for actor your want to retrieve
            ignore_warnings (bool): ignore warning messages

        Returns:
            DataFrame: data of emission datasets
        """
        return Emissions().datasets(actor_id=actor_id, ignore_warnings=ignore_warnings)

    def targets(self, actor_id: str = None, ignore_warnings: bool = False) -> pd.DataFrame:
        """retreive actor targets

        Args:
            actor_id (str|List[str]): code for actor your want to retrieve
            ignore_warnings (bool): ignore warning messages

        Returns:
            DataFrame: dataframe of targets
        """
        return Targets().targets(actor_id=actor_id, ignore_warnings=ignore_warnings)

    def population(self, actor_id: str = None, ignore_warnings: bool = False) -> pd.DataFrame:
        """retreive actor population

        Args:
            actor_id (str|List[str]): code for actor your want to retrieve
            ignore_warnings (bool): ignore warning messages

        Returns:
            DataFrame: dataframe of population
        """
        return Population().population(actor_id=actor_id, ignore_warnings=ignore_warnings)

    def gdp(self, actor_id: str = None, ignore_warnings: bool = False) -> pd.DataFrame:
        """retreive actor GDP

        Args:
            actor_id (str|List[str]): code for actor your want to retrieve
            ignore_warnings (bool): ignore warning messages

        Returns:
            DataFrame: dataframe of GDP
        """
        return GDP().gdp(actor_id=actor_id, ignore_warnings=ignore_warnings)

    def parts(
        self, actor_id: str = None, part_type: str = None, *args, **kwargs
    ) -> pd.DataFrame:
        """retreive actor parts

        returns subnational, cities, companies, etc. within an actor_id

        Args:
            actor_id (str|List[str]): code for actor your want to retrieve
            part_type (str): retrieve actors from administrative part ['planet', 'country', 'adm1', 'adm2', 'city', 'organization', 'site']

        Returns:
            DataFrame: dataframe of actors parts
        """
        return ActorOverview().parts(actor_id=actor_id, part_type=part_type)

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
        """search actor names and identifiers

        Args:
            query (str): full search of identifiers and names that include the search parameter
            name (str): searches for actors with exact name match (e.g. "Minnesota")
            language (str, optional): two letter language code [requires name to be set]
            identifier (str): searches for actors with exact identifier code match (e.g. "US")
            namespace (str, optional): actor namespace code [requires identifier to be be set]

        Returns:
            DataFrame: dataframe of search results
        """
        return Search().search(
            name=name,
            identifier=identifier,
            query=query,
            language=language,
            namespace=namespace,
            *args,
            **kwargs,
        )

    def country_codes(
        self,
        like: str = None,
        case_sensitive: bool = False,
        regex: bool = True,
        *args,
        **kwargs,
    ) -> pd.DataFrame:
        """get country codes and filter using `like` regex phrases

        Args:
            like (str): phrase to search for in name (optional)
            case_senstive (bool): case senstive search [default: False] (optional)
            regex (bool): use regex with like [default: True] (optional)

        Returns:
            DataFrame: dataframe of country codes
        """
        return (
            ActorOverview()
            .country_codes(
                like=like, case_sensitive=case_sensitive, regex=regex, *args, **kwargs
            )
            .reset_index(drop=True)
        )
