import pandas as pd
import time
import json
import os
from typing import Union, Dict, Any, List, Tuple
from ytmusicapi import YTMusic

CHECKPOINT_FILE = "checkpoint.json"


def _ensure_playlist_id(result: Union[str, Dict[str, Any]]) -> str:
    """
    Ensure playlist creation succeeded and return playlist ID.
    """
    if isinstance(result, str):
        return result

    raise RuntimeError(f"Failed to create playlist: {result}")


def run_import(
    processed_file: str,
    playlist_name: str,
    auth_file: str,
    batch_size: int = 50,
    delay: float = 0.5,
    resume: bool = False,
):

    yt = YTMusic(auth_file)

    df = pd.read_csv(processed_file)

    songs: List[Tuple[str, str]] = [
        (str(r["Track Name"]), str(r["Artist Name"]))
        for _, r in df.iterrows()
    ]

    start = 0
    if resume and os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE) as f:
            start = json.load(f).get("index", 0)
            print(f"Resuming from {start}")

    playlist_raw = yt.create_playlist(playlist_name, "Imported via CLI")
    playlist_id: str = _ensure_playlist_id(playlist_raw)

    video_ids: List[str] = []
    failed: List[str] = []

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

        except Exception as e:
            print(f"Search error: {e}")
            failed.append(query)

        # batch add
        if len(video_ids) >= batch_size:
            try:
                yt.add_playlist_items(playlist_id, video_ids)
            except Exception as e:
                print(f"Batch add error: {e}")

            video_ids = []
            time.sleep(2)

        # checkpoint
        if resume:
            with open(CHECKPOINT_FILE, "w") as f:
                json.dump({"index": i}, f)

        time.sleep(delay)

    if video_ids:
        try:
            yt.add_playlist_items(playlist_id, video_ids)
        except Exception as e:
            print(f"Final batch error: {e}")

    # save failures
    if failed:
        with open("failed.txt", "w") as f:
            f.write("\n".join(failed))

    print("Done.")