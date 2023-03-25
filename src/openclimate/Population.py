from dataclasses import dataclass
import pandas as pd
from typing import List, Dict, Union, Tuple

from .utils import explode_dict_columns
from .utils import filter_overviews

from .ActorOverview import ActorOverview
from .Base import Base


@dataclass
class Population(Base):
    def _get_population(self, overview: Dict = None) -> pd.DataFrame:
        """retreive population from overview dictionary

        Args:
            overview (Dict): dictionary of overview

        Returns:
            pd.DataFrame
        """
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

    def population(
        self, actor_id: Union[str, List[str], Tuple[str]] = None, *args, **kwargs
    ) -> pd.DataFrame:
        """retreive actor population

        Args:
            actor_id (Union[str, List[str], Tuple[str]], optional): actor code

        Returns:
            pd.DataFrame:
        """
        try:
            actor_id = [actor_id] if isinstance(actor_id, str) else actor_id
            overviews = ActorOverview().overview(actor_id=actor_id)
        except Exception:
            print(f"Something went wrong, check that {actor_id} is an actor")
        else:
            overviews = filter_overviews(overviews, 'population')
            df_list = [
                self._get_population(overview) for overview in overviews if overview
            ]
            return pd.concat(df_list)
