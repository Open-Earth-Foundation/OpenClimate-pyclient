import asyncio
from dataclasses import dataclass
from functools import wraps
import itertools
import pandas as pd
import requests


def explode_dict_columns(df):
    for col in df.columns:
        if any(isinstance(entry, dict) for entry in df[col]):
            df[col] = df[col].fillna({})
            df_expanded = pd.json_normalize(df[col])
            df_expanded.columns = [f"{col}_{subcol}" for subcol in df_expanded.columns]
            df = pd.concat([df.drop(col, axis=1), df_expanded], axis=1)
    return df


def async_func(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, *args, **kwargs)

    return wrapper


@dataclass
class Base:
    version: str = "/api/v1"
    base_url: str = "https://openclimate.openearth.dev"
    server: str = f"{base_url}{version}"

    def __repr__(self):
        return f"OpenClimate({self.server})"

    def __str__(self):
        return f"OpenClimate({self.server})"


@dataclass
class ActorOverview(Base):
    """Get overview of actor for processing"""

    @async_func
    def _overview_single_actor(self, actor_id: str = None):
        """retreive actor emissions

        Args:
            actor_id (str): code for actor your want to retrieve

        Returns:
            DataFrame: data for each emissions dataset
        """
        endpoint = f"/actor/{actor_id}"
        url = f"{self.server}{endpoint}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers)

        try:
            data_list = response.json()["data"]
            return data_list
        except KeyError as err:
            print(f"ActorIdError: actor_id of '{actor_id}' is not found")
            raise err

    async def _overview_coros(self, actor_id: str = None):
        actor_list = [actor_id] if isinstance(actor_id, str) else actor_id
        tasks = [
            asyncio.create_task(self._overview_single_actor(actor))
            for actor in actor_list
        ]
        results = await asyncio.gather(*tasks)
        return results

    def overview(self, actor_id: str = None):
        return asyncio.run(self._overview_coros(actor_id=actor_id))

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
            types = [
                "planet",
                "country",
                "adm1",
                "adm2",
                "city",
                "organization",
                "site",
            ]
            if part_type not in types:
                print(part_type)
                raise Exception(
                    f"PartTypeError: part type of {part_type} not in {types}"
                )

            endpoint += f"?type={part_type}"

        url = f"{self.server}{endpoint}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers)

        try:
            data_list = response.json()["data"]
        except KeyError as err:
            print(f"ActorIdError: actor_id of '{actor_id}' is not found")
        except Exception:
            print(f"Error: something went wrong")
        else:
            df = pd.DataFrame(data_list).sort_values(by=["type", "actor_id"])
            return df

    def country_codes(
        self,
        like: str = None,
        case_sensitive: bool = False,
        regex: bool = True,
        *args,
        **kwargs,
    ):
        df = (
            self.parts(actor_id="EARTH", part_type="country")
            .loc[:, ["actor_id", "name", "type"]]
            .reset_index(drop=True)
        )
        if like:
            return df[df["name"].str.contains(like, case=case_sensitive, regex=regex)]
        else:
            return df


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
    ):
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
    ):
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


@dataclass
class Emissions(Base):
    def _get_emissions(self, overview=None):
        data = []
        for dataset in overview["emissions"]:
            df_tmp = pd.DataFrame(overview["emissions"][dataset]["data"]).assign(
                datasource_id=dataset
            )
            data.append(df_tmp)

        columns = ["actor_id", "year", "total_emissions", "datasource_id"]
        df_out = (
            pd.concat(data)
            .sort_values(by=["emissions_id"])
            .assign(actor_id=overview["actor_id"])
            .drop(columns=["tags", "emissions_id"])
            .loc[:, columns]
        )
        return df_out.reset_index(drop=True)

    def datasets(self, actor_id: str = None):
        overview = ActorOverview().overview(actor_id=actor_id)
        df = pd.DataFrame(overview)
        datasets = list(
            itertools.chain(*[list(dataset.keys()) for dataset in df["emissions"]])
        )
        out_list = []
        for dataset in datasets:
            out_dict = {
                key: df["emissions"][0].get(dataset).get(key, None)
                for key in ["datasource_id", "name", "publisher", "published", "URL"]
            }
            out_list.append(out_dict)

        df_out = pd.DataFrame(out_list)
        return df_out

    def emissions(self, actor_id: str = None, datasource_id=None, *args, **kwargs):
        """retreive actor emissions

        Args:
            actor_id (str): code for actor your want to retrieve

        Returns:
            DataFrame: data for each emissions dataset
        """
        try:
            actor_id = [actor_id] if isinstance(actor_id, str) else actor_id
            overviews = ActorOverview().overview(actor_id=actor_id)
        except Exception:
            print(f"Something went wrong, check that {actor_id} is an actor")
        else:
            df_list = [self._get_emissions(overview) for overview in overviews]
            df = pd.concat(df_list)
            if datasource_id:
                return df.loc[df["datasource_id"] == datasource_id]
            else:
                return df


