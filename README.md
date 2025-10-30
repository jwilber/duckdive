# duckdive

Query Surfline surf forecast data from your CLI and save it to csv or DuckDB.

## Installation

```bash
# Using uv (recommended)
uv pip install duckdive


## Development

First, clone the repo:

```bash
git clone https://github.com/jwilber/duckdive.git
```

Create an environment:
```bash
```

Install the module:
```bash
pip install -e
```

Then run the module:
```bash
duckdive -t swells --csv "tides_data.csv"
```

We're using `uv` for development. To get up and running, use the following command:

```bash
# Get tide forecast for default spot (El Porto)
duckdive forecast

# Get wave forecast and save to CSV
duckdive forecast -t wave --csv waves.csv

# Generate daily surf report for multiple spots
duckdive report

# Save report to DuckDB
duckdive report --duckdb today.duckdb
```

## Commands

### `duckdive forecast`

Query a single forecast type for a single spot.

```bash
# Get 5-day wave forecast
duckdive forecast -t wave --days 5

# Get wind data with 3-hour intervals
duckdive forecast -t wind -i 3 --csv wind.csv

# Save to DuckDB
duckdive forecast -t tides --duckdb tides.duckdb

# Different spot (use Surfline spot ID)
duckdive forecast 5842041f4e65fad6a770881b -t wave
```

**Options:**

| Option                 | Description                               | Default                  |
| ---------------------- | ----------------------------------------- | ------------------------ |
| `spot_id`              | Surfline spot ID                          | 5842041f4e65fad6a7708839 |
| `-t, --forecast-type`  | Forecast type (see available types below) | tides                    |
| `--days`               | Number of forecast days                   | 3                        |
| `-i, --interval-hours` | Interval in hours for forecast data       | 1                        |
| `-m, --max-heights`    | Include maximum heights in output         | True                     |
| `-s, --sds`            | Use LOTUS forecast engine                 | True                     |
| `-a, --access-token`   | Access token for premium Surfline data    | None                     |
| `--csv`                | Save to CSV file                          | None                     |
| `--duckdb`             | Save to DuckDB file                       | None                     |

### `duckdive report`

Generate a comprehensive surf report with multiple forecast types across multiple spots.

```bash
# Generate today's report (7am-8pm, simplified view)
duckdive report

# Full 3-day report for all spots
duckdive report --no-today --no-simplify

# Specific forecast types only
duckdive report --types wave --types wind --types tides

# Custom spots via CLI
duckdive report --spot-ids 5842041f4e65fad6a7708839 --spot-ids 5842041f4e65fad6a77088bd

# Save outputs
duckdive report --csv report.csv --duckdb report.duckdb
```

**Options:**

| Option                     | Description                         | Default            |
| -------------------------- | ----------------------------------- | ------------------ |
| `-s, --spot-ids`           | List of Surfline spot IDs           | From JSON or error |
| `--days`                   | Number of forecast days             | 3                  |
| `-i, --interval-hours`     | Interval in hours for forecast data | 1                  |
| `-t, --types`              | Specific forecast types to fetch    | all                |
| `--simplify/--no-simplify` | Return simplified column subset     | True               |
| `--today/--no-today`       | Only include today's data (7am-8pm) | True               |
| `--csv`                    | Save to CSV file                    | None               |
| `--duckdb`                 | Save to DuckDB file                 | None               |

## Configuration

### Spot Configuration

Create a `duckdive_spots.json` file in your working directory to define your default spots:

```json
{
  "el_porto": "5842041f4e65fad6a7708839",
  "manhattan_beach": "5842041f4e65fad6a77088bd",
  "hermosa_beach": "5842041f4e65fad6a7708978",
  "redondo_beach": "5842041f4e65fad6a77089a2"
}
```

The `report` command will use these spots by default. You can override with `--spot-ids`.

## Forecast Types

Available forecast types:

- `rating` - Surf quality rating
- `conditions` - Overall surf conditions
- `swells` - Swell data (height, period, direction)
- `wave` - Wave heights and surf data
- `wind` - Wind speed, direction, and gusts
- `tides` - Tide heights and timing
- `weather` - Temperature and conditions

## Data Storage

### CSV Export

```bash
duckdive forecast -t wave --csv waves.csv
duckdive report --csv daily_report.csv
```

### DuckDB Export

```bash
duckdive forecast -t wave --duckdb surfline.duckdb
duckdive report --duckdb report.duckdb
```

Query your DuckDB files:

```bash
# Using DuckDB CLI
duckdb surfline.duckdb "SELECT * FROM surfline_data LIMIT 10"

# Or in Python
import duckdb
con = duckdb.connect('surfline.duckdb')
df = con.execute('SELECT * FROM surfline_data').df()
```

## Data Models

### Rating

| Field     | Type   | Description             |
| --------- | ------ | ----------------------- |
| timestamp | int    | Timestamp of the rating |
| rating    | object | Rating value data       |

### Conditions

| Field       | Type   | Description                    |
| ----------- | ------ | ------------------------------ |
| timestamp   | int    | Timestamp of the conditions    |
| forecastDay | str    | Forecast day                   |
| forecaster  | object | Forecaster information         |
| human       | bool   | Whether forecast is by a human |
| observation | str    | Observation text               |
| am          | object | Morning observation data       |
| pm          | object | Evening observation data       |

### Swells

| Field       | Type  | Description                 |
| ----------- | ----- | --------------------------- |
| timestamp   | int   | Timestamp of the swell data |
| probability | float | Probability of the swell    |
| power       | float | Power of the swell          |
| swells      | list  | List of swell details       |

### Tides

| Field     | Type  | Description                |
| --------- | ----- | -------------------------- |
| timestamp | int   | Timestamp of the tide data |
| type      | str   | Type of tide (HIGH/LOW)    |
| height    | float | Height of the tide (ft)    |

### Wave

| Field       | Type   | Description                |
| ----------- | ------ | -------------------------- |
| timestamp   | int    | Timestamp of the wave data |
| probability | float  | Probability of the wave    |
| surf        | object | Surf height data           |
| power       | float  | Power of the wave          |
| swells      | list   | List of swell data         |

### Wind

| Field         | Type  | Description                       |
| ------------- | ----- | --------------------------------- |
| timestamp     | int   | Timestamp of the wind data        |
| speed         | float | Wind speed (mph)                  |
| gust          | float | Wind gust speed (mph)             |
| direction     | float | Wind direction (degrees)          |
| directionType | str   | Wind direction type (ONSHORE/etc) |
| optimalScore  | int   | Optimal score for conditions      |

### Weather

| Field       | Type            | Description                   |
| ----------- | --------------- | ----------------------------- |
| timestamp   | int             | Timestamp of the weather data |
| temperature | Optional[float] | Temperature                   |
| pressure    | Optional[float] | Atmospheric pressure          |
| condition   | str             | Weather condition description |


Reduced dependencies
More efficient data processing (data stays in DuckDB)
Better memory usage (no pandas DataFrame intermediary)
Simpler data pipeline
