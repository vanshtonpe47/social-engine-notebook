from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# 1. Define project paths
# ------------------------------------------------------------

PHASE2_DIR = Path(__file__).resolve().parent
RESULTS_DIR = PHASE2_DIR / "results"
SCREENSHOTS_DIR = PHASE2_DIR / "screenshots"

SCREENSHOTS_DIR.mkdir(exist_ok=True)


# ------------------------------------------------------------
# 2. Screenshot creation function
# ------------------------------------------------------------

def create_table_screenshot(
    csv_filename,
    output_filename,
    title,
    max_rows=25
):
    """
    Read a generated CSV result and save it as a JPEG table image.
    """

    input_file = RESULTS_DIR / csv_filename
    output_file = SCREENSHOTS_DIR / output_filename

    if not input_file.exists():
        raise FileNotFoundError(
            f"Missing result file: {input_file}"
        )

    data = pd.read_csv(input_file)

    # Display only a limited number of rows in the screenshot.
    # The complete result remains available in the CSV file.
    displayed_data = data.head(max_rows).copy()

    # Round decimal values for readability.
    for column in displayed_data.columns:
        if pd.api.types.is_float_dtype(displayed_data[column]):
            displayed_data[column] = displayed_data[column].round(2)

    figure_height = max(
        3.5,
        0.55 * (len(displayed_data) + 3)
    )

    figure, axis = plt.subplots(
        figsize=(16, figure_height)
    )

    axis.axis("off")

    axis.set_title(
        title,
        fontsize=16,
        fontweight="bold",
        loc="left",
        pad=18
    )

    table = axis.table(
        cellText=displayed_data.astype(str).values,
        colLabels=displayed_data.columns,
        cellLoc="left",
        colLoc="left",
        loc="center"
    )

    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.6)

    # Style the table header and alternate rows.
    for (row, column), cell in table.get_celld().items():

        if row == 0:
            cell.set_facecolor("#1F4E79")
            cell.set_text_props(
                color="white",
                weight="bold"
            )

        elif row % 2 == 0:
            cell.set_facecolor("#EAF2F8")

    figure.tight_layout()

    figure.savefig(
        output_file,
        format="jpeg",
        dpi=180,
        bbox_inches="tight"
    )

    plt.close(figure)

    print(f"Created: {output_file}")


# ------------------------------------------------------------
# 3. Create E3 screenshot
# ------------------------------------------------------------

create_table_screenshot(
    csv_filename="E3_result.csv",
    output_filename="E3_platform_engagement.jpeg",
    title="E3 - Average Engagement by Platform",
    max_rows=10
)


# ------------------------------------------------------------
# 4. Create M2 screenshot
# ------------------------------------------------------------

create_table_screenshot(
    csv_filename="M2_result.csv",
    output_filename="M2_follower_groups.jpeg",
    title="M2 - Average Engagement by Follower Group",
    max_rows=10
)


# ------------------------------------------------------------
# 5. Create H3 screenshot
# ------------------------------------------------------------

create_table_screenshot(
    csv_filename="H3_result.csv",
    output_filename="H3_platform_anomalies.jpeg",
    title="H3 - Exceptional Posts: Top 25 Results",
    max_rows=25
)


print()
print("ALL JPEG SCREENSHOTS CREATED")
