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


def load_spot_config() -> Dict[str, str]:
    """
    Load spot configuration from duckdive_spots.json file.
    Returns dict mapping spot_id -> spot_name if file exists, empty dict otherwise.
    """
    spots_file = Path.cwd() / "duckdive_spots.json"
    if spots_file.exists():
        with open(spots_file) as f:
            data = json.load(f)
            # Return inverted dict: {spot_id: spot_name}
            return {v: k for k, v in data.items()}
    return {}


def get_spot_name(spot_id: str, spot_config: Dict[str, str]) -> str:
    """Get friendly name for spot_id, or return spot_id if not found."""
    return spot_config.get(spot_id, spot_id)


@app.command()
def forecast(
    spot_id: str = typer.Argument("5842041f4e65fad6a7708839", help="Surfline spot ID"),
    days: int = typer.Option(3, help="Number of forecast days"),
    forecast_type: str = typer.Option(
        "tides",
        "-t",
        "--forecast-type",
        help=(
            "Forecast type (must be 'rating', 'conditions', 'swells',"
            " 'sunlight', 'wave', 'wind', 'tides', or 'weather')"
        ),
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
    duckdb: Optional[str] = typer.Option(
        None, "--duckdb", help="Save data to DuckDB file (e.g., surfline.duckdb)"
    ),
    csv: Optional[str] = typer.Option(
        None, "--csv", help="Save the data to a local CSV file with the given file name"
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

    result = query_surfline(url, duckdb_file=duckdb)

    if isinstance(result, pd.DataFrame):
        console.print(create_pretty_table(result.head()))
        if csv:
            result.to_csv(csv, index=False)
            typer.echo(f"Data saved to {csv}")
    else:
        typer.echo("No data was returned.", err=True)


@app.command()
def report(
    spot_ids: Optional[List[str]] = typer.Option(
        None,
        "--spot-ids",
        "-s",
        help="List of Surfline spot IDs (e.g., 5842041f4e65fad6a7708839 for Scripps)",
    ),
    days: int = typer.Option(3, help="Number of forecast days"),
    interval_hours: float = typer.Option(
        1, "-i", "--interval-hours", help="Interval hours for forecast"
    ),
    max_heights: bool = typer.Option(
        True, "-m", "--max-heights", help="Include max heights in output"
    ),
    sds: bool = typer.Option(True, "--sds", help="Use LOTUS forecast engine"),
    access_token: Optional[str] = typer.Option(
        None, "-a", "--access-token", help="Access token for premium data"
    ),
    duckdb: Optional[str] = typer.Option(
        None, "--duckdb", help="Save data to DuckDB file (e.g., report.duckdb)"
    ),
    csv: Optional[str] = typer.Option(
        None, "--csv", help="Save the data to a local CSV file with the given file name"
    ),
    forecast_types: Optional[List[str]] = typer.Option(
        None, "--types", "-t", help="Specific forecast types to fetch (default: all)"
    ),
    simplify: bool = typer.Option(
        True,
        "--simplify/--no-simplify",
        help="Return simplified subset of columns only",
    ),
    today: bool = typer.Option(
        True,
        "--today/--no-today",
        help="Only include data for today's date",
    ),
):
    """
    Generate a daily surf report for multiple spots with combined forecast data.
    """
    # Load spot config for name mapping
    spot_config = load_spot_config()

    # Load spot IDs from CLI args or JSON file
    if spot_ids is None:
        if spot_config:
            spot_ids = list(spot_config.keys())
        else:
            console.print(
                "[red]Error: No spot_ids specified![/red]\n\n"
                "Either provide spot_ids directly:\n"
                "  duckdive report --spot-ids 5842041f4e65fad6a7708839\n\n"
                "Or create a duckdive_spots.json file with spot mappings:\n"
                "  {\n"
                '    "scripps": "5842041f4e65fad6a7708839",\n'
                '    "blacks": "5842041f4e65fad6a770881b"\n'
                "  }\n\n"
                "Read more: https://github.com/jwilber/duckdive/tree/main"
            )
            raise typer.Exit(code=1)

    all_forecast_types = [
        "rating",
        "conditions",
        "swells",
        "wave",
        "wind",
        "tides",
        "weather",
    ]
    types_to_fetch = forecast_types if forecast_types else all_forecast_types

    for ft in types_to_fetch:
        if ft not in all_forecast_types:
            typer.echo(f"Invalid forecast type: {ft}", err=True)
            raise typer.Exit(code=1)

    all_data = {}
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for spot_id in spot_ids:
            spot_data = {}
            spot_name = get_spot_name(spot_id, spot_config)
            task = progress.add_task(
                f"Fetching data for spot {spot_name}...",
                total=len(types_to_fetch),
            )
            for forecast_type in types_to_fetch:
                progress.update(
                    task,
                    description=f"Fetching {forecast_type} data for spot {spot_name}...",
                )
                try:
                    url = construct_surfline_api_url(
                        spot_id=spot_id,
                        days=days,
                        interval_hours=interval_hours,
                        max_heights=max_heights,
                        sds=sds,
                        access_token=access_token,
                        forecast_type=forecast_type,
                    )
                    result = query_surfline(url, save_to_duckdb=False, verbose=False)
                    if isinstance(result, pd.DataFrame) and not result.empty:
                        cols_to_rename = {
                            col: f"{forecast_type}_{col}"
                            for col in result.columns
                            if col not in ["timestamp", "spot_id"]
                        }
                        result = result.rename(columns=cols_to_rename)
                        result["spot_id"] = spot_id
                        spot_data[forecast_type] = result
                except Exception as e:
                    console.print(
                        f"[red]Error fetching {forecast_type} data for spot {spot_name}: {e}[/red]"
                    )
                progress.advance(task)

            if spot_data:
                merged_df = None
                for df in spot_data.values():
                    merged_df = (
                        df
                        if merged_df is None
                        else pd.merge(
                            merged_df, df, on=["timestamp", "spot_id"], how="outer"
                        )
                    )
                all_data[spot_id] = merged_df

    if all_data:
        final_df = pd.concat(all_data.values(), ignore_index=True)
        final_df["timestamp"] = pd.to_datetime(final_df["timestamp"], format="mixed")

        if simplify:
            if (
                "wave_surf_max" in final_df.columns
                and "wave_surf_min" in final_df.columns
            ):

                def fill_min(row):
                    if pd.isna(row["wave_surf_min"]):
                        try:
                            return row["wave_surf_max"] - 1
                        except Exception:
                            return row["wave_surf_max"]
                    return row["wave_surf_min"]

                final_df["wave_surf_min"] = final_df.apply(fill_min, axis=1)
                final_df["wave_surf"] = (
                    final_df["wave_surf_min"].astype(str)
                    + "-"
                    + final_df["wave_surf_max"].astype(str)
                    + "ft"
                )
            elif "wave_surf" in final_df.columns:

                def format_ws(ws):
                    if isinstance(ws, dict):
                        minv = ws.get("min") or ws.get("max") - 1
                        maxv = ws.get("max") or 0
                        return f"{int(minv)}-{int(maxv)}ft"
                    return str(ws)

                final_df["wave_surf"] = final_df["wave_surf"].apply(format_ws)

            # Map spot_id to spot name using config
            final_df["spot"] = final_df["spot_id"].apply(
                lambda x: get_spot_name(x, spot_config)
            )
            cols_order = [
                "timestamp",
                "spot",
                "wave_surf",
                "rating_rating_key",
                "tides_type",
                "tides_height",
                "rating_rating_value",
                "swells_height",
                "swells_period",
                "wind_directionType",
                "weather_temperature",
                "weather_condition",
            ]
            final_df = final_df[cols_order]

        if today:
            today_date = datetime.now().date()
            mask = (
                (final_df["timestamp"].dt.date == today_date)
                & (final_df["timestamp"].dt.hour >= 7)
                & (final_df["timestamp"].dt.hour <= 20)
            )
            final_df = final_df[mask]

            # Extract hour for sorting and formatting
            final_df["hour"] = final_df["timestamp"].dt.hour

            # Sort by hour desc, then spot asc
            final_df = final_df.sort_values(["hour", "spot"], ascending=[False, True])

            # Format timestamp to '6pm', '7pm', ...
            final_df["timestamp"] = final_df["hour"].apply(
                lambda h: f"{(h % 12) or 12}{'am' if h < 12 else 'pm'}"
            )

            # Drop helper column
            final_df = final_df.drop(columns=["hour"])
        else:
            sort_cols = ["timestamp", "spot"] if simplify else ["timestamp", "spot_id"]
            final_df = final_df.sort_values(sort_cols, ascending=[False, True])

        console.print(
            f"\n[green]Successfully fetched data for {len(spot_ids)} spot(s)"
            f" with {len(types_to_fetch)} forecast type(s)[/green]"
        )
        console.print(f"Total rows: {len(final_df)}")
        console.print(f"Columns: {', '.join(final_df.columns)}\n")
        console.print(create_pretty_table(final_df.head(10)))

        if csv:
            final_df.to_csv(csv, index=False)
            console.print(f"\n[green]Data saved to {csv}[/green]")

        if duckdb:
            con = duckdb.connect(database=duckdb)
            con.execute(
                "CREATE OR REPLACE TABLE surfline_data AS SELECT * FROM final_df"
            )
            con.close()
            console.print(f"\n[green]Data saved to {duckdb}[/green]")
        return final_df

    else:
        typer.echo("No data was retrieved.", err=True)
        return None


if __name__ == "__main__":
    app()
