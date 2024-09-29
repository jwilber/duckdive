import typer
import requests
import json
import pandas as pd
import duckdb
from typing import Optional
from rich.console import Console

from .models import FullResponse
from .util import format_dataframe

console = Console()

def query_surfline(url: str, save_to_duckdb: bool = True) -> Optional[pd.DataFrame]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.surfline.com/',
        'Origin': 'https://www.surfline.com'
    }

    try:
        with console.status("[bold green]Querying Surfline API...") as status:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

        # Parse the JSON response into the FullResponse model
        parsed_data = FullResponse(**data.get('data', {}))
        
       # Handle different types of data
        if parsed_data.tides:
            df = pd.DataFrame([tide.dict() for tide in parsed_data.tides])
            df = format_dataframe(df)  # Apply formatting to the DataFrame
            typer.echo("Tide data retrieved successfully.")

        elif parsed_data.conditions:
            df = pd.DataFrame([conditions.dict() for conditions in parsed_data.conditions])
            df = format_dataframe(df)  # Apply formatting to the DataFrame
            typer.echo("Conditions data retrieved successfully.")

        elif parsed_data.swells:
            df = pd.DataFrame([swells.dict() for swells in parsed_data.swells])
            df = format_dataframe(df)  # Apply formatting to the DataFrame
            typer.echo("Swells data retrieved successfully.")

        elif parsed_data.sunlight:
            df = pd.DataFrame([sunlight.dict() for sunlight in parsed_data.sunlight])
            df = format_dataframe(df)  # Apply formatting to the DataFrame
            typer.echo("Sunlight data retrieved successfully.")

        elif parsed_data.wave:
            df = pd.DataFrame([wave.dict() for wave in parsed_data.wave])
            df = format_dataframe(df)  # Apply formatting to the DataFrame
            typer.echo("Wave data retrieved successfully.")

        elif parsed_data.rating:
            df = pd.DataFrame([rating.dict() for rating in parsed_data.rating])
            df = format_dataframe(df)  # Apply formatting to the DataFrame
            typer.echo("Rating data retrieved successfully.")

        elif parsed_data.wind:
            df = pd.DataFrame([wind.dict() for wind in parsed_data.wind])
            df = format_dataframe(df)  # Apply formatting to the DataFrame
            typer.echo("Wind data retrieved successfully.")

        elif parsed_data.weather:
            df = pd.DataFrame([weather.dict() for weather in parsed_data.weather])
            df = format_dataframe(df)  # Apply formatting to the DataFrame
            typer.echo("Weather data retrieved successfully.")

        else:
            typer.echo("No data found.")
            return None

        if save_to_duckdb:
            con = duckdb.connect(database=':memory:')
            con.execute("CREATE TABLE surfline_data AS SELECT * FROM df")
            typer.echo("Data saved to DuckDB.")
            
            result = con.execute("SELECT * FROM surfline_data LIMIT 5").fetchdf()
            # console.print(create_pretty_table(result))
            return con

        # console.print(create_pretty_table(df))
        return df

    except requests.RequestException as e:
        typer.echo(f"An error occurred while fetching data: {e}", err=True)
    except json.JSONDecodeError as e:
        typer.echo(f"An error occurred while parsing JSON: {e}", err=True)

    return None