
# Store the current working directory and change it to the root dir of this script.
Push-Location -Path $PSScriptRoot

# Upgrade pip to ensure that latest features are avialable.
python -m pip install --upgrade pip
# Get the package name from the first directory within the '.\src' subdirectory.
$pkgName = Get-ChildItem -Path (Join-Path -Path $PsScriptRoot -ChildPath 'src') -Directory | Select-Object -First 1 -ExpandProperty Name
# Install the package.
if(Test-Path requirements.txt){
    python -m pip install $pkgName --no-index --find-links dist --requirement requirements.txt
}
else {
    python -m pip install $pkgName --no-index --find-links dist
}

# Switch back to the original current working directory.
Pop-Location
