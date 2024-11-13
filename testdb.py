import duckdb

# Create a DuckDB connection
conn = duckdb.connect()

# Install and load the http_client extension
conn.execute("INSTALL http_client FROM community;")
conn.execute("LOAD http_client;")

# Fetch data from Surfline API
query = """
WITH __input AS (
    SELECT
        http_get(
            'https://services.surfline.com/kbyg/spots/forecasts/swells?spotId=5842041f4e65fad6a7708839'
        ) AS res
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
    body
FROM __response;
"""

# Execute the query and fetch results
result = conn.execute(query).fetchone()

# Print results
print(f"Status: {result[0]}")
print(f"Reason: {result[1]}")
print("\nResponse body:")
print(result[2])

# Close the connection
conn.close()
