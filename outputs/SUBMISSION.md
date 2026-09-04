# JPEG-to-folder bucketing submission

## Deliverables

- `folder_identifiers.txt`: 500 valid folder identifiers.
- `jpeg_filenames.txt`: 50,000 valid JPEG scan names.
- `bucketed_files.json`: structured JSON mapping every folder to its JPEGs.
- `summary.csv`: one row per folder (all rows have 100 JPEGs).

## Algorithm (pseudocode)

```text
known_folders = set(folder_identifiers)
buckets = map each folder identifier to an empty list

for jpeg_filename in jpeg_filenames:
    validate that filename ends with ".jpg"
    split filename at its final "_J_"
    folder_identifier = text before "_J_"
    scan_number = text after "_J_" and before ".jpg"
    validate scan_number is exactly four digits
    if folder_identifier is not in known_folders:
        raise an error for an unmatched scan
    append jpeg_filename to buckets[folder_identifier]

write buckets as JSON
```

The executable, reproducible Python implementation is `../generate_and_bucket.py`.
Run `python3 generate_and_bucket.py` from the parent directory to recreate every data file exactly.

## Verification performed

```
Generated 500 folders and 50000 JPEG filenames.
folders: 500
images: 50000
```
