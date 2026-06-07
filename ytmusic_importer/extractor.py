import pandas as pd
import os

REQUIRED_COLUMNS = ["Track Name", "Artist Name(s)"]

def process_csv(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)

    df = pd.read_csv(filepath)

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    df = df[REQUIRED_COLUMNS].copy()

    df = df.rename(columns={
        "Artist Name(s)": "Artist Name"
    })

    df["Track Name"] = df["Track Name"].astype(str).str.strip()
    df["Artist Name"] = df["Artist Name"].astype(str).str.strip()

    df = df.dropna().drop_duplicates()

    name = os.path.splitext(os.path.basename(filepath))[0]
    os.makedirs("processed", exist_ok=True)

    output = f"processed/{name}_processed.csv"
    df.to_csv(output, index=False)

    return output