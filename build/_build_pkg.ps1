# Store the current working directory and change it to the tool's root dir.
Push-Location -Path (Join-Path -Path $PSScriptRoot -ChildPath '..')

# Set paths to the directories with built distribution packages and with egg-info files.
$BuildPaths =   (Join-Path -Path $PSScriptRoot -ChildPath '..\dist'),
                (Join-Path -Path $PSScriptRoot -ChildPath "*.egg-info")

foreach($BuildPath in $BuildPaths)
{
    # Remove directory if it exists.
    if(Test-Path -Path $BuildPath)
    {
        Remove-Item -Path $BuildPath -Force -Recurse
    }
}

# Upgrade pip to ensure that latest features are avialable.
python -m pip install --upgrade pip
# Install build package to ensure it can be executed.
python -m pip install build
# Build new package distribution files.
python -m build

# Switch back to the original current working directory.
Pop-Location
