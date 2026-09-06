"""
paths.py
--------
Single source of truth for every path in the project.

Everything is resolved from the repository root, so scripts work no matter
which directory you run them from.
"""

from pathlib import Path

# src/paths.py -> src/ -> repository root
ROOT = Path(__file__).resolve().parents[1]

# ── Data ──
DATA_ROOT = ROOT / "data"
DATA_DIR = DATA_ROOT / "2nd_test" / "2nd_test"   # ที่อยู่จริงของไฟล์ 984 ไฟล์
DATA_DIR_FALLBACK = DATA_ROOT / "2nd_test"       # เผื่อแตกไฟล์แบบไม่มีโฟลเดอร์ซ้อน
IMS_RAR = ROOT / "IMS" / "IMS" / "2nd_test.rar"

# ── Training artifacts ──
OUTPUT_DIR = ROOT / "outputs"
RESULTS_JSON = OUTPUT_DIR / "comparison_results.json"
FEATURES_CACHE = OUTPUT_DIR / "features_cache.npz"

# ── Generated HTML report (also the GitHub Pages root) ──
DOCS_DIR = ROOT / "docs"
ASSETS_DIR = DOCS_DIR / "assets"

# ── Third-party extraction tools ──
TOOLS_DIR = ROOT / "tools"


def resolve_data_dir() -> Path:
    """Return the folder that actually holds the IMS files."""
    if DATA_DIR.is_dir():
        return DATA_DIR
    return DATA_DIR_FALLBACK
