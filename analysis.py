import load_data

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

    for row in load_data.getAllSampleRows():
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
                percentage = count / total * 100
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




if __name__ == "__main__":
    print(createFrequencyTable())

            


