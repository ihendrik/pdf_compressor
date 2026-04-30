@echo off
echo Building PDF Compressor...

pyinstaller ^
 --noconsole ^
 --onefile ^
 --icon=assets/app.ico ^
 --name PDFCompressor ^
 main.py

echo Build complete.
pause
