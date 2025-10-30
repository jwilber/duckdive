from datetime import datetime, timedelta

import pandas as pd
from rich.table import Table
from typing import Dict, List, Optional


# surfline optimal score mapping
optimal_score_mapping = {0: "Suboptimal", 1: "Good", 2: "Optimal"}

units_mapping = {
    "temperature": "F",
    "height": "FT",
    "swellHeight": "FT",
    "waveHeight": "FT",
    "windSpeed": "KTS",
    "pressure": "MB",
}

spot_dict = {
    "5842041f4e65fad6a7708839": "Scripps",
    "5842041f4e65fad6a77088cc": "LJ Shores",
    "5842041f4e65fad6a770883b": "Blacks",
    "5842041f4e65fad6a77088c4": "Tourmo",
    "5842041f4e65fad6a7708842": "Mission",
    "5842041f4e65fad6a7708841": "PB",
    "5842041f4e65fad6a770883f": "OB",
    "5842041f4e65fad6a77088af": "Del Mar",
}


def load_spot_ids() -> List[str]:
    """
    Load spot IDs from duckdive_spots.json file.
    Returns list of spot IDs if file exists, None otherwise.
    """
    spots_file = Path.cwd() / "duckdive_spots.json"
    if spots_file.exists():
        with open(spots_file) as f:
            data = json.load(f)
            return list(data.values())
    return None


column_colors = [
    "cyan",
    "green",
    "yellow",
    "magenta",
    "red",
    "white",
    "bright_green",
    "bright_blue",
    "bright_magenta",
]


