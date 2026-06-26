import streamlit as st
import analysis




def navBar():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ("Relative Frequency Table", "Advanced Analysis"),
    )
    return page

def relativeFrequencyTablePage():
    st.set_page_config(page_title="Cell Frequency Analysis", layout="wide")
    st.title("Cell Type Frequency Analysis")

    rows = analysis.createFrequencyTable()

    # 
    all_populations = set()
    for row in rows:
        all_populations.add(row["Population"])

    # --- Sidebar filters ---
    st.sidebar.header("Filters")
    selected_populations = st.sidebar.multiselect(
        "Populations", options=all_populations, default=all_populations
    )

    # Apply filters

    filteredRows = []
    for row in rows:
        if row["Population"] in selected_populations:
            filteredRows.append(row)



    # little bit of logic to calculate the total number of samples, populations, and cells
    unique_samples = set()
    unique_pops = set()
    total_cells = 0
    for row in filteredRows:
        unique_samples.add(row["Sample"])
        unique_pops.add(row["Population"])
        total_cells += row["Count"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Samples", len(unique_samples))
    col2.metric("Total Populations", len(unique_pops))
    col3.metric("Total Cells", f"{total_cells:,}")

    st.subheader("Frequency Table")
    st.dataframe(
        filteredRows,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Percentage": st.column_config.NumberColumn(format="%.2f %%"),
            "Count": st.column_config.NumberColumn(format="%d"),
            "Total Count": st.column_config.NumberColumn(format="%d"),
        },
    )


def main():
    page = navBar()

    if page == "Relative Frequency Table":
        relativeFrequencyTablePage()
    elif page == "Advanced Analysis":
        st.title("Advanced Analysis")
        st.write("This is the advanced analysis page.")

main()