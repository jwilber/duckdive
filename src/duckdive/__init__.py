import typer
import pandas as pd
import duckdb
from typing import Optional
from rich.console import Console
from .query_surfline import query_surfline
from .api import construct_surfline_api_url
from .util import create_pretty_table

app = typer.Typer()
console = Console()

@app.command()
def main(
    spot_id: str = typer.Argument("5842041f4e65fad6a7708839", help="Surfline spot ID"),
    days: int = typer.Option(3, help="Number of forecast days"),
    forecast_type: str = typer.Option("tides", "-t", "--forecast-type", help="Forecast type (must be 'rating', 'conditions', 'swells', 'sunlight', 'wave', 'wind', 'tides', or 'weather')"),
    interval_hours: float = typer.Option(1, "-i", "--interval-hours", help="Interval hours for forecast"),
    max_heights: bool = typer.Option(True, "-m", "--max-heights", help="Include max heights in output"),
    sds: bool = typer.Option(True, "-s", "--sds", help="Use LOTUS forecast engine"),
    access_token: Optional[str] = typer.Option(None, "-a", "--access-token", help="Access token for premium data"),
    save_to_duckdb: bool = typer.Option(False, "-d", "--save-to-duckdb", help="Save data to DuckDB"),
    csv: Optional[str] = typer.Option(None, "--csv", help="Save the data to a local CSV file with the given file name")
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
        forecast_type=forecast_type
    )

    result = query_surfline(url, save_to_duckdb)

    if isinstance(result, duckdb.DuckDBPyConnection):
        typer.echo("DuckDB connection returned. You can now run SQL queries on the 'surfline_data' table.")
    elif isinstance(result, pd.DataFrame):
        # Display the data
        console.print(create_pretty_table(result.head()))

        # If the --csv option is provided, save the DataFrame to a CSV file
        if csv:
            result.to_csv(csv, index=False)
            typer.echo(f"Data saved to {csv}")
    else:
        typer.echo("No data was returned.", err=True)

if __name__ == "__main__":
    app()
