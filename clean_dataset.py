# clean_dataset.py
# -------------------------------------------------------
# Removes corrupted images + duplicate images from dataset
# -------------------------------------------------------

from PIL import Image
import os, hashlib

EMOTIONS = ["happy", "sad", "angry", "surprised", "neutral"]
BASE_PATH = "dataset"   # adjust if needed


# ----------------------------------------
# Check if an image is corrupted
# ----------------------------------------
def is_corrupted(path):
    try:
        Image.open(path).verify()
        return False
    except:
        return True


# ----------------------------------------
# Remove corrupted images
# ----------------------------------------
def remove_bad_images(folder):
    removed = 0
    for file in os.listdir(folder):
        fpath = os.path.join(folder, file)
        if not os.path.isfile(fpath):
            continue
        
        if is_corrupted(fpath):
            os.remove(fpath)
            removed += 1
    return removed


# ----------------------------------------
# Remove duplicate images (by file hash)
# ----------------------------------------
def remove_duplicates(folder):
    hashes = set()
    removed = 0
    for file in os.listdir(folder):
        fpath = os.path.join(folder, file)
        if not os.path.isfile(fpath):
            continue

        try:
            data = open(fpath, "rb").read()
            h = hashlib.sha1(data).hexdigest()
            if h in hashes:
                os.remove(fpath)
                removed += 1
                continue
            hashes.add(h)
        except:
            continue
    return removed


# ----------------------------------------
# Run cleaning for all emotion folders
# ----------------------------------------
def clean_all():
    print(" Starting dataset cleaning...\n")

    for emotion in EMOTIONS:
        folder = os.path.join(BASE_PATH, emotion)
        if not os.path.isdir(folder):
            print(f"⚠ Folder not found: {folder}")
            continue

        print(f"Cleaning: {emotion}")

        bad = remove_bad_images(folder)
        dups = remove_duplicates(folder)

        print(f"   - Removed corrupted: {bad}")
        print(f"   - Removed duplicates: {dups}\n")

    print("Cleaning complete!")


if __name__ == "__main__":
    clean_all()
