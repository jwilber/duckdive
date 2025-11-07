# Output file

Output ../img/readme.gif

# Require duckdive to be installed

Require duckdive

# Terminal settings

Set Shell "bash"
Set FontSize 29
Set Width 1800
Set Height 1300
Set Theme "Dracula"
Set TypingSpeed 40ms

# Introduction

Type "# get today's wind conditions:"
Sleep 500ms
Enter
Type "duckdive forecast -t wind"
Enter
Sleep 4s

# Clear screen

Ctrl+L
Sleep 500ms

# Show ratings

Type "# get surfline's ratings:"
Sleep 500ms
Enter
Type "duckdive forecast -t rating"
Enter
Sleep 4s

# Clear screen

Ctrl+L
Sleep 500ms

Type "# Generate the report for today's full forecast (and, optionally, save to duckdb):"
Enter
Sleep 500ms
Type "duckdive report --duckdb lj_today.duckdb"
Enter
Sleep 8s

# Clear screen

Ctrl+L
Sleep 500ms

Type "# Query the data from duckdb"
Enter
Sleep 500ms
Type `duckdb lj_today.duckdb "SELECT * FROM surfline_data LIMIT 5"`
Enter
Sleep 4s