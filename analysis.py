import db
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for Streamlit
import matplotlib.pyplot as plt
from scipy import stats
import json
import os

CELL_POPULATIONS = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]
POPULATION_LABELS = {
    "b_cell": "B cell",
    "cd8_t_cell": "CD8+ T cell",
    "cd4_t_cell": "CD4+ T cell",
    "nk_cell": "NK cell",
    "monocyte": "Monocyte",
}


def createFrequencyTable():
    """Builds a frequency table of cell populations per sample.

    Returns a list of dicts, one per cell-population/sample combination,
    with keys: Sample, Population, Count, Total Count, Percentage.
    """
    rows = []

    for row in db.getAllSampleRows():
        (
            sample,
            _sample_type,
            _time_from_treatment_start,
            b_cell,
            cd8_t_cell,
            cd4_t_cell,
            nk_cell,
            monocyte,
            _project,
            _subject,
        ) = row

        counts = {
            "b_cell": b_cell,
            "cd8_t_cell": cd8_t_cell,
            "cd4_t_cell": cd4_t_cell,
            "nk_cell": nk_cell,
            "monocyte": monocyte,
        }

        total = sum(counts.values())

        for cell_population in CELL_POPULATIONS:
            count = counts[cell_population]
            if total != 0:
                percentage = round((count / total * 100), 2)
            else:
                percentage = None
            
            rows.append({
                "Sample": sample,
                "Total Count": total,
                "Population": POPULATION_LABELS[cell_population],
                "Count": count,
                "Percentage": percentage,
            })

    return rows



def statisticalAnalysis():
    """Compare relative frequencies: responders vs non-responders (PBMC only).
    """
    frequency_table = createFrequencyTable()

    # Get sample IDs for each response group
    yes_samples, no_samples = db.getTargetSamples()
    # TODO: maybe get getTargetSamples() to return a normal list instead of a list of tuples of single elements
    yes_samples = {row[0] for row in yes_samples}
    no_samples = {row[0] for row in no_samples}

    # Group percentage values by population and response
    plot_data = {}
    for pop in CELL_POPULATIONS:
        label = POPULATION_LABELS[pop]
        yes_percentages = []
        no_percentages = []
        for row in frequency_table:
            if row["Population"] == label:
                if row["Sample"] in yes_samples:
                    yes_percentages.append(row["Percentage"])
                elif row["Sample"] in no_samples:
                    no_percentages.append(row["Percentage"])

        plot_data[label] = {"Yes": yes_percentages, "No": no_percentages}

    # Mann–Whitney U test per population
    p_values = {}
    summary_rows = []
    for label in plot_data:
        data = plot_data[label]

        yes_vals = data["Yes"]
        no_vals = data["No"]
        if len(yes_vals) >= 3 and len(no_vals) >= 3:
            _stat, p = stats.mannwhitneyu(
                yes_vals, no_vals, alternative="two-sided"
            )
            p_values[label] = p
        else:
            p_values[label] = None


        if len(yes_vals):
            yes_mean = round(sum(yes_vals) / len(yes_vals), 2)
        else:
            yes_mean = None
        
        if len(no_vals):
            no_mean = round(sum(no_vals) / len(no_vals), 2)
        else:
            no_mean = None

        if len(yes_vals) > 0 and len(no_vals) > 0:
            # TODO: rename this later, bad name
            average_difference = round((sum(yes_vals) / len(yes_vals)) - (sum(no_vals) / len(no_vals)), 2)
        else:
            average_difference = None



        summary_rows.append({
            "Population": label,
            "Responder mean %": yes_mean, 
            "Non-responder mean %": no_mean,
            "Difference in means": average_difference,
            "p-value": p_values[label],
        })

    return plot_data, p_values, summary_rows

