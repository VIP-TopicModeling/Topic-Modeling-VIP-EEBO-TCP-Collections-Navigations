import json
import os
import shutil

# --- USER INPUT ---
META_PATH = "PATH/TO/meta.json"  # e.g., "../data/meta.json"
SOURCE_TEXT_DIR = "PATH/TO/full_corpus"  # folder where the .txt files live
OUTPUT_BASE_DIR = "PATH/TO/split_corpus"  # e.g., "../data/split_corpus/"
# ------------------

# Define time periods
time_periods = {
    "1640_1720": (1640, 1720),
    "1721_1780": (1721, 1780),
    "1781_1900": (1781, 1900)
}

# Load metadata
with open(META_PATH, 'r', encoding='utf-8') as f:
    metadata = json.load(f)

# Create output folders
for period in time_periods:
    os.makedirs(os.path.join(OUTPUT_BASE_DIR, period), exist_ok=True)

# Assign files to correct period
count = {k: 0 for k in time_periods}

for doc in metadata:
    try:
        year = int(doc.get('year', 0))
        filename = doc['filename']
    except (KeyError, ValueError):
        continue  # Skip if year or filename is missing/bad

    # Determine time period
    for period, (start, end) in time_periods.items():
        if start <= year <= end:
            src_path = os.path.join(SOURCE_TEXT_DIR, filename)
            dest_path = os.path.join(OUTPUT_BASE_DIR, period, filename)

            if os.path.exists(src_path):
                shutil.copy(src_path, dest_path)
                count[period] += 1
            break  # Stop checking other periods

# --- Summary ---
print("Corpus was split into time periods.")
for period in time_periods:
    print(f"{period}: {count[period]} files")
