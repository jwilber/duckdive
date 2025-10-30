import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

import duckdb
import pandas as pd
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .api import construct_surfline_api_url
from .query_surfline import query_surfline
from .util import create_pretty_table

app = typer.Typer()
console = Console()


@app.command()
def forecast(
    spot_id: str = typer.Argument("5842041f4e65fad6a7708839", help="Surfline spot ID"),
    days: int = typer.Option(3, help="Number of forecast days"),
    forecast_type: str = typer.Option(
        "tides", "-t", "--forecast-type", help="Forecast type"
    ),
    interval_hours: float = typer.Option(
        1, "-i", "--interval-hours", help="Interval hours for forecast"
    ),
    max_heights: bool = typer.Option(
        True, "-m", "--max-heights", help="Include max heights in output"
    ),
    sds: bool = typer.Option(True, "-s", "--sds", help="Use LOTUS forecast engine"),
    access_token: Optional[str] = typer.Option(
        None, "-a", "--access-token", help="Access token for premium data"
    ),
    save_to_duckdb: bool = typer.Option(
        False, "-d", "--save-to-duckdb", help="Save data to DuckDB"
    ),
    csv: Optional[str] = typer.Option(
        None, "--csv", help="Save the data to a local CSV file"
    ),
):
    """
    Query the Surfline API for forecast data.
    """
    url = construct_surfline_api_url(
        spot_id=spot_id,
        days=days,
        interval_hours=interval_hours,
        max_heights=max_heights,
        sds=sds,
        access_token=access_token,
        forecast_type=forecast_type,
    )
    print("url here sir", url)

    result = query_surfline(url, duckdb_file=duckdb)

    if isinstance(result, duckdb.DuckDBPyConnection):
        if csv:
            # Export to CSV using DuckDB
            result.execute(f"COPY surfline_data TO '{csv}' (HEADER, DELIMITER ',')")
            typer.echo(f"Data saved to {csv}")

        # Display preview
        preview_data = result.execute("SELECT * FROM surfline_data LIMIT 5").fetchall()
        console.print(create_pretty_table(preview_data))

        if save_to_duckdb:
            typer.echo(
                "DuckDB connection returned. You can now run SQL queries on the 'surfline_data' table."
            )
    else:
        typer.echo("No data was returned.", err=True)
