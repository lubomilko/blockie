REM Store the current working dir and switch to the directory where this bat file is located, 
REM because all paths in tests are relative to the test dir.
@pushd %~dp0

REM Execute tests. -s: disable all stdout/stderr capturing, -v: verbose
pytest test.py -s -v

REM Switch back to the original current working directory.
@popd
