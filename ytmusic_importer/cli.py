import argparse
from .extractor import process_csv
from .importer import run_import

def main():
    parser = argparse.ArgumentParser(
        description="Import Spotify CSV to YouTube Music"
    )

    parser.add_argument("input", help="Path to raw CSV file")
    parser.add_argument("playlist", help="Playlist name")

    parser.add_argument("--auth", default="browser.json")
    parser.add_argument("--batch-size", type=int, default=50)
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--resume", action="store_true")

    args = parser.parse_args()

    processed = process_csv(args.input)

    run_import(
        processed_file=processed,
        playlist_name=args.playlist,
        auth_file=args.auth,
        batch_size=args.batch_size,
        delay=args.delay,
        resume=args.resume
    )