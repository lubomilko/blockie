# Store the current working directory and change it to the location of this script.
Push-Location -Path $PSScriptRoot

# Remove the build directory to avoid potential issues with the old build.
if(Test-Path 'build')
{
    Remove-Item -Recurse -Force 'build'
}

# Build HTML documentation and save it into the "html" directory in the doc root directory.
sphinx-build -M html src build

# Move back to the original current working directory.
Pop-Location
