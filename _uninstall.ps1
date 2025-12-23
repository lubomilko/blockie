# Upgrade pip to ensure that latest features are available.
python -m pip install --upgrade pip
# Get the package name from the first directory within the '.\src' subdirectory.
$pkgName = Get-ChildItem -Path (Join-Path -Path $PsScriptRoot -ChildPath 'src') -Directory | Select-Object -First 1 -ExpandProperty Name
# Uninstall the package.
python -m pip uninstall -y $pkgName
