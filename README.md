# ytmusic-importer

[![PyPI version](https://img.shields.io/pypi/v/ytmusic-importer.svg)](https://pypi.org/project/ytmusic-importer/)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Import Spotify playlist CSV exports into YouTube Music from the command line.

---

## Overview

`ytmusic-importer` is a simple CLI tool that converts a Spotify playlist export into a YouTube Music playlist. It handles CSV cleaning, track matching, and playlist creation automatically.

---

## Features

* Batch importing for better performance
* Resume support for large playlists
* Automatic CSV normalization
* Failure tracking (`failed.txt`)
* Designed for Linux CLI workflows

---

## Installation

Install from PyPI:

```bash
pip install ytmusic-importer
```

Or install locally:

```bash
git clone https://github.com/YOUR_USERNAME/ytmusic-importer.git
cd ytmusic-importer
pip install -e .
```

---

## Authentication

This tool relies on `ytmusicapi`, which requires authentication via browser headers.

Run:

```bash
ytmusicapi setup
```

This will generate:

```
browser.json
```

Place it in your working directory or pass it via `--auth`.

---

## Input Format

Export your playlist from Spotify as CSV.

Required columns:

```
Track Name
Artist Name(s)
```

The tool will automatically convert this into the required format.

---

## Usage

Basic usage:

```bash
ytmusic-import raw/playlist.csv "My Playlist"
```

Advanced usage:

```bash
ytmusic-import raw/playlist.csv "My Playlist" \
  --auth browser.json \
  --batch-size 50 \
  --delay 0.5 \
  --resume
```

---

## Arguments

| Argument   | Description      |
| ---------- | ---------------- |
| `input`    | Path to CSV file |
| `playlist` | Playlist name    |

---

## Options

| Option         | Default      | Description            |
| -------------- | ------------ | ---------------------- |
| `--auth`       | browser.json | Auth file path         |
| `--batch-size` | 50           | Songs per batch        |
| `--delay`      | 0.5          | Delay between requests |
| `--resume`     | false        | Resume from checkpoint |

---

## How it works

1. Parse Spotify CSV
2. Extract track and artist
3. Search YouTube Music
4. Retrieve `videoId`
5. Add tracks to playlist

---

## Output

| File                  | Description    |
| --------------------- | -------------- |
| `processed_csv/*.csv` | Cleaned CSV    |
| `checkpoint.json`     | Resume state   |
| `failed.txt`          | Failed matches |

---

## Notes

* Large playlists can take time (~0.5s per song)
* Matching is best-effort and not guaranteed to be perfect
* Playlist size is practically limited (~5000 songs)
* Uses an unofficial API

---

## Troubleshooting

**Invalid auth JSON**

```bash
ytmusicapi setup
```

**Command not found**

```bash
pip install -e .
```

**Missing columns**

Ensure your CSV includes:

```
Track Name, Artist Name(s)
```

---

## Example

```bash
ytmusic-import raw/this_is_james_blake.csv "This is James Blake"
```

---

## License

MIT
