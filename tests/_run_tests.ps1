# Store the current working directory.
Push-Location -Path $PSScriptRoot

# Execute tests. -s: disable all stdout/stderr capturing, -v: verbose
& pytest test.py -s -v

# Switch back to the original current working directory.
Pop-Location
