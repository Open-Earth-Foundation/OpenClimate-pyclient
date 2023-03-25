from dataclasses import dataclass
import pandas as pd
from typing import List, Dict, Union, Tuple

from .utils import explode_dict_columns
from .utils import filter_overviews

from .ActorOverview import ActorOverview
from .Base import Base


@dataclass
class GDP(Base):
    def _get_gdp(self, overview: Dict = None) -> pd.DataFrame:
        """retreive GDP from overview dictionary

        Args:
            overview (Dict): dictionary of overview

        Returns:
            pd.DataFrame
        """
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

    def gdp(
        self, actor_id: Union[str, List[str], Tuple[str]] = None, ignore_warnings: bool = False, *args, **kwargs
    ) -> pd.DataFrame:
        """retreive actor GDP

        Args:
            actor_id (Union[str, List[str], Tuple[str]], optional): actor code
            ignore_warnings (bool): ignore warning messages

        Returns:
            pd.DataFrame:
        """
        try:
            actor_id = [actor_id] if isinstance(actor_id, str) else actor_id
            overviews = ActorOverview().overview(actor_id=actor_id, ignore_warnings=ignore_warnings)
        except Exception:
            print(f"Something went wrong, check that {actor_id} is an actor")
        else:
            overviews = filter_overviews(overviews, 'gdp', ignore_warnings)
            overviews = [overview for overview in overviews if 'gdp' in overview.keys()]
            df_list = [self._get_gdp(overview) for overview in overviews if overview]
            return pd.concat(df_list)
