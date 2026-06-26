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

    # Sidebar filters
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

def advancedAnalysisPage():
    st.title("Advanced Analysis")
    st.markdown(
        "Comparing relative frequencies of immune cell populations between "
        "**responders** (response = yes) and **non‑responders** (response = no) — "
        "PBMC samples only, melanoma patients on miraclib."
    )

    plot_data, p_values, summary_rows = analysis.statisticalAnalysis()

    # summary tavle which shows the mean relative frequencies and p-values for each cell population
    st.subheader("Mean relative frequencies & p‑values")
    st.dataframe(
        summary_rows,
        use_container_width=True,
        hide_index=True,
        column_config={
            "p-value": st.column_config.NumberColumn(format="%.4f"),
            "Responder mean %": st.column_config.NumberColumn(format="%.2f %%"),
            "Non-responder mean %": st.column_config.NumberColumn(format="%.2f %%"),
            "Difference in means": st.column_config.NumberColumn(format="%.2f %%"), 
        },
    )

    # significance caption
    st.caption("\* p < 0.05 \*\* p < 0.01 \*\*\* p < 0.001  —  Mann–Whitney U test")
    st.write("So we can see from our mann-whitney U test that there are significant differences between the CD4 T cell counts of responders and non-responders, with a p-value of 0.0134. " \
             "\nThis suggests that the CD4 T cell counts could be a useful marker for predicting response to miraclib treatment in melanoma patients.")
    # boxplots
    st.subheader("Boxplots")
    fig = analysis.buildBoxplotFigure(plot_data, p_values)
    st.pyplot(fig)

def main():
    page = navBar()

    if page == "Relative Frequency Table":
        relativeFrequencyTablePage()
    elif page == "Advanced Analysis":
        advancedAnalysisPage()

main()