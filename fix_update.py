"""
SETUP (one time):
  1. Move this file into your git repo folder
     (the one where 'git status' works — likely "identite-cosmetics-site (4)").

RUN IT:
  From inside that repo folder, in PyCharm's terminal:
      python fix_update.py

WHAT IT DOES:
  - Searches your entire Downloads folder for any folder named
    "identite-cosmetics-site*" that contains app.py
  - Picks the most recently modified one (your latest download)
  - Copies static/css/style.css and templates/index.html from it
    into the folder this script is running from (your repo)
  - Skips itself and the repo folder so it doesn't copy onto itself
"""

import shutil
from pathlib import Path

REPO_FOLDER = Path.cwd()
DOWNLOADS = Path.home() / "Downloads"

print(f"Repo folder (destination): {REPO_FOLDER}")
print(f"Searching for source in:   {DOWNLOADS}\n")

candidates = []
for path in DOWNLOADS.glob("identite-cosmetics-site*"):
    if not path.is_dir():
        continue
    # the zip extracts a folder that may contain ANOTHER nested folder
    # with the same name -- search a couple levels deep for app.py
    for app_py in path.rglob("app.py"):
        candidate_root = app_py.parent
        if candidate_root.resolve() == REPO_FOLDER.resolve():
            continue  # skip the repo itself if it matches the glob
        candidates.append((candidate_root, app_py.stat().st_mtime))

if not candidates:
    print("No source folder found containing app.py under Downloads.")
    print("Double check the zip was actually unzipped (not just downloaded as .zip).")
else:
    # pick the most recently modified app.py -> that's the newest download
    candidates.sort(key=lambda x: x[1], reverse=True)
    source_root = candidates[0][0]
    print(f"Using newest source found: {source_root}\n")

    files_to_copy = [
        Path("static/css/style.css"),
        Path("templates/index.html"),
    ]

    for rel_path in files_to_copy:
        src = source_root / rel_path
        dst = REPO_FOLDER / rel_path

        if not src.exists():
            print(f"  MISSING SOURCE: {src}")
            continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  Copied: {rel_path}")

    print("\nDone. Now run:")
    print("  git status")
    print("  git add .")
    print('  git commit -m "Remove photo from homepage hero, use texture instead"')
    print("  git push")
