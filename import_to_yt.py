import pandas as pd
from ytmusicapi import YTMusic
import time
import os
import json

from csv_extractor import process_csv

# ===== CONFIG =====
AUTH_FILE = "browser.json"
BATCH_SIZE = 50
DELAY = 0.5
RETRY_LIMIT = 3
CHECKPOINT_FILE = "checkpoint.json"

# ===== USER INPUT =====
RAW_FILE = input("Enter raw CSV path: ")
PLAYLIST_NAME = input("Enter playlist name: ")

# ===== STEP 1: PROCESS CSV =====
processed_file = process_csv(RAW_FILE)

# ===== INIT =====
yt = YTMusic(AUTH_FILE)

# ===== LOAD CSV =====
df = pd.read_csv(processed_file)

# validate columns
required_cols = {"Track Name", "Artist Name"}
if not required_cols.issubset(df.columns):
    raise ValueError(f"CSV missing required columns: {required_cols}")

songs = [(str(r["Track Name"]), str(r["Artist Name"])) for _, r in df.iterrows()]

print(f"Loaded {len(songs)} songs")

# ===== RESUME SUPPORT =====
start_index = 0
if os.path.exists(CHECKPOINT_FILE):
    with open(CHECKPOINT_FILE) as f:
        data = json.load(f)
        start_index = data.get("last_index", 0)
        print(f"🔁 Resuming from index {start_index}")

# ===== CREATE PLAYLIST =====
playlist_id = yt.create_playlist(PLAYLIST_NAME, "Imported from CSV")
print(f"Created playlist: {PLAYLIST_NAME}")

# ===== STATE =====
video_ids = []
failed = []
seen = set()

# ===== HELPERS =====
def save_checkpoint(index):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump({"last_index": index}, f)

def search_with_retry(query):
    for attempt in range(RETRY_LIMIT):
        try:
            results = yt.search(query, filter="songs")
            if results:
                return results[0]["videoId"]
            return None
        except Exception as e:
            print(f"Retry {attempt+1}/{RETRY_LIMIT} failed:", e)
            time.sleep(1)
    return None

# ===== MAIN LOOP =====
for i in range(start_index, len(songs)):

    track, artist = songs[i]

    key = f"{track}-{artist}"
    if key in seen:
        continue
    seen.add(key)

    query = f"{artist} - {track}"
    print(f"[{i+1}/{len(songs)}] {query}")

    video_id = search_with_retry(query)

    if video_id:
        video_ids.append(video_id)
    else:
        failed.append(query)

    # batch upload
    if len(video_ids) >= BATCH_SIZE:
        try:
            yt.add_playlist_items(playlist_id, video_ids)
            video_ids = []
        except Exception as e:
            print("Batch add failed:", e)
        time.sleep(2)

    # save progress
    save_checkpoint(i)

    time.sleep(DELAY)

# ===== FINAL FLUSH =====
if video_ids:
    yt.add_playlist_items(playlist_id, video_ids)

# ===== SAVE FAILED =====
if failed:
    with open("failed.txt", "w") as f:
        f.write("\n".join(failed))

print("\n✅ DONE")
print(f"Playlist ID: {playlist_id}")
print(f"Failed songs: {len(failed)}")