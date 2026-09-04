# JPEG folder bucketing submission

Run from this directory:

```sh
python3 generate_and_bucket.py
```

The generator creates reproducible, deterministic test data:

- `outputs/folder_identifiers.txt` — 500 folder identifiers
- `outputs/jpeg_filenames.txt` — 50,000 scanned JPEG filenames
- `outputs/bucketed_files.json` — every JPEG grouped under its folder
- `outputs/summary.csv` — per-folder counts and boundary filenames

## Matching rule

For a filename such as `MS-011_1_1_1_1_J_0001.jpg`, the script splits at the final `_J_`; the text before it is the folder identifier. It validates the `.jpg` extension and four-digit scan sequence, then checks that the identifier exists in the supplied folder list. Invalid or unmatched filenames stop the run with a clear error.

The included data assigns 100 JPEGs to each of the 500 folders, for 50,000 files total.
