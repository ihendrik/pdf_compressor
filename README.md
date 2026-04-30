# PDF Compressor (Windows Desktop App)

A modern PySide6-based desktop application for compressing PDF files using Ghostscript, with real-time progress tracking and configurable quality settings.

---

## 🚀 Features

- 📉 Compress PDF files efficiently using Ghostscript
- 🎯 Choose compression via:
  - Presets (Fast / Balanced / High Quality)
  - Manual DPI & JPEG tuning
- 📊 Real-time progress bar (per page)
- 🧾 Live logging panel
- 🪟 Native Windows GUI (PySide6)
- ⚡ Fast execution (no unnecessary iterations)

---

## 🧱 Tech Stack

- Python 3.10+
- PySide6 (Qt for Python)
- Ghostscript (external dependency)

---

## 📦 Installation

### 1. Clone repository

```bash
git clone https://github.com/yourusername/pdf-compressor.git
cd pdf-compressor
```
### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Install Ghostscript
Download from:
```
https://www.ghostscript.com/releases/gsdnld.html
```
Ensure it's installed in:
```
C:\Program Files\gs\
```

▶️ Run the app
```python
python main.py
```

🖥️ Usage
-  Click Select PDF
- Choose output location
- Select:
 - Preset OR
 - Manual DPI & JPEG
- Click Start
- Monitor progress bar

⚙️ Presets
| Preset | DPI | JPEG | Use Case |
| ------ | --- | ---- | -------- |
|Fast|	96|	55|	Smallest size|
|Balanced|	150|	70|	Default|
|High Quality|	220|	85|	Best readability|

🏗️ Build Executable
pyinstaller --onefile --noconsole --icon=assets/app.ico main.py

📁 Project Structure
```
pdf_compressor/
│
├── app/
│   ├── ui_main.py
│   ├── worker.py
│   ├── compressor.py
│   ├── constants.py
│   └── settings.py
│
├── assets/
│   ├── app.ico
│   └── style.qss
│
├── main.py
├── requirements.txt
└── README.md
```
⚠️ Notes
- Ghostscript must be installed
- Works best on scanned/image-heavy PDFs
- Some PDFs cannot be reduced below a certain size

## 🤖 AI Assistance

This project was developed with the assistance of AI tools. Users should review and validate the software before using it in critical environments.
