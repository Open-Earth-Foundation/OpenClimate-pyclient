from dataclasses import dataclass
import pandas as pd
from typing import List, Dict, Union, Tuple

from .ActorOverview import ActorOverview
from .Base import Base


@dataclass
class Emissions(Base):
    def _get_emissions(self, overview: Dict = None) -> pd.DataFrame:
        """retreive emissions from overview dictionary

        Args:
            overview (Dict): dictionary of overview

        Returns:
            pd.DataFrame
        """
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

    def datasets(
        self, actor_id: Union[str, List[str], Tuple[str]] = None
    ) -> pd.DataFrame:
        """retreive emissions datasets for an actor

        Args:
            actor_id (Union[str, List[str], Tuple[str]], optional): actor code

        Returns:
            pd.DataFrame:
        """
        overviews = ActorOverview().overview(actor_id=actor_id)
        list_out = [
            {
                "actor_id": overview.get("actor_id"),
                "datasource_id": datasource,
                "name": data.get("name"),
                "publisher": data.get("publisher"),
                "published": data.get("published"),
                "URL": data.get("URL"),
            }
            for overview in overviews
            if overview
            for datasource, data in overview.get("emissions").items()
        ]
        if list_out:
            return pd.DataFrame(list_out)
        return None

    def emissions(
        self,
        actor_id: Union[str, List[str], Tuple[str]] = None,
        datasource_id: str = None,
        *args,
        **kwargs,
    ) -> pd.DataFrame:
        """retrieve actor emissions

        Args:
            actor_id (Union[str, List[str], Tuple[str]], optional): actor code
            datasource_id (str, optional): emissions datasource. Defaults to None.

        Returns:
            pd.DataFrame: _description_
        """
        try:
            actor_id = [actor_id] if isinstance(actor_id, str) else actor_id
            overviews = ActorOverview().overview(actor_id=actor_id)
        except Exception:
            print(f"Something went wrong, check that {actor_id} is an actor")
        else:
            df_list = [
                self._get_emissions(overview) for overview in overviews if overview
            ]
            df = pd.concat(df_list)
            if datasource_id:
                return df.loc[df["datasource_id"] == datasource_id]
            else:
                return df
