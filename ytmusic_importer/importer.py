import pandas as pd
import time
import json
import os
from ytmusicapi import YTMusic

CHECKPOINT_FILE = "checkpoint.json"

def run_import(processed_file, playlist_name, auth_file,
               batch_size=50, delay=0.5, resume=False):

    yt = YTMusic(auth_file)

    df = pd.read_csv(processed_file)

    songs = [(r["Track Name"], r["Artist Name"]) for _, r in df.iterrows()]

    start = 0
    if resume and os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE) as f:
            start = json.load(f).get("index", 0)
            print(f"Resuming from {start}")

    playlist_id = yt.create_playlist(playlist_name, "Imported via CLI")

    video_ids = []
    failed = []

    for i in range(start, len(songs)):
        track, artist = songs[i]
        query = f"{artist} - {track}"

        print(f"[{i+1}/{len(songs)}] {query}")

        try:
            results = yt.search(query, filter="songs")
            if results:
                video_ids.append(results[0]["videoId"])
            else:
                failed.append(query)
        except Exception:
            failed.append(query)

        if len(video_ids) >= batch_size:
            yt.add_playlist_items(playlist_id, video_ids)
            video_ids = []
            time.sleep(2)

        if resume:
            with open(CHECKPOINT_FILE, "w") as f:
                json.dump({"index": i}, f)

        time.sleep(delay)

    if video_ids:
        yt.add_playlist_items(playlist_id, video_ids)

    if failed:
        with open("failed.txt", "w") as f:
            f.write("\n".join(failed))

    print("Done.")