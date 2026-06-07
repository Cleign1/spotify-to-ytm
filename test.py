from typing import cast

from ytmusicapi import YTMusic
import json
from datetime import datetime
import os
import pandas as pd

video_ids: list[str] = []

def fileNaming() -> str:
  date = datetime.now()
  formatted = date.strftime("%Y-%m-%d-%H-%M-%S")
  return formatted

def saveToFile(data: object, directory: str, prefix: str):
  filename = f"{prefix}-{fileNaming()}.json"
  if not os.path.exists(directory):
    os.makedirs(directory)
  with open(f"{directory}/{filename}", "w") as f:
    json.dump(data, f, indent=2)
    
def loadFromFile(filepath: str):
  df = pd.read_csv(filepath)
  songs: list[str] = [
    (str(r["Track Name"]))
    for _, r in df.iterrows()]
  return songs

def searchSongs(query: str):
  yt = YTMusic('browser.json')
  
  search = yt.search(
    query=query,
    filter="songs");
  
  # saveToFile(search)  
  if search:
    video_ids.append(search[0]["videoId"])
    print(f"Found video ID: {search[0]['videoId']} for query: {query}")
  
  print(video_ids)
  # return video_ids

REQUIRED_COLUMNS = ["Track Name", "Artist Name(s)"]

def process_csv(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)

    df = pd.read_csv(filepath)

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    df = df[REQUIRED_COLUMNS].copy()

    df = df.rename(columns={
        "Artist Name(s)": "Artist Name"
    })

    df["Track Name"] = df["Track Name"].astype(str).str.strip()
    df["Artist Name"] = df["Artist Name"].astype(str).str.strip()

    df = df.dropna().drop_duplicates()

    name = os.path.splitext(os.path.basename(filepath))[0]
    os.makedirs("processed", exist_ok=True)

    output = f"processed/{name}_processed.csv"
    df.to_csv(output, index=False)

    return output

def checkSources(video_id: str):
  yt = YTMusic('browser.json')
  song = yt.get_song(video_id)
  songUrl = song["microformat"]["microformatDataRenderer"]["urlCanonical"]
  return songUrl


# songs = loadFromFile('processed/popular_stuff_processed.csv')

# for track in songs:
#   query = cast(str, track)
#   searchSongs(query)
#   # print(query)

# saveToFile(video_ids, "searched_song", "searched")

# with open("searched_song/searched-2026-06-07-18-22-21.json") as f:
#   video_ids = json.load(f)
  
# print(video_ids[0])
# print(checkSources(video_ids[0]))

