@ECHO OFF

rem Store the current working directory and move into the directory containing this bat file.
pushd %~dp0

rem Remove the entire "build" directory for Sphinx build files and create a new empty one.
if exist build\ (
    rmdir /s /q build
)

rem Build the HTML documentand save it into the "html" dir.
sphinx-build -M html src build %O%

rem Move back to the original current working directory.
popd
