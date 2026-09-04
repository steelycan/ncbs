#!/usr/bin/env python3
"""Create deterministic test data and bucket scanned JPEGs by folder identifier."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

OUTPUT = Path("outputs")
FOLDER_COUNT = 500
JPEG_COUNT = 50_000


def make_folder_identifiers() -> list[str]:
    """Return 500 identifiers in the requested MS-011_a_b_c_d shape."""
    folders: list[str] = []
    for volume in range(1, 7):
        for section in range(1, 3):
            for series in range(1, 7):
                for item in range(1, 342):
                    folders.append(f"MS-011_{volume}_{section}_{series}_{item}")
                    if len(folders) == FOLDER_COUNT:
                        return folders
    raise RuntimeError("Not enough identifiers generated")


def make_jpeg_filenames(folders: list[str]) -> list[str]:
    """Distribute exactly 50,000 images cyclically across the folders."""
    return [
        f"{folders[index % len(folders)]}_J_{(index // len(folders)) + 1:04d}.jpg"
        for index in range(JPEG_COUNT)
    ]


def folder_from_filename(filename: str) -> str:
    """Extract identifier, validating the expected scan-name suffix."""
    marker = "_J_"
    if not filename.endswith(".jpg") or marker not in filename:
        raise ValueError(f"Invalid JPEG filename: {filename}")
    folder, image_number = filename.rsplit(marker, 1)
    if not image_number[:-4].isdigit() or len(image_number[:-4]) != 4:
        raise ValueError(f"Invalid JPEG sequence: {filename}")
    return folder


def bucket_files(folders: list[str], jpeg_filenames: list[str]) -> dict[str, list[str]]:
    """Bucket every JPEG under its matching, known folder identifier."""
    known_folders = set(folders)
    buckets: dict[str, list[str]] = defaultdict(list)
    for filename in jpeg_filenames:
        folder = folder_from_filename(filename)
        if folder not in known_folders:
            raise ValueError(f"No folder supplied for {filename}")
        buckets[folder].append(filename)
    return {folder: buckets[folder] for folder in folders}


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    folders = make_folder_identifiers()
    images = make_jpeg_filenames(folders)
    buckets = bucket_files(folders, images)

    (OUTPUT / "folder_identifiers.txt").write_text("\n".join(folders) + "\n")
    (OUTPUT / "jpeg_filenames.txt").write_text("\n".join(images) + "\n")
    (OUTPUT / "bucketed_files.json").write_text(json.dumps(buckets, indent=2) + "\n")

    with (OUTPUT / "summary.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["folder_identifier", "jpeg_count", "first_jpeg", "last_jpeg"])
        for folder, files in buckets.items():
            writer.writerow([folder, len(files), files[0], files[-1]])

    assert len(folders) >= 500
    assert len(images) >= 50_000
    assert sum(map(len, buckets.values())) == len(images)
    print(f"Generated {len(folders)} folders and {len(images)} JPEG filenames.")


if __name__ == "__main__":
    main()
