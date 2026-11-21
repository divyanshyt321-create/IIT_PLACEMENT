from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "Dataset" / "cleaned_placement_data.csv"
REPORT_DIR = ROOT / "Reports"

REPORT_DIR.mkdir(exist_ok=True)


def analyze_data(input_path=INPUT):
    df = pd.read_csv(input_path)

    total_students = int(df["Students"].sum())
    total_placed = int(df["Placed"].sum())
    total_unplaced = int(df["Unplaced"].sum())

    overall_rate = round(
        total_placed / total_students * 100, 2
    )

    weighted_average_package = round(
        (df["Average_Package"] * df["Placed"]).sum()
        / total_placed,
        2
    )

    highest_package_branch = df.loc[
        df["Highest_Package"].idxmax()
    ]

    highest_placement_branch = df.loc[
        df["Placement_Percentage"].idxmax()
    ]

    lowest_placement_branch = df.loc[
        df["Placement_Percentage"].idxmin()
    ]

    summary = {
        "total_students": total_students,
        "total_placed": total_placed,
        "total_unplaced": total_unplaced,
        "overall_placement_percentage": overall_rate,
        "weighted_average_package_estimate_lpa": weighted_average_package,
        "highest_package_lpa": float(df["Highest_Package"].max()),
        "branch_with_highest_package": str(
            highest_package_branch["Branch"]
        ),
        "branch_with_highest_placement_rate": str(
            highest_placement_branch["Branch"]
        ),
        "highest_placement_rate_percentage": float(
            highest_placement_branch["Placement_Percentage"]
        ),
        "branch_with_lowest_placement_rate": str(
            lowest_placement_branch["Branch"]
        ),
        "lowest_placement_rate_percentage": float(
            lowest_placement_branch["Placement_Percentage"]
        )
    }

    df.to_csv(
        REPORT_DIR / "branch_analysis.csv",
        index=False
    )

    with open(
        REPORT_DIR / "summary.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(summary, file, indent=4)

    print("PLACEMENT ANALYSIS")
    print("------------------")

    for key, value in summary.items():
        print(f"{key}: {value}")

    return df, summary


if __name__ == "__main__":
    analyze_data()
