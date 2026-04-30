[Setup]
AppName=PDF Compressor
AppVersion=1.0
DefaultDirName={pf}\PDFCompressor

[Files]
Source: "dist\main.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\PDF Compressor"; Filename: "{app}\main.exe"