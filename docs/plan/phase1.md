# Phase 1: Parse Exportify CSV

## Objective

Build a parser that converts an Exportify CSV export into clean Python objects that can later be used for:

- YouTube Music searching
- Song matching
- Playlist creation
- FastAPI endpoints

Do **not** worry about YouTube Music yet.

Focus only on transforming raw CSV data into a clean internal representation.

---

# Expected Input

Exportify CSV:

```csv
Track URI,Track Name,Artist URI(s),Artist Name(s),...
spotify:track:...,Runaway Baby,spotify:artist:...,Bruno Mars,...
spotify:track:...,Slow It Down,spotify:artist:...,Benson Boone,...
```

---

# Expected Output

Python objects:

```python
[
    {
        "title": "Runaway Baby",
        "artists": ["Bruno Mars"]
    },
    {
        "title": "Slow It Down",
        "artists": ["Benson Boone"]
    }
]
```

Multiple artists:

Input:

```csv
Track Name,Artist Name(s)
Industry Baby,"Lil Nas X, Jack Harlow"
```

Output:

```python
{
    "title": "Industry Baby",
    "artists": [
        "Lil Nas X",
        "Jack Harlow"
    ]
}
```

---

# Task 1 — Understand the Input Data

## Goal

Learn exactly what data Exportify gives you.

Example columns:

```text
Track URI
Track Name
Artist URI(s)
Artist Name(s)
Album URI
Album Name
Album Artist Name(s)
Track Duration (ms)
...
```

## Deliverable

Identify the minimum columns needed for v1.

Required:

```text
Track Name
Artist Name(s)
```

Everything else can be ignored for now.

---

# Task 2 — Create a Track Model

## Goal

Represent a song using a Python object instead of dictionaries.

Create:

```python
from dataclasses import dataclass

@dataclass
class Track:
    title: str
    artists: list[str]
```

## Why

Instead of:

```python
song["Track Name"]
```

you can do:

```python
track.title
```

which is cleaner and easier to maintain.

## Deliverable

A working `Track` dataclass.

---

# Task 3 — Read the CSV File

## Goal

Learn how to load CSV data into Python.

Research:

```python
csv.DictReader
```

Expected row format:

```python
{
    "Track Name": "Runaway Baby",
    "Artist Name(s)": "Bruno Mars"
}
```

## Deliverable

Print every row from the CSV.

Do not transform anything yet.

---

# Task 4 — Extract Required Fields

## Goal

Ignore unnecessary Spotify metadata.

Convert:

```python
{
    "Track URI": "...",
    "Track Name": "Runaway Baby",
    "Artist Name(s)": "Bruno Mars",
    ...
}
```

into:

```python
{
    "title": "Runaway Baby",
    "artists": "Bruno Mars"
}
```

## Deliverable

Successfully extract:

- Track Name
- Artist Name(s)

from every row.

---

# Task 5 — Parse Artist Names

## Goal

Convert artist strings into lists.

### Single Artist

Input:

```python
"Bruno Mars"
```

Output:

```python
["Bruno Mars"]
```

### Multiple Artists

Input:

```python
"Lil Nas X, Jack Harlow"
```

Output:

```python
[
    "Lil Nas X",
    "Jack Harlow"
]
```

## Hint

Useful methods:

```python
.split(",")
```

```python
.strip()
```

## Deliverable

A helper function:

```python
parse_artists(...)
```

that always returns:

```python
list[str]
```

---

# Task 6 — Create Track Objects

## Goal

Convert CSV rows into Track objects.

Example:

```python
Track(
    title="Runaway Baby",
    artists=["Bruno Mars"]
)
```

Store them inside:

```python
tracks = []
```

## Deliverable

A list of Track objects generated from the CSV.

---

# Task 7 — Create a Playlist Model

## Goal

Represent an entire playlist.

Create:

```python
from dataclasses import dataclass

@dataclass
class Playlist:
    name: str
    tracks: list[Track]
```

Example:

```python
Playlist(
    name="popular_stuff",
    tracks=[...]
)
```

## Deliverable

A working Playlist dataclass.

---

# Task 8 — Generate Playlist Name

## Goal

Automatically derive the playlist name from the CSV filename.

Input:

```text
popular_stuff.csv
```

Output:

```python
"popular_stuff"
```

Optional future enhancement:

```python
"Popular Stuff"
```

## Deliverable

A helper function:

```python
get_playlist_name(...)
```

---

# Task 9 — Create the Exportify Parser

## Goal

Build the first real component of the application.

Suggested structure:

```text
ytmusic_importer/

├── models/
│   ├── track.py
│   └── playlist.py
│
└── parsers/
    └── exportify.py
```

Example usage:

```python
parser = ExportifyParser()

playlist = parser.parse(
    "popular_stuff.csv"
)
```

Expected return value:

```python
Playlist(...)
```

## Deliverable

A reusable parser class.

---

# Task 10 — Add Validation

## Goal

Detect invalid CSV files early.

Required columns:

```text
Track Name
Artist Name(s)
```

If missing:

```python
raise ValueError(...)
```

Example invalid CSV:

```csv
Song,Artist
```

## Deliverable

Meaningful validation errors.

---

# Definition of Done

The parser should support:

```python
parser = ExportifyParser()

playlist = parser.parse(
    "popular_stuff.csv"
)

print(playlist.name)

for track in playlist.tracks:
    print(track.title)
    print(track.artists)
```

Expected output:

```python
popular_stuff

Runaway Baby
["Bruno Mars"]

Slow It Down
["Benson Boone"]

Marry You
["Bruno Mars"]

...
```

---

# Final Output Structure

At the end of Phase 1, your application should produce:

```python
Playlist(
    name="popular_stuff",
    tracks=[
        Track(
            title="Runaway Baby",
            artists=["Bruno Mars"]
        ),
        Track(
            title="Slow It Down",
            artists=["Benson Boone"]
        )
    ]
)
```

This becomes the foundation for every future feature.

---

# Future Phases

## Phase 1

✅ Parse CSV

## Phase 2

Search YouTube Music

## Phase 3

Match Songs

## Phase 4

Create Playlist

## Phase 5

Add Songs

## Phase 6

Generate Reports

## Phase 7

Caching and Resume Support

## Phase 8

FastAPI Backend

## Phase 9

Web UI

---

# Success Criteria

Before moving to Phase 2, ensure:

- CSV files load successfully
- Playlist names are extracted correctly
- Artist names become lists
- Track objects are created correctly
- Invalid CSV files fail gracefully
- Parser works on multiple Exportify exports

Once this is complete, every future feature will operate on:

```python
Playlist
└── Track
    ├── title
    └── artists[]
```

rather than raw CSV data.