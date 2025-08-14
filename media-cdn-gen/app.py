import os
import uuid
import json
from datetime import datetime


def is_uuid_filename(filename):
    """Check if filename (without extension) looks like a UUID"""
    name, _ = os.path.splitext(filename)
    return len(name) == 32 and all(c in "0123456789abcdef" for c in name.lower())


def rename_files_randomly(img_path: str, json_path: str):
    if not os.path.isdir(img_path):
        print("❌ Folder does not exist.")
        return

    # Get list of normal files that are not already UUID-named
    files = [
        f
        for f in os.listdir(img_path)
        if os.path.isfile(os.path.join(img_path, f))
        and not f.startswith(".")
        and not is_uuid_filename(f)
    ]

    files.sort()  # Keep consistent order

    new_filenames = []

    for filename in files:
        old_path = os.path.join(img_path, filename)
        _, ext = os.path.splitext(filename)

        new_name = f"{uuid.uuid4().hex}{ext}"
        new_path = os.path.join(img_path, new_name)

        os.rename(old_path, new_path)
        new_filenames.append(new_name)

        print(f"Renamed: {filename} ➝ {new_name}")

    if new_filenames:
        # Create a timestamped JSON filename to prevent overwrite
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f"renamed_files.json"
        # json_filename = f"renamed_files_{timestamp}.json"
        json_new_path = os.path.join(json_path, json_filename)

        with open(json_new_path, "w", encoding="utf-8") as f:
            json.dump(new_filenames, f, indent=4)

        print(f"\n✅ Renamed {len(new_filenames)} files.")
        print(f"📝 New filenames saved to: {json_filename}")
    else:
        print("\n⚠️ No files to rename (maybe already renamed).")


# 🔧 Set your target folder path here
imgPath = "media-cdn-gen/img"
jsonPath = "media-cdn-gen"
rename_files_randomly(imgPath, jsonPath)
