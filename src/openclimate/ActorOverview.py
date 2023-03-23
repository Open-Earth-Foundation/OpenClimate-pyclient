import asyncio
from dataclasses import dataclass
import pandas as pd
import requests
from typing import List, Dict, Union, Tuple
import warnings

from .utils import async_func
from .Base import Base


@dataclass
class ActorOverview(Base):
    """ActorOveriew API class
    get overview information of an actor

    Returns:
        object
    """
    @async_func
    def _overview_single_actor(self, actor_id: str = None) -> Dict:
        """retreive actor emissions

        Args:
            actor_id (str): code for actor your want to retrieve

        Returns:
            DataFrame: data for each emissions dataset
        """
        endpoint = f"/actor/{actor_id}"
        url = f"{self.server}{endpoint}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers).json()
        data_list = response.get("data", None)
        if data_list is None:
            warnings.warn(
                f"ActorIDError: {actor_id} was not found", category=SyntaxWarning
            )
            return None
        return data_list

    async def _overview_coros(self, actor_id: str = None) -> Dict:
        """overview coroutines

        Args:
            actor_id (str): actor identifier. Defaults to None.

        Returns:
            Dict: dictionary with actor overview
        """
        actor_list = [actor_id] if isinstance(actor_id, str) else actor_id
        tasks = [
            asyncio.create_task(self._overview_single_actor(actor))
            for actor in actor_list
        ]
        results = await asyncio.gather(*tasks)
        return results

    def overview(
        self, actor_id: Union[str, List[str], Tuple[str]] = None
    ) -> List[Dict]:
        """Retretive actor overview

        Args:
            actor_id (Union[str, List[str], Tuple[str]]): actor identifier. Defaults to None.

        Returns:
            List[Dict]: dictionary with actor overview
        """
        return asyncio.run(self._overview_coros(actor_id=actor_id))

    def parts(
        self, actor_id: str = None, part_type: str = None, *args, **kwargs
    ) -> pd.DataFrame:
        """Retreive actor parts (e.g. subnational, cities, ...)

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
        response = requests.get(url, headers=headers).json()
        data_list = response.get("data", None)
        if data_list is None:
            warnings.warn(f"{actor_id} is not in our database", category=SyntaxWarning)
            return None
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
    ) -> pd.DataFrame:
        """returns two-letter country codes

        Args:
            like (str, optional): filters names. Defaults to None.
            case_sensitive (bool, optional): make search case-senstive. Defaults to False.
            regex (bool, optional): use regular expression like phrases. Defaults to True.

        Returns:
            pd.DataFrame
        """
        df = (
            self.parts(actor_id="EARTH", part_type="country")
            .loc[:, ["actor_id", "name", "type"]]
            .reset_index(drop=True)
        )
        if like:
            return df[df["name"].str.contains(like, case=case_sensitive, regex=regex)]
        else:
            return df
