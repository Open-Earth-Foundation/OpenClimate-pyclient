from dataclasses import dataclass
import pandas as pd
from typing import List, Dict, Union, Tuple

from .utils import explode_dict_columns

from .ActorOverview import ActorOverview
from .Base import Base


@dataclass
class Targets(Base):
    def _get_target(self, overview: Dict = None) -> pd.DataFrame:
        """retreive targets from overview dictionary

        Args:
            overview (Dict): dictionary of overview

        Returns:
            pd.DataFrame
        """
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

    def targets(
        self, actor_id: Union[str, List[str], Tuple[str]] = None, *args, **kwargs
    ) -> pd.DataFrame:
        """retreive actor targets

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
            df_list = [self._get_target(overview) for overview in overviews if overview]
            return pd.concat(df_list)
