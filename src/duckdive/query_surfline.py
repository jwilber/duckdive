import typer
import json
import duckdb
from typing import Optional

import duckdb
import pandas as pd
import requests
import typer
from rich.console import Console
from .models import FullResponse

console = Console()


def query_surfline(
    url: str, save_to_duckdb: bool = True
) -> Optional[duckdb.DuckDBPyConnection]:
    try:
        # Initialize DuckDB connection
        con = duckdb.connect()

        # Install and load HTTP client extension
        con.execute("INSTALL http_client FROM community;")
        con.execute("LOAD http_client;")

        with console.status("[bold green]Querying Surfline API...") as status:
            # Make HTTP request using DuckDB
            query = """
            WITH __input AS (
                SELECT http_get($1) AS res
            ),
            __response AS (
                SELECT 
                    (res->>'status')::INT AS status,
                    (res->>'reason') AS reason,
                    (res->>'body')::JSON AS body
                FROM __input
            )
            SELECT 
                status,
                reason,
                body->>'data' AS data
            FROM __response;
            """
            result = con.execute(query, [url]).fetchone()

        if result[0] != 200:  # Check status code
            typer.echo(f"API request failed with status {result[0]}: {result[1]}")
            return None

        # Parse the JSON response into the FullResponse model
        parsed_data = FullResponse(**json.loads(result[2]))

        # Define data type mapping
        data_types = {
            "tides": (parsed_data.tides, "Tide"),
            "conditions": (parsed_data.conditions, "Conditions"),
            "swells": (parsed_data.swells, "Swells"),
            "sunlight": (parsed_data.sunlight, "Sunlight"),
            "wave": (parsed_data.wave, "Wave"),
            "rating": (parsed_data.rating, "Rating"),
            "wind": (parsed_data.wind, "Wind"),
            "weather": (parsed_data.weather, "Weather"),
        }

        # Find which data type we have and create table
        for data_type, (data, message) in data_types.items():
            if data:
                records = [item.dict() for item in data]
                con.execute(
                    "CREATE TABLE surfline_data AS SELECT * FROM json_array_to_table($1)",
                    [json.dumps(records)],
                )
                typer.echo(f"{message} data retrieved successfully.")

                if save_to_duckdb:
                    return con
                else:
                    return con

        typer.echo("No data found.")
        return None

    except Exception as e:
        typer.echo(f"An error occurred: {e}", err=True)
        return None
