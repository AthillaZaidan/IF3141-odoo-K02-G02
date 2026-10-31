@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "PROJECT_DIR=%%~fI"
set "DUMP_DIR=%PROJECT_DIR%\dump"

docker compose version >nul 2>&1
if %errorlevel%==0 (
	set "DC=docker compose"
) else (
	docker-compose --version >nul 2>&1
	if %errorlevel%==0 (
		set "DC=docker-compose"
	) else (
		echo Error: neither "docker compose" nor "docker-compose" is available.
		exit /b 1
	)
)

for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "TS=%%I"

set "OUT_FILE=%~1"
if "%OUT_FILE%"=="" set "OUT_FILE=%DUMP_DIR%\odoo_backup_%TS%.dump"
set "FS_FILE=%OUT_FILE:.dump=_filestore.tar.gz%"

pushd "%PROJECT_DIR%" || exit /b 1
if not exist "%DUMP_DIR%" mkdir "%DUMP_DIR%"

echo Starting db container...
%DC% up -d --wait db || goto :error

echo Exporting database to: %OUT_FILE%
%DC% exec -T db sh -c "pg_dump -U \"$POSTGRES_USER\" -d \"$ODOO_DB_NAME\" -Fc" > "%OUT_FILE%" || goto :error
for %%A in ("%OUT_FILE%") do if %%~zA==0 (
	echo Error: database dump is empty.
	goto :error
)

echo Exporting filestore to: %FS_FILE%
%DC% run --rm --no-deps -T --entrypoint tar web czf - -C /var/lib/odoo . > "%FS_FILE%" || goto :error
for %%A in ("%FS_FILE%") do if %%~zA==0 (
	echo Error: filestore archive is empty.
	goto :error
)

echo Done. Backup files:
echo   DB:        %OUT_FILE%
echo   Filestore: %FS_FILE%
popd
exit /b 0

:error
if exist "%OUT_FILE%" del "%OUT_FILE%"
if exist "%FS_FILE%" del "%FS_FILE%"
echo Export failed.
popd
exit /b 1
