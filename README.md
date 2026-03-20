# 🎧 ytmusic-importer

[![PyPI version](https://img.shields.io/pypi/v/ytmusic-importer.svg)](https://pypi.org/project/ytmusic-importer/)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> Import Spotify playlist CSV exports into YouTube Music — from your terminal.

---

## ✨ Overview

**ytmusic-importer** is a lightweight CLI tool that automates:

```
Spotify CSV → YouTube Music Playlist
```

It handles:

* CSV cleaning
* Track matching
* Playlist creation
* Batch uploads

---

## 🚀 Features

* ⚡ Fast batch importing
* 🔁 Resume support (checkpoint-based)
* 🧹 Automatic CSV cleaning
* 📉 Failure tracking (`failed.txt`)
* 🐧 Designed for Linux CLI workflows

---

## 📦 Installation

### Install from PyPI

```bash
pip install ytmusic-importer
```

---

### Install locally (dev)

```bash
git clone https://github.com/YOUR_USERNAME/ytmusic-importer.git
cd ytmusic-importer
pip install -e .
```

---

## 🔐 Authentication Setup

This tool uses `ytmusicapi` and requires your YouTube Music session.

Run:

```bash
ytmusicapi setup
```

This creates:

```
browser.json
```

Place it in your working directory.

---

## 📁 Input Format

Export your playlist from Spotify as CSV.

Required columns:

```
Track Name
Artist Name(s)
```

---

## ▶️ Usage

### Basic

```bash
ytmusic-import raw/playlist.csv "My Playlist"
```

---

### Advanced

```bash
ytmusic-import raw/playlist.csv "My Playlist" \
  --auth browser.json \
  --batch-size 50 \
  --delay 0.5 \
  --resume
```

---

## ⚙️ CLI Arguments

| Argument   | Description      |
| ---------- | ---------------- |
| `input`    | Path to CSV file |
| `playlist` | Playlist name    |

---

## 🔧 Options

| Option         | Default      | Description            |
| -------------- | ------------ | ---------------------- |
| `--auth`       | browser.json | Auth file path         |
| `--batch-size` | 50           | Songs per batch        |
| `--delay`      | 0.5          | Delay between requests |
| `--resume`     | false        | Resume import          |

---

## 🔄 How It Works

1. Parse Spotify CSV
2. Clean track + artist data
3. Search YouTube Music
4. Extract `videoId`
5. Add to playlist

---

## 📂 Output

| File                  | Description    |
| --------------------- | -------------- |
| `processed_csv/*.csv` | Cleaned CSV    |
| `checkpoint.json`     | Resume state   |
| `failed.txt`          | Failed matches |

---

## ⚠️ Notes

* Large playlists may take time (~0.5s per song)
* Matching is best-effort (not 100% perfect)
* Practical playlist limit ≈ 5000 songs
* Uses unofficial API (may break)

---

## 🛠 Troubleshooting

### ❌ Invalid auth

```bash
ytmusicapi setup
```

---

### ❌ Command not found

```bash
pip install -e .
```

---

### ❌ Missing columns

Ensure CSV contains:

```
Track Name, Artist Name(s)
```

---

## 🧪 Example

```bash
ytmusic-import raw/this_is_james_blake.csv "This is James Blake"
```

---

## 🧑‍💻 Contributing

PRs are welcome. For major changes, open an issue first.

---

## 📜 License

MIT License © 2026