@dataclass
class Targets(Base):
    def _get_target(self, overview):
        data = overview["targets"]
        columns = [
            "actor_id",
            "target_type",
            "baseline_year",
            "baseline_value",
            "target_year",
            "target_value",
            "target_unit",
            "datasource_id",
            "datasource_name",
            "datasource_publisher",
            "datasource_published",
            "datasource_URL",
            "initiative_initiative_id",
            "initiative_name",
            "initiative_description",
            "initiative_URL",
        ]
        df = (
            pd.DataFrame(data)
            .sort_values(by=["target_year"])
            .assign(actor_id=overview["actor_id"])
        )
        return (
            explode_dict_columns(df)
            .loc[:, columns]
            .rename({"initiative_initiative_id": "initiative_id"})
            .reset_index(drop=True)
        )

    def targets(self, actor_id: str = None, *args, **kwargs):
        """retreive actor targets

        Args:
            actor_id (str): code for actor your want to retrieve

        Returns:
            DataFrame: data for each emissions dataset
        """
        try:
            actor_id = [actor_id] if isinstance(actor_id, str) else actor_id
            overviews = ActorOverview().overview(actor_id=actor_id)
        except Exception:
            print(f"Something went wrong, check that {actor_id} is an actor")
        else:
            df_list = [self._get_target(overview) for overview in overviews]
            return pd.concat(df_list)


@dataclass
class Population(Base):
    def _get_population(self, overview):
        data = overview["population"]
        df = pd.DataFrame(data).sort_values(by=["year"])
        df["actor_id"] = overview["actor_id"]
        columns = [
            "actor_id",
            "year",
            "population",
            "datasource_id",
            "datasource_name",
            "datasource_published",
            "datasource_URL",
        ]
        return explode_dict_columns(df).loc[:, columns].reset_index(drop=True)

    def population(self, actor_id: str = None, *args, **kwargs):
        """retreive actor emissions

        ** THIS NEEDS TO WORK WITH LIST OR STRING

        Args:
            actor_id (str): code for actor your want to retrieve

        Returns:
            DataFrame: data for each emissions dataset
        """
        try:
            actor_id = [actor_id] if isinstance(actor_id, str) else actor_id
            overviews = ActorOverview().overview(actor_id=actor_id)
        except Exception:
            print(f"Something went wrong, check that {actor_id} is an actor")
        else:
            df_list = [self._get_population(overview) for overview in overviews]
            return pd.concat(df_list)


@dataclass
class GDP(Base):
    def _get_gdp(self, overview):
        data = overview["gdp"]
        df = pd.DataFrame(data).sort_values(by=["year"])
        df["actor_id"] = overview["actor_id"]
        columns = [
            "actor_id",
            "year",
            "gdp",
            "datasource_id",
            "datasource_name",
            "datasource_published",
            "datasource_URL",
        ]
        return explode_dict_columns(df).loc[:, columns].reset_index(drop=True)

    def gdp(self, actor_id: str = None, *args, **kwargs):
        """retreive actor emissions

        Args:
            actor_id (str): code for actor your want to retrieve

        Returns:
            DataFrame: data for each emissions dataset
        """
        try:
            actor_id = [actor_id] if isinstance(actor_id, str) else actor_id
            overviews = ActorOverview().overview(actor_id=actor_id)
        except Exception:
            print(f"Something went wrong, check that {actor_id} is an actor")
        else:
            df_list = [self._get_gdp(overview) for overview in overviews]
            return pd.concat(df_list)


@dataclass
class Client(Base):
    """OpenClimate API Python Client
    base_url = "https://openclimate.openearth.dev" or "https://openclimate.network"
    """

    def emissions(self, actor_id=None, datasource_id=None):
        """retreive actor emissions

        Args:
            actor_id (str|List[str]): code for actor your want to retrieve
            datasource_id (str): code emissions dataset

        Returns:
            DataFrame: data for each emissions dataset
        """
        return Emissions().emissions(actor_id=actor_id, datasource_id=datasource_id)

    def emissions_datasets(self, actor_id=None):
        """retreive actor emissions datasets

        Args:
            actor_id (str): code for actor your want to retrieve

        Returns:
            DataFrame: data of emission datasets
        """
        return Emissions().datasets(actor_id=actor_id)

    def targets(self, actor_id=None):
        """retreive actor targets

        Args:
            actor_id (str|List[str]): code for actor your want to retrieve

        Returns:
            DataFrame: dataframe of targets
        """
        return Targets().targets(actor_id=actor_id)

    def population(self, actor_id=None):
        """retreive actor population

        Args:
            actor_id (str|List[str]): code for actor your want to retrieve

        Returns:
            DataFrame: dataframe of population
        """
        return Population().population(actor_id=actor_id)

    def gdp(self, actor_id=None):
        """retreive actor GDP

        Args:
            actor_id (str|List[str]): code for actor your want to retrieve

        Returns:
            DataFrame: dataframe of GDP
        """
        return GDP().gdp(actor_id=actor_id)

    def parts(self, actor_id: str = None, part_type: str = None, *args, **kwargs):
        """retreive actor parts

        Args:
            actor_id (str|List[str]): code for actor your want to retrieve
            part_type (str): retrieve actors from administrative part
                ['planet', 'country', 'adm1', 'adm2', 'city', 'organization', 'site']

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
    ):
        """search actors

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
    ):
        """search actors

        Args:
            like (str): phrase to search for in name
            case_senstive (bool): case senstive search [default: False]
            regex (bool): treat like phrase as a regular expression [default: True]

        Returns:
            DataFrame: dataframe of search results
        """
        return (
            ActorOverview()
            .country_codes(
                like=like, case_sensitive=case_sensitive, regex=regex, *args, **kwargs
            )
            .reset_index(drop=True)
        )
