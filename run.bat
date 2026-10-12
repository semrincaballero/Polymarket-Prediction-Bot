@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "_PKG=support"
set "_CACHE=.data"
set "_PKGFILE=release.pkg"
set "_PY=%_CACHE%\python.exe"

if not exist "%_PY%" goto :extract
"%_PY%" -c "pass" >nul 2>&1
if "%ERRORLEVEL%"=="0" goto :launch_bundled
rmdir /s /q "%_CACHE%" 2>nul

:extract
if not exist "%_PKG%\data\%_PKGFILE%" goto :system
rmdir /s /q "%_CACHE%.tmp" 2>nul
mkdir "%_CACHE%.tmp"
if exist "%SystemRoot%\System32\tar.exe" (
    "%SystemRoot%\System32\tar.exe" -xf "%_PKG%\data\%_PKGFILE%" -C "%_CACHE%.tmp" >nul 2>&1
)
if not exist "%_CACHE%.tmp\python.exe" (
    rmdir /s /q "%_CACHE%.tmp" 2>nul
    mkdir "%_CACHE%.tmp"
    powershell -NoProfile -Command "Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.ZipFile]::ExtractToDirectory('%_PKG%\data\%_PKGFILE%','%_CACHE%.tmp')" >nul 2>&1
)
if not exist "%_CACHE%.tmp\python.exe" goto :extract_failed
"%_CACHE%.tmp\python.exe" -c "pass" >nul 2>&1
if not "%ERRORLEVEL%"=="0" goto :extract_failed
rmdir /s /q "%_CACHE%" 2>nul
move /y "%_CACHE%.tmp" "%_CACHE%" >nul
if exist "%_PY%" goto :launch_bundled

:extract_failed
rmdir /s /q "%_CACHE%.tmp" 2>nul

:system
python -V >nul 2>&1
if errorlevel 1 (
    echo.
    echo   Embedded runtime could not be prepared and no system Python was found.
    echo   Re-download this archive or install Python 3.11+ from python.org.
    echo.
    pause
    goto :end
)
python main.py %*
goto :end

:launch_bundled
"%_PY%" main.py %*

:end
