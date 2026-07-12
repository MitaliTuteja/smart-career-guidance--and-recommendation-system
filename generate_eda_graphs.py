from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# ---------------------------------------------------------
# 1. File and folder configuration
# ---------------------------------------------------------

DATASET_FILE = "Dataset.csv"
OUTPUT_FOLDER = Path("eda_graphs")

OUTPUT_FOLDER.mkdir(exist_ok=True)


# ---------------------------------------------------------
# 2. Load the dataset
# ---------------------------------------------------------

try:
    df = pd.read_csv(DATASET_FILE)
except FileNotFoundError as exc:
    raise FileNotFoundError(
        f"Could not find '{DATASET_FILE}'. "
        "Keep this Python file in the same folder as the CSV file."
    ) from exc


# Remove unnecessary spaces from column names
df.columns = df.columns.str.strip()

print("Dataset loaded successfully.")
print("Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())


# ---------------------------------------------------------
# 3. Check required columns
# ---------------------------------------------------------

required_columns = [
    "Academic Score",
    "Stream",
    "Technical Skill",
    "Career Domain",
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        "These columns were not found in the dataset: "
        f"{missing_columns}\n"
        f"Available columns: {df.columns.tolist()}"
    )


# ---------------------------------------------------------
# 4. Basic data cleaning for graphs
# ---------------------------------------------------------

for column in ["Stream", "Technical Skill", "Career Domain"]:
    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
        .replace("", pd.NA)
    )

df["Academic Score"] = pd.to_numeric(
    df["Academic Score"],
    errors="coerce"
)


# ---------------------------------------------------------
# 5. Reusable formatting function
# ---------------------------------------------------------

def format_bar_chart(
    title: str,
    xlabel: str,
    ylabel: str,
) -> None:
    """Apply consistent formatting to horizontal bar charts."""

    plt.title(
        title,
        fontsize=18,
        fontweight="bold",
        pad=14,
    )
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis="x", alpha=0.25)

    # Add numeric count labels at the end of each bar
    axis = plt.gca()

    for bar in axis.patches:
        width = bar.get_width()
        axis.text(
            width + max(width * 0.01, 5),
            bar.get_y() + bar.get_height() / 2,
            f"{int(width):,}",
            va="center",
            fontsize=11,
        )


# ---------------------------------------------------------
# Graph 1: Top 10 Technical Skills
# ---------------------------------------------------------

technical_skill_counts = (
    df["Technical Skill"]
    .dropna()
    .value_counts()
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))

technical_skill_counts.plot(kind="barh")

format_bar_chart(
    title="Top 10 Technical Skills",
    xlabel="Number of Student Profiles",
    ylabel="Technical Skill",
)

plt.tight_layout()

plt.savefig(
    OUTPUT_FOLDER / "top_technical_skills.png",
    dpi=300,
    bbox_inches="tight",
)

plt.close()


# ---------------------------------------------------------
# Graph 2: Top 10 Career Domains
# ---------------------------------------------------------

career_domain_counts = (
    df["Career Domain"]
    .dropna()
    .value_counts()
)

top_career_domains = (
    career_domain_counts
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))

top_career_domains.plot(kind="barh")

format_bar_chart(
    title="Top 10 Career Domains",
    xlabel="Number of Student Profiles",
    ylabel="Career Domain",
)

plt.tight_layout()

plt.savefig(
    OUTPUT_FOLDER / "top_career_domains.png",
    dpi=300,
    bbox_inches="tight",
)

plt.close()


# ---------------------------------------------------------
# Graph 3: Academic Score Distribution
# ---------------------------------------------------------

academic_scores = df["Academic Score"].dropna()

plt.figure(figsize=(10, 6))

plt.hist(
    academic_scores,
    bins=8,
    edgecolor="black",
    linewidth=0.8,
)

plt.title(
    "Academic Score Distribution",
    fontsize=18,
    fontweight="bold",
    pad=14,
)
plt.xlabel("Academic Score", fontsize=14)
plt.ylabel("Number of Student Profiles", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis="y", alpha=0.25)

plt.tight_layout()

plt.savefig(
    OUTPUT_FOLDER / "academic_score_distribution.png",
    dpi=300,
    bbox_inches="tight",
)

plt.close()


# ---------------------------------------------------------
# Graph 4: Student Stream Distribution
# ---------------------------------------------------------

stream_counts = (
    df["Stream"]
    .dropna()
    .value_counts()
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))

stream_counts.plot(kind="barh")

format_bar_chart(
    title="Student Stream Distribution",
    xlabel="Number of Student Profiles",
    ylabel="Stream",
)

plt.tight_layout()

plt.savefig(
    OUTPUT_FOLDER / "stream_distribution.png",
    dpi=300,
    bbox_inches="tight",
)

plt.close()


# ---------------------------------------------------------
# 6. Print actual findings in the terminal
# ---------------------------------------------------------

print("\nEDA graphs generated successfully:")
print("1. top_technical_skills.png")
print("2. top_career_domains.png")
print("3. academic_score_distribution.png")
print("4. stream_distribution.png")

if not technical_skill_counts.empty:
    print(
        "\nMost common technical skill:",
        technical_skill_counts.idxmax(),
    )
    print(
        "Technical skill count:",
        int(technical_skill_counts.max()),
    )

if not career_domain_counts.empty:
    print(
        "\nMost common career domain:",
        career_domain_counts.idxmax(),
    )
    print(
        "Career domain count:",
        int(career_domain_counts.max()),
    )

if not stream_counts.empty:
    print(
        "\nMost common stream:",
        stream_counts.idxmax(),
    )
    print(
        "Stream count:",
        int(stream_counts.max()),
    )

if not academic_scores.empty:
    print(
        "\nAverage academic score:",
        round(academic_scores.mean(), 2),
    )
    print(
        "Minimum academic score:",
        round(academic_scores.min(), 2),
    )
    print(
        "Maximum academic score:",
        round(academic_scores.max(), 2),
    )