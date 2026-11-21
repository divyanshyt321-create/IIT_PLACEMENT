from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "Dataset" / "placement_data.csv"
OUTPUT = ROOT / "Dataset" / "cleaned_placement_data.csv"

REQUIRED_COLUMNS = {
    "Branch",
    "Students",
    "Placed",
    "Average_Package",
    "Highest_Package"
}

def clean_data(input_path=INPUT, output_path=OUTPUT):
    df = pd.read_csv(input_path)

    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    df = df.drop_duplicates().copy()

    if df[list(REQUIRED_COLUMNS)].isnull().any().any():
        raise ValueError("Missing values found in required columns.")

    if (df["Students"] < 0).any() or (df["Placed"] < 0).any():
        raise ValueError("Student counts cannot be negative.")

    if (df["Placed"] > df["Students"]).any():
        raise ValueError("Placed students cannot exceed total students.")

    if (df["Students"] == 0).any():
        raise ValueError("Students must be greater than zero to calculate placement rate.")

    if (df[["Average_Package", "Highest_Package"]] < 0).any().any():
        raise ValueError("Package values cannot be negative.")

    df["Unplaced"] = df["Students"] - df["Placed"]
    df["Placement_Percentage"] = (
        df["Placed"] / df["Students"] * 100
    ).round(2)

    df.to_csv(output_path, index=False)

    print(f"Cleaned dataset saved to: {output_path}")
    return df

if __name__ == "__main__":
    clean_data()
