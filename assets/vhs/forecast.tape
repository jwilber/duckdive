# Output file

Output ../img/forecast.gif

# Require duckdive to be installed

Require duckdive

# Terminal settings

Set Shell "bash"
Set FontSize 28
Set Width 1400
Set Height 800
Set Theme "Dracula"
Set TypingSpeed 40ms

# Introduction

Type "# get today's wind and tide conditions:"
Sleep 500ms
Enter
Type "duckdive forecast -t wind"
Enter
Sleep 4.5s
Type "duckdive forecast -t tides"
Enter
Sleep 4.5s



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

# Save to csv and duckdb

Type "# save to csv or duckdb:"
Enter
Sleep 500ms
Type "duckdive forecast -t swells --csv swells.csv --duckdb swells.duckdb"
Enter
Sleep 4s

# Clear screen

Ctrl+L
Sleep 500ms

