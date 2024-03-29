import asyncio
from functools import wraps
import pandas as pd
from typing import List, Dict, Any
import warnings


def explode_dict_columns(df: pd.DataFrame = None) -> pd.DataFrame:
    """expand rows with dictionaries into separate columns

    Args:
        df (pd.DataFrame): pandas dataframe. Defaults to None.

    Returns:
        pd.DataFrame: pandas dataframe
    """
    for col in df.columns:
        if any(isinstance(entry, dict) for entry in df[col]):
            df[col] = df[col].fillna({})
            df_expanded = pd.json_normalize(df[col])
            df_expanded.columns = [f"{col}_{subcol}" for subcol in df_expanded.columns]
            df = pd.concat([df.drop(col, axis=1), df_expanded], axis=1)
    return df


def async_func(func):
    """decorator to turn a synchronous function into async

    Args:
        func (function): synchronous function

    Returns:
        function: async function
    """

    @wraps(func)
    async def wrapper():
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func)

    return wrapper


def filter_overviews(overviews: List[Dict[Any, Any]], key: str, ignore_warnings: bool = False) -> List[Dict[Any, Any]]:
    """filter overviews if has data for key

    Args:
        overviews (List[Dict]): list of actor overviews
        ignore_warnings (bool): ignore warning messages

    Returns:
        List[Dict]: filtered overviews
    """
    overviews = [d for d in overviews if d is not None]
    filtered_overviews = []
    warnings.simplefilter('ignore') if ignore_warnings else warnings.simplefilter('default')
    for overview in overviews:
        if overview.get(key):
            filtered_overviews.append(overview)
        else:
            warnings.warn(
                f"NoDataError: {overview.get('actor_id')} has no {key} data", category=UserWarning
            )
    return filtered_overviews