def create_pretty_table(data: pd.DataFrame) -> Table:
    """
    Create a pretty table from a pandas DataFrame using rich's Table.
    Each column will have a different color.

    :param data: pandas DataFrame
    :return: rich Table object
    """
    table = Table(show_header=True, header_style="bold magenta")

    # Cycle through the column colors if there are more columns than colors
    num_columns = len(data.columns)
    colors = column_colors * ((num_columns // len(column_colors)) + 1)

    # Add columns to the rich Table with a different color for each
    for i, col in enumerate(data.columns):
        table.add_column(col, style=colors[i])

    # Add rows to the rich Table
    for _, row in data.iterrows():
        table.add_row(*[str(value) for value in row])

    return table


def format_sunlight_timestamp(timestamp: int) -> str:
    """
    Converts a UNIX timestamp into a human-readable format.
    Format: day-month-year hour-minute AM/PM

    :param timestamp: The UNIX timestamp to convert
    :return: A string in the format 'day-month-year hour-minute AM/PM'
    """
    # Convert the UNIX timestamp to a datetime object
    dt_object = datetime.fromtimestamp(timestamp)

    # Format the datetime object into the required string format
    return dt_object.strftime("%Y-%m-%d %I:%M %p")


def format_timestamp(unix_timestamp: int, utc_offset: int = 0) -> str:
    """
    Convert a Unix timestamp into a human-readable date-time format.

    :param unix_timestamp: The Unix timestamp (e.g., 1727517600).
    :param utc_offset: UTC offset in hours (defaults to 0).
    :return: A string representing the human-readable date and time.
    """
    dt = datetime.utcfromtimestamp(unix_timestamp) + timedelta(hours=utc_offset)
    return dt.strftime("%Y-%m-%d %I%p")  # Format to 'YYYY-MM-DD HAMP/PM'


def format_ratings_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Formats the ratings DataFrame by:
    - Destructuring the 'rating' column into 'rating_key' and 'rating_value'

    :param df: The DataFrame containing rating data
    :return: The formatted DataFrame with 'rating_key' and 'rating_value' columns, and the original 'rating' column dropped
    """
    df["rating_key"] = df["rating"].apply(
        lambda x: x.get("key") if isinstance(x, dict) else None
    )
    df["rating_value"] = df["rating"].apply(
        lambda x: x.get("value") if isinstance(x, dict) else None
    )
    df = df.drop(columns=["rating"])  # Drop the original "rating" column
    return df


def format_swells_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Formats the swells DataFrame by:
    - Taking only the primary (first) swell from each timestamp

    :param df: The DataFrame containing swells data
    :return: The DataFrame with only primary swell data
    """
    # Process each row to extract only the primary swell
    for idx, row in df.iterrows():
        swells = row["swells"]
        if isinstance(swells, list) and len(swells) > 0:
            # Take only the first (primary) swell
            primary_swell = swells[0]
            # Update the row with primary swell data
            for key, value in primary_swell.items():
                df.at[idx, key] = value

    # Drop the original swells column
    df = df.drop(columns=["swells"])

    return df


def format_conditions_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Formats the conditions DataFrame by:
    - Destructuring the 'forecaster' column into 'forecaster_name' and 'forecaster_avatar'
    - Destructuring the 'am' and 'pm' columns into individual columns like 'am_observation', 'am_rating', etc.

    :param df: The DataFrame containing conditions data
    :return: The formatted DataFrame with additional columns and original columns dropped
    """

    # Destructure 'forecaster' into separate columns
    df["forecaster_name"] = df["forecaster"].apply(
        lambda x: x.get("name") if isinstance(x, dict) else None
    )
    df["forecaster_avatar"] = df["forecaster"].apply(
        lambda x: x.get("avatar") if isinstance(x, dict) else None
    )
    df = df.drop(columns=["forecaster"])  # Drop the original "forecaster" column

    # Destructure 'am' into separate columns
    df["am_timestamp"] = df["am"].apply(
        lambda x: x.get("timestamp") if isinstance(x, dict) else None
    )
    df["am_observation"] = df["am"].apply(
        lambda x: x.get("observation") if isinstance(x, dict) else None
    )
    df["am_rating"] = df["am"].apply(
        lambda x: x.get("rating") if isinstance(x, dict) else None
    )
    df["am_minHeight"] = df["am"].apply(
        lambda x: x.get("minHeight") if isinstance(x, dict) else None
    )
    df["am_maxHeight"] = df["am"].apply(
        lambda x: x.get("maxHeight") if isinstance(x, dict) else None
    )
    df["am_plus"] = df["am"].apply(
        lambda x: x.get("plus") if isinstance(x, dict) else None
    )
    df["am_humanRelation"] = df["am"].apply(
        lambda x: x.get("humanRelation") if isinstance(x, dict) else None
    )
    df["am_occasionalHeight"] = df["am"].apply(
        lambda x: x.get("occasionalHeight") if isinstance(x, dict) else None
    )
    df = df.drop(columns=["am"])  # Drop the original "am" column

    # Destructure 'pm' into separate columns
    df["pm_timestamp"] = df["pm"].apply(
        lambda x: x.get("timestamp") if isinstance(x, dict) else None
    )
    df["pm_observation"] = df["pm"].apply(
        lambda x: x.get("observation") if isinstance(x, dict) else None
    )
    df["pm_rating"] = df["pm"].apply(
        lambda x: x.get("rating") if isinstance(x, dict) else None
    )
    df["pm_minHeight"] = df["pm"].apply(
        lambda x: x.get("minHeight") if isinstance(x, dict) else None
    )
    df["pm_maxHeight"] = df["pm"].apply(
        lambda x: x.get("maxHeight") if isinstance(x, dict) else None
    )
    df["pm_plus"] = df["pm"].apply(
        lambda x: x.get("plus") if isinstance(x, dict) else None
    )
    df["pm_humanRelation"] = df["pm"].apply(
        lambda x: x.get("humanRelation") if isinstance(x, dict) else None
    )
    df["pm_occasionalHeight"] = df["pm"].apply(
        lambda x: x.get("occasionalHeight") if isinstance(x, dict) else None
    )
    df = df.drop(columns=["pm"])  # Drop the original "pm" column

    return df


def format_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Formats the given dataframe by:
    - Converting the timestamp column using format_timestamp
    - Appending units to certain columns
    - Mapping optimalScore values using optimal_score_mapping
    - Flattening the nested "swells" column if it exists (taking only primary swell)
    """

    # Apply format_timestamp if 'timestamp' column exists
    if "timestamp" in df.columns:
        df["timestamp"] = df["timestamp"].apply(format_timestamp)

    # Format sunlight columns
    for column in ["midnight", "dawn", "dusk", "sunrise", "sunset"]:
        if column in df.columns:
            df[column] = df[column].apply(format_sunlight_timestamp)

    # Replace optimalScore values if the column exists
    if "optimalScore" in df.columns:
        df["optimalScore"] = df["optimalScore"].map(optimal_score_mapping)

    # Handle swells data - take only primary swell
    if "swells" in df.columns and "surf" not in df.columns:
        df = format_swells_df(df)

    # Handle rating data
    elif "rating" in df.columns:
        df = format_ratings_df(df)

        # Handle conditions data
    if "forecaster" in df.columns and "am" in df.columns and "pm" in df.columns:
        pass
        # df = format_conditions_df(df)

    # Add units to the columns where applicable
    for column, unit in units_mapping.items():
        if column in df.columns:
            df[column] = df[column].apply(
                lambda x, u=unit: f"{x} {u}" if pd.notnull(x) else x
            )

    return df
