:: Store the current working dir and switch to the directory where this bat file is located, because all paths below are relative to this dir.
:: %~dp0 contains the dir path of this bat file.
@pushd %~dp0

:: Execute tests. -s: disable all stdout/stderr capturing, -v: verbose
pytest test.py -s -v

:: Switch back to the original current working directory.
@popd
