import json, os
from pathlib import Path

APP_DIR = Path(os.getenv("APPDATA", ".")) / "PDFCompressor"
APP_DIR.mkdir(exist_ok=True)

SETTINGS_FILE = APP_DIR / "settings.json"

DEFAULT = {
    "ghostscript_path": "",
    "preset": "Balanced",
    "max_size": 200
}

def load_settings():
    if SETTINGS_FILE.exists():
        return json.loads(SETTINGS_FILE.read_text())
    return DEFAULT.copy()

def save_settings(cfg):
    SETTINGS_FILE.write_text(json.dumps(cfg, indent=2))