"""
extract_data.py — Extract IMS 2nd_test.rar to data/2nd_test/
Usage: python extract_data.py
"""

import os
import sys

RAR_PATH = os.path.join("IMS", "IMS", "2nd_test.rar")
OUT_DIR  = os.path.join("data", "2nd_test")


def check_already_extracted():
    if os.path.isdir(OUT_DIR):
        files = [f for f in os.listdir(OUT_DIR)
                 if os.path.isfile(os.path.join(OUT_DIR, f))]
        if len(files) > 0:
            print(f"[OK] Found {len(files)} files already in {OUT_DIR}")
            return True
    return False


def extract_with_rarfile():
    try:
        import rarfile
    except ImportError:
        print("[ERROR] rarfile not installed. Run: pip install rarfile")
        return False

    if not os.path.isfile(RAR_PATH):
        print(f"[ERROR] RAR file not found: {RAR_PATH}")
        return False

    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"[INFO] Extracting {RAR_PATH} -> {OUT_DIR} ...")
    print("[INFO] This may take a while (~85 MB)...")

    try:
        with rarfile.RarFile(RAR_PATH) as rf:
            members = rf.infolist()
            print(f"[INFO] Found {len(members)} files in archive")
            for i, member in enumerate(members):
                rf.extract(member, OUT_DIR)
                if (i + 1) % 100 == 0:
                    print(f"  Extracted {i+1}/{len(members)}...")
        print(f"[OK] Extraction complete! Files at: {os.path.abspath(OUT_DIR)}")
        return True
    except rarfile.NeedFirstVolume:
        print("[ERROR] Multi-part RAR — use 7-Zip instead")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("  IMS 2nd_test Data Extractor")
    print("=" * 50)

    if check_already_extracted():
        print("[OK] Skipping extraction (data already present)")
        sys.exit(0)

    success = extract_with_rarfile()

    if not success:
        print("\n[HELP] Manual extraction steps:")
        print(f"  1. Download 7-Zip from https://www.7-zip.org/")
        print(f"  2. Right-click {RAR_PATH}")
        print(f"  3. Extract to -> data\\2nd_test\\")
        sys.exit(1)

