# Technical Documentation

## 1. Architecture Overview
UI (PySide6)
↓
Worker Thread (QThread)
↓
Compressor (Ghostscript subprocess)

---

## 2. Core Components

### 2.1 UI Layer (`ui_main.py`)
- Handles user input
- Displays progress and logs
- Connects signals from Worker

---

### 2.2 Worker (`worker.py`)
- Runs in background thread
- Emits signals:
  - `progress` (str)
  - `percent` (int)
  - `done` (bool, float)

---

### 2.3 Compressor (`compressor.py`)
- Builds Ghostscript command
- Executes subprocess
- Parses stdout for progress:
  - `Processing pages X through Y`
  - `Page N`

---

### 2.4 Constants (`constants.py`)
Defines:
```python
PRESET_QUALITY = {
    "Fast": {"dpi": 96, "jpeg": 55},
    "Balanced": {"dpi": 150, "jpeg": 70},
    "High Quality": {"dpi": 220, "jpeg": 85},
}
```

---


## 3. Data Flow
- User selects file
- UI creates Worker
- Worker calls run_gs_with_progress
- Ghostscript processes pages
- Output parsed → progress %
- UI updates progress bar

---


## 4. Ghostscript Command
Example:
```
 gswin64c.exe -sDEVICE=pdfwrite -dNOPAUSE -dBATCH \
-dColorImageResolution=150 \
-dJPEGQ=70 \
-sOutputFile=output.pdf input.pdf
```

---


## 5. Progress Parsing

Regex used:
- Processing pages \d+ through (\d+)
- Page (\d+)

---


## 6. Threading Model
- UI thread → responsive
- Worker thread → heavy processing
- Signals → thread-safe communication

---


## 7. Error Handling
- Missing file → UI alert
- Ghostscript failure → logged
- Cancellation → process terminated

---


## 8. Limitations
- No preview of output
- No OCR support
- Compression depends on PDF structure

---


## 9. Future Enhancements
- Dual mode (Target Size + Quality)
- Drag & drop support
- ETA estimation
- PDF preview
- Batch processing

---
