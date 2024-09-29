# duckdive

Query surfline data from your cli, and (optionally) store it with pandas or duckdb.

todo: finish this

## Installation

[Installation instructions to be added]

## Development

We're using `uv` for development. To get up and running, use the following command:

```bash
uv run duckdive -t swells --csv "tides_data.csv"
```

## API

| Field          | Description                                                                                                       |
| :------------- | :---------------------------------------------------------------------------------------------------------------- |
| spot_id        | Surfline spot ID (default: 5842041f4e65fad6a7708839).                                                             |
| days           | Number of forecast days (default: 3).                                                                             |
| forecast_type  | Forecast type, options include: 'rating', 'conditions', 'swells', 'sunlight', 'wave', 'wind', 'tides', 'weather'. |
| interval_hours | Interval in hours for forecast data (default: 1).                                                                 |
| max_heights    | Include maximum heights in the output (default: True).                                                            |
| sds            | Use the LOTUS forecast engine (default: True).                                                                    |
| access_token   | Optional access token for premium Surfline data.                                                                  |
| save_to_duckdb | Save the data directly to DuckDB (default: False).                                                                |
| csv            | Save the data to a local CSV file if a file name is provided.                                                     |

## Data Models

The api exposes several models.

### Rating

| Field     | Type            | Description             |
| --------- | --------------- | ----------------------- |
| timestamp | int             | Timestamp of the rating |
| rating    | RatingValueData | Rating value data       |

### Conditions

| Field       | Type                      | Description                        |
| ----------- | ------------------------- | ---------------------------------- |
| timestamp   | int                       | Timestamp of the conditions        |
| forecastDay | str                       | Forecast day                       |
| forecaster  | Optional[ForecasterData]  | Forecaster information             |
| human       | bool                      | Whether the forecast is by a human |
| observation | Optional[str]             | Observation text                   |
| am          | Optional[ObservationData] | Morning observation data           |
| pm          | Optional[ObservationData] | Evening observation data           |

### Sunlight

| Field    | Type | Description            |
| -------- | ---- | ---------------------- |
| midnight | int  | Timestamp for midnight |
| dawn     | int  | Timestamp for dawn     |
| sunrise  | int  | Timestamp for sunrise  |
| sunset   | int  | Timestamp for sunset   |
| dusk     | int  | Timestamp for dusk     |

### Swells

| Field       | Type               | Description                 |
| ----------- | ------------------ | --------------------------- |
| timestamp   | int                | Timestamp of the swell data |
| probability | Optional[float]    | Probability of the swell    |
| power       | Optional[float]    | Power of the swell          |
| swells      | List[SwellDetails] | List of swell details       |

### Tides

| Field     | Type  | Description                |
| --------- | ----- | -------------------------- |
| timestamp | int   | Timestamp of the tide data |
| type      | str   | Type of tide (high/low)    |
| height    | float | Height of the tide         |

### Wave

| Field       | Type                      | Description                |
| ----------- | ------------------------- | -------------------------- |
| timestamp   | int                       | Timestamp of the wave data |
| probability | Optional[float]           | Probability of the wave    |
| surf        | SurfData                  | Surf data                  |
| power       | Optional[float]           | Power of the wave          |
| swells      | Optional[List[SwellData]] | List of swell data         |

### Wind

| Field         | Type            | Description                       |
| ------------- | --------------- | --------------------------------- |
| timestamp     | int             | Timestamp of the wind data        |
| speed         | float           | Wind speed                        |
| gust          | Optional[float] | Wind gust speed                   |
| direction     | Optional[float] | Wind direction in degrees         |
| directionType | Optional[str]   | Wind direction type               |
| optimalScore  | Optional[int]   | Optimal score for wind conditions |

### Weather

| Field       | Type            | Description                   |
| ----------- | --------------- | ----------------------------- |
| timestamp   | int             | Timestamp of the weather data |
| temperature | Optional[float] | Temperature                   |
| pressure    | Optional[float] | Atmospheric pressure          |
| condition   | str             | Weather condition description |
