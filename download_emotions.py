from ddgs import DDGS
import requests, os, time, hashlib
from tqdm import tqdm

# ----------------------------------------
# Helper: create a unique filename per image
# ----------------------------------------
def hash_bytes(data):
    return hashlib.sha1(data).hexdigest()

# ----------------------------------------
# Multi-keyword image downloader
# ----------------------------------------
def download_images(keywords, folder, min_images=140):
    os.makedirs(folder, exist_ok=True)
    print(f"\nDownloading images for: {folder}")
    print(f"Using {len(keywords)} search queries...")
    
    downloaded = set()  # to avoid duplicates
    count = len(os.listdir(folder))

    with DDGS() as ddgs:
        for query in keywords:
            print(f"\n🔍 Query: {query}")
            try:
                results = ddgs.images(query, safesearch="off")
            except Exception as e:
                print(f"Error starting query: {e}")
                continue

            for r in tqdm(results):
                if count >= min_images:
                    print(f"Reached {min_images} images for {folder}")
                    return

                url = r.get("image")
                if not url:
                    continue

                try:
                    img_data = requests.get(url, timeout=10).content
                except:
                    continue

                # Skip duplicates
                img_hash = hash_bytes(img_data)
                if img_hash in downloaded:
                    continue

                downloaded.add(img_hash)

                # Save image
                file_path = os.path.join(folder, f"{count}.jpg")
                try:
                    with open(file_path, "wb") as f:
                        f.write(img_data)
                    count += 1
                except:
                    continue

                time.sleep(0.1)  # reduce rate-limit risk

    print(f"⚠ Only got {count} images for {folder}. Try adding more keywords.")


# ----------------------------------------
# Emotion → multiple keywords per class
# ----------------------------------------

emotions = {
    "happy": [
        # NEW diverse queries
        "happy cartoon portrait",
        "happy cartoon avatar",
        "happy cartoon icon",
        "3d happy cartoon face",
        "happy character doodle",
        "happy cartoon child drawing",
        "happy chibi face",
        "happy manga close up",
        "happy comic style face",
        "happy cartoon flat design",

        # EXISTING queries
        "smiling child cartoon",
        "grinning cartoon character",
        "laughing cartoon character",
        "cheerful cartoon portrait",
        "happy cartoon character",
        "happy cartoon face",
        "smiling cartoon face",
        "happy emoji face",
        "kawaii happy face",
        "happy animated face",
        "happy cartoon expression",
        "smiley cartoon face",
        "joyful cartoon character",
        "happy face drawing cartoon",
        "cute happy cartoon face",
        "happy cartoon vector",
        "anime happy face closeup",
        "happy cartoon clipart face",
        "smiling character illustration",
        "happy manga face expression",
        "beaming cartoon face",
        "smiling mascot character",
        "smiley cartoon sticker",
        "happy child animation",
    ],

    "sad": [
        # NEW diverse queries
        "sad cartoon portrait",
        "sad cartoon avatar",
        "sad cartoon icon",
        "3d sad cartoon face",
        "sad character doodle",
        "crying cartoon child drawing",
        "sad chibi face",
        "sad manga close up",
        "sad comic style face",
        "sad cartoon flat design",

        # EXISTING queries
        "sad cartoon character",
        "sad cartoon face",
        "crying cartoon face",
        "sad emoji face",
        "kawaii sad face",
        "upset cartoon face",
        "tearful cartoon character",
        "sad animated face",
        "depressed cartoon face",
        "blue sad cartoon drawing",
        "sad expression cartoon",
        "sad cartoon vector",
        "crying anime face closeup",
        "tearful cartoon illustration",
        "sad character clipart",
        "sad manga expression face",
        "mourning cartoon character",
        "gloomy cartoon face",
        "sad sticker cartoon",
        "tear drop cartoon face",
    ],

    "angry": [
        # NEW diverse queries
        "angry cartoon portrait",
        "angry cartoon avatar",
        "angry cartoon icon",
        "3d angry cartoon face",
        "angry character doodle",
        "angry child drawing cartoon",
        "angry chibi face",
        "angry manga close up",
        "angry comic style face",
        "angry cartoon flat design",

        # EXISTING queries
        "angry cartoon character",
        "angry cartoon face",
        "mad cartoon face",
        "angry emoji face",
        "furious cartoon face",
        "kawaii angry face",
        "rage cartoon face",
        "angry animated face",
        "irritated cartoon character",
        "angry expression cartoon drawing",
        "mad expression cartoon face",
        "angry cartoon vector",
        "furious anime face closeup",
        "angry cartoon clipart",
        "mad manga expression",
        "rage cartoon illustration face",
        "steaming mad cartoon face",
        "scowling cartoon character",
        "angry mascot illustration",
        "gritting teeth cartoon face",
    ],

    "surprised": [
        # NEW diverse queries
        "surprised cartoon portrait",
        "surprised cartoon avatar",
        "surprised cartoon icon",
        "3d surprised cartoon face",
        "surprised character doodle",
        "surprised child drawing cartoon",
        "surprised chibi face",
        "surprised manga close up",
        "surprised comic style face",
        "surprised cartoon flat design",

        # EXISTING queries
        "surprised cartoon character",
        "surprised cartoon face",
        "shocked cartoon face",
        "wow cartoon face",
        "surprised emoji face",
        "kawaii surprised face",
        "astonished cartoon character",
        "surprise expression cartoon",
        "open mouth cartoon face",
        "shocked animated face",
        "surprised face illustration cartoon",
        "surprised cartoon vector",
        "shocked anime face closeup",
        "surprised cartoon clipart",
        "astonished manga expression",
        "wow face cartoon illustration",
        "gasping cartoon face",
        "jaw drop cartoon character",
        "wide eyed cartoon face",
        "surprised sticker cartoon",
    ],

    "neutral": [
        # NEW diverse queries
        "neutral cartoon portrait",
        "neutral cartoon avatar",
        "neutral cartoon icon",
        "3d neutral cartoon face",
        "neutral character doodle",
        "neutral child drawing cartoon",
        "neutral chibi face",
        "neutral manga close up",
        "neutral comic style face",
        "neutral cartoon flat design",

        # EXISTING queries
        "neutral cartoon character",
        "neutral cartoon face",
        "expressionless cartoon face",
        "blank cartoon face",
        "neutral emoji face",
        "kawaii neutral face",
        "straight face cartoon",
        "calm cartoon expression",
        "plain expression cartoon face",
        "emotionless cartoon character",
        "neutral animated face",
        "neutral cartoon vector",
        "expressionless anime face closeup",
        "neutral character clipart",
        "blank manga expression",
        "calm face cartoon illustration",
        "indifferent cartoon face",
        "poker face cartoon character",
        "neutral sticker illustration",
        "flat expression cartoon face",
    ],

}

# ----------------------------------------
# Run all downloads
# ----------------------------------------
for emotion, keywords in emotions.items():
    download_images(keywords, f"dataset/{emotion}", min_images=150)
