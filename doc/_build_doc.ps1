# Store the current working directory and change it to the location of this script.
Push-Location -Path $PSScriptRoot

# Build HTML documentation and save it into the "build\html" directory.
sphinx-build -M html src build

# Move back to the original current working directory.
Pop-Location