def buildBoxplotFigure(plot_data, p_values):
    """Create a matplotlib Figure with side‑by‑side boxplots."""
    populations = list(plot_data.keys())
    n = len(populations)
    fig, axes = plt.subplots(1, n, figsize=(3.2 * n, 5), sharey=True)
    if n == 1:
        axes = [axes]

    for ax, pop in zip(axes, populations):
        data = plot_data[pop]
        bp = ax.boxplot(
            [data["Yes"], data["No"]],
            tick_labels=["Yes", "No"],
            patch_artist=True,
            widths=0.5,
        )
        bp["boxes"][0].set_facecolor("#4CAF50")
        bp["boxes"][1].set_facecolor("#F44336")
        for median in bp["medians"]:
            median.set_color("white")
            median.set_linewidth(1.5)

        ax.set_title(pop, fontsize=12, fontweight="bold")
        ax.set_ylabel("Relative frequency (%)")

        # Significance annotation
        p = p_values.get(pop)
        if p is not None:
            if p < 0.001:
                sig = "***"
            elif p < 0.01:
                sig = "**"
            elif p < 0.05:
                sig = "*"
            else:
                sig = f"p={p:.3f}"
            ax.text(
                0.5, 0.93, sig,
                transform=ax.transAxes, ha="center", va="top",
                fontsize=11, fontweight="bold",
            )

    fig.suptitle(
        "Cell Population Relative Frequencies: Responders vs Non‑responders",
        fontsize=14, fontweight="bold", y=1.02,
    )
    fig.tight_layout()
    return fig


def dataSubsetSummary():
    """Summarise the baseline (time=0) melanoma / PBMC / miraclib subset.
    """
    rows = db.getTargetSamplesAtBaseline()
    # rows: [(sample, project, subject, response, sex), ...]

    # Count by project
    project_counts = {}
    for sample, project, subject, response, sex in rows:
        project_counts[project] = project_counts.get(project, 0) + 1

    # Count unique subjects by response
    response_subjects = {}
    for sample, project, subject, response, sex in rows:
        response_subjects.setdefault(response, set()).add(subject)
    response_counts = {k: len(v) for k, v in response_subjects.items()}

    # Count unique subjects by sex
    sex_subjects = {}
    for sample, project, subject, response, sex in rows:
        sex_subjects.setdefault(sex, set()).add(subject)
    sex_counts = {k: len(v) for k, v in sex_subjects.items()}

    total_samples = len(rows)

    # Build summary table
    summary = []
    for project, count in sorted(project_counts.items()):
        summary.append({
            "Category": "Project",
            "Group": project,
            "Count": count,
            "Pct of subset": round(count / total_samples * 100, 1),
        })
    for resp, count in sorted(response_counts.items()):
        summary.append({
            "Category": "Response",
            "Group": resp,
            "Count": count,
            "Pct of subset": round(count / len({r[2] for r in rows}) * 100, 1),
        })
    for sex, count in sorted(sex_counts.items()):
        summary.append({
            "Category": "Sex",
            "Group": sex,
            "Count": count,
            "Pct of subset": round(count / len({r[2] for r in rows}) * 100, 1),
        })

    return summary




OUTPUT_DIR = "output"


def write_json(filename, data):
    """Write a dict/list to a JSON file inside OUTPUT_DIR."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def save_all_results():
    """Run the full analysis and persist every output to disk."""
    # Frequency table
    freq = createFrequencyTable()
    write_json("frequency_table.json", freq)

    # Data subset summary (baseline demographics)
    subset = dataSubsetSummary()
    write_json("baseline_subset_summary.json", subset)

    # Statistical analysis
    plot_data, p_values, summary = statisticalAnalysis()
    write_json("responder_summary.json", summary)

    # Boxplot data (percentages per population per response group)
    write_json("boxplot_data.json", plot_data)

    # Boxplot figure as PNG
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fig = buildBoxplotFigure(plot_data, p_values)
    fig.savefig(
        os.path.join(OUTPUT_DIR, "boxplot.png"),
        dpi=150,
        bbox_inches="tight",
    )
    plt.close(fig)

    print(f"All results saved to ./{OUTPUT_DIR}/")


if __name__ == "__main__":
    save_all_results()

            


