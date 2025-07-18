@echo off
echo Starting optimized build...

REM Use the spec file for faster, controlled builds
python -m PyInstaller --log-level=ERROR main.spec

echo.
echo Build complete! Executable is in the 'dist' folder.
pause 