"""
Run this from inside your git repo folder
(the one where 'git status' worked — likely "identite-cosmetics-site (4)").

It copies the two updated files from your new download folder
("identite-cosmetics-site (5)") into this repo, overwriting the old ones.

Usage:
    python copy_update.py
"""

import shutil
from pathlib import Path

# ---- EDIT THIS if your folder numbers are different ----
SOURCE_DOWNLOAD_FOLDER = Path(r"C:\Users\prest\Downloads\identite-cosmetics-site (5)\identite-cosmetics-site")
# ----------------------------------------------------------

DEST_REPO_FOLDER = Path.cwd()  # assumes you run this FROM the repo folder

files_to_copy = [
    Path("static/css/style.css"),
    Path("templates/index.html"),
]

print(f"Copying from: {SOURCE_DOWNLOAD_FOLDER}")
print(f"Copying into: {DEST_REPO_FOLDER}\n")

for rel_path in files_to_copy:
    src = SOURCE_DOWNLOAD_FOLDER / rel_path
    dst = DEST_REPO_FOLDER / rel_path

    if not src.exists():
        print(f"  MISSING SOURCE: {src}")
        continue

    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"  Copied: {rel_path}")

print("\nDone. Now run:")
print("  git status")
print("  git add .")
print('  git commit -m "Editorial hero redesign"')
print("  git push")
