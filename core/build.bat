setlocal EnableDelayedExpansion

rem %~dp0 is the containing directory

rem compression command
pushd %~dp0..
set parentdir=%cd%
popd
rem echo %parentdir%

rem Just in case 7zip is finnicky about automatically creating new zips.
if not exist "%parentdir%\core.zip" (
	7z a -tzip "%parentdir%\core.zip" "%~f0"
)
for %%v in ("%~dp0*") do (
	7z u -tzip "%parentdir%\core.zip" "%%v"
)
for /d %%v in ("%~dp0*") do (
	7z u -tzip "%parentdir%\core.zip" "%%v"
)