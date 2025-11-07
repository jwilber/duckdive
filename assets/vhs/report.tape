# Output file

Output ../img/report.gif

# Require duckdive to be installed

Require duckdive

# Terminal settings

Set Shell "bash"
Set FontSize 28
Set Width 1800
Set Height 1200
Set Theme "Dracula"
Set TypingSpeed 40ms

# Introduction

# Show the spots config

Type "# get full forecasts for multiple spots:"
Enter
Sleep 500ms
Type "# first, save spot ids to duckdive_spots.json:"
Enter
Sleep 500ms
Type "cat duckdive_spots.json"
Enter
Sleep 2s

Ctrl+L
Sleep 500ms
Type "# Then, generate the report for today's full forecast:"
Enter
Sleep 500ms
Type "duckdive report --duckdb lj_today.duckdb"
Enter
Sleep 8s

# Clear screen

Ctrl+L
Sleep 500ms

Type "# Query data from duckdb"
Enter
Sleep 500ms
Type `duckdb lj_today.duckdb "SELECT * FROM surfline_data LIMIT 5"`
Enter
Sleep 4s
