from urllib.parse import urlencode


def construct_surfline_api_url(
    spot_id="5842041f4e65fad6a7708839",
    days=None,
    interval_hours=None,
    max_heights=None,
    sds=None,
    access_token=None,
    forecast_type="wave",
):
    """
    Construct the Surfline API URL based on user input parameters.
    If no parameters are provided, a default URL is returned with only the spotId and forecast_type.

    :param spot_id: String, Surfline spot id
    :param days: Integer, number of forecast days (optional)
    :param interval_hours: Integer, minimum of 1 hour (optional)
    :param max_heights: Boolean, if True, removes min & optimal values from wave data output (optional)
    :param sds: Boolean, if True, uses the new LOTUS forecast engine (optional)
    :param access_token: String, auth token for premium data access (optional)
    :param forecast_type: String, type of data to include (must be one of the valid types)
    :return: String, constructed API URL
    """
    base_url = "https://services.surfline.com/kbyg/spots/forecasts"

    valid_types = [
        "rating",
        "conditions",
        "swells",
        "sunlight",
        "wave",
        "wind",
        "tides",
        "weather",
    ]
    if forecast_type not in valid_types:
        raise ValueError(f"Invalid forecast_type. Must be one of {valid_types}")

    params = {"spotId": spot_id}

    if days is not None:
        max_days = 17 if access_token else 6
        if days < 1 or days > max_days:
            raise ValueError("Days must be between 1 and 6 (or 17 with premium token)")
        params["days"] = days

    if interval_hours is not None:
        if interval_hours < 1:
            raise ValueError("Interval hours must be at least 1")
        params["intervalHours"] = interval_hours

    if max_heights is not None:
        params["maxHeights"] = str(max_heights).lower()

    if sds is not None:
        params["sds"] = str(sds).lower()

    if access_token:
        params["accesstoken"] = access_token

    url = f"{base_url}/{forecast_type}?{urlencode(params)}"
    return url


if __name__ == "__main__":
    # Case where no extra parameters are provided, defaults to wave and spotId
    default_url = construct_surfline_api_url()
    print(f"Default URL: {default_url}")

    # Case where additional parameters are provided
    try:
        custom_url = construct_surfline_api_url(
            spot_id="5842041f4e65fad6a7708839",
            days=3,
            interval_hours=3,
            max_heights=True,
            sds=True,
            forecast_type="wind",
        )
        print(f"Custom URL: {custom_url}")
    except ValueError as e:
        print(f"Error: {e}")
