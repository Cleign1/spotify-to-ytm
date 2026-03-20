import pandas as pd
import os

def process_csv(filepath):
    # read CSV
    raw_csv = pd.read_csv(filepath)
    print("Original:")
    print(raw_csv.tail())

    # select columns
    new_csv = raw_csv[['Track Name', 'Artist Name(s)']].copy()
    new_csv = new_csv.rename(columns={
        "Artist Name(s)": "Artist Name"
    })
    
    new_csv = new_csv.dropna()
    
    # clean whitespace
    new_csv["Track Name"] = new_csv["Track Name"].str.strip()
    new_csv["Artist Name"] = new_csv["Artist Name"].str.strip()

    # generate new filename safely
    filename = os.path.basename(filepath)  # nfs_rivals.csv
    name, _ = os.path.splitext(filename)   # nfs_rivals
    
    output_dir = "processed"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{name}_processed.csv")

    new_csv.to_csv(output_path, index=False)

    print(f"✅ Saved: {output_path}")

    return output_path

