import re 
from nba_api.stats.endpoints import playercareerstats, playerindex, playbyplayv3
import pandas as pd
import numpy as np
from typing import Union

def standarsize_clock(clock: str) -> str:
    m = re.match(r'^(\d{1,2}):(\d{2})$', clock)
    if clock.startswith('PT'):
        return clock
    elif m:
        ex = m.groups()
        result = f"PT{ex[0].zfill(2)}M{ex[1]}.00S"
        return result

def clock_to_absolute_seconds(clock: str, period: int) -> float:
    """
    Convert a clock string to absolute seconds in a game

    Returns:
    float: Time in seconds
    """
    if not clock.startswith('PT'):
        m = re.match(r'^(\d{1,2}):(\d{1,2})$', clock)
        if m:
            clock = standarsize_clock(clock)
        else:
            raise ValueError("Clock format should start with 'PT' or be in the format MM:SS")
    
    time_str = clock[2:]
    minutes, seconds = time_str.split('M')
    seconds = seconds.rstrip('S')
    
    period_seconds = (period - 1) * 12 * 60  # Each period is 12 minutes
    clock_seconds = int(minutes) * 60 + float(seconds)
    time_passed = 12 * 60 - clock_seconds # the shot clock shows time remaining
    
    return period_seconds + time_passed

def gather_mul_career_stats(player_ids: Union[list, np.ndarray]) -> pd.DataFrame:
    player_stats = []
    for player_id in player_ids:
        career = playercareerstats.PlayerCareerStats(player_id=player_id)
        career = career.get_data_frames()[0]
        player_stats.append(career)
    return pd.concat(player_stats, ignore_index=True)


def gather_mul_player_index(player_ids: Union[list, np.ndarray]) -> pd.DataFrame:
    player_index = []
    for player_id in player_ids:
        player = playerindex.PlayerIndex(season='2014-15', active_flag='Y')
        player = player.get_data_frames()[0]
        player_index.append(player)
    return pd.concat(player_index, ignore_index=True)


def missing_values_summary(df):
    """
    Function to summarize missing values in a dataframe.
    
    Parameters:
    df (pd.DataFrame): The dataframe to check for missing values.
    
    Returns:
    pd.DataFrame: A dataframe summarizing the missing values for each column.
    """
    missing_values = df.isna().sum()
    missing_percentage = (missing_values / len(df)) * 100
    missing_summary = pd.DataFrame({'Missing Values': missing_values, 'Percentage': missing_percentage})
    return missing_summary[missing_summary['Missing Values'] > 0].sort_values(by='Missing Values', ascending=False)


def find_constant_columns(df):
    """
    Find columns with constant values in a DataFrame.
    
    Parameters:
    df (pd.DataFrame): The dataframe to check for constant columns.
    
    Returns:
    list: A list of column names with constant values.
    """
    constant_columns = [col for col in df.columns if df[col].nunique() == 1]
    return constant_columns
