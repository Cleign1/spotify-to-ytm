# ytmusic_importer/__init__.py

"""
ytmusic_importer

CLI tool for importing Spotify CSV playlists into YouTube Music.
"""

__version__ = "0.1.0"

# Explicit public API
from .extractor import process_csv
from .importer import run_import

__all__ = [
    "process_csv",
    "run_import",
]