import load_data




# Create a frequency table for each sample, with the total count of cells and the percentage of each cell type.
def createFrequencyTable():
    allRows = load_data.getAllSampleRows()

    # Create a dictionary to hold the frequency table data 
    tableDict = {"sample": list(), "total_count": list(), "population": list(), "count": list(), "percentage": list()}
    cellList = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]
    for row in allRows:

        totalCount = 0
        # Unpack the row into variables
        (sample, 
        sample_type, 
        time_from_treatment_start, 
        b_cell, 
        cd8_t_cell, 
        cd4_t_cell, 
        nk_cell, 
        monocyte,
        project,
        subject) = row 

        # Create a dictionary for the current row, 
        # this will make it easier to access the cell counts by name
        # but its mostly because my initial approach used a dictionary, might rewrite this later
        rowDict =  {"sample": sample, 
                    "b_cell": b_cell, 
                    "cd8_t_cell": cd8_t_cell, 
                    "cd4_t_cell": cd4_t_cell, 
                    "nk_cell": nk_cell, 
                    "monocyte": monocyte}
         
        # looping through to get the counts
        for cell in cellList:
            tableDict["sample"].append(rowDict["sample"])
            count = rowDict[cell]
            tableDict["count"].append(count)
            totalCount+= count

        # looping through again to get the percentages
        for cell in cellList:
            tableDict["total_count"].append(totalCount)
            count = rowDict[cell]
            if totalCount != 0:
                percentage = count/totalCount * 100
                tableDict["percentage"].append(percentage) 
            else:
                tableDict["percentage"].append(None)

    return tableDict




if __name__ == "__main__":
    print(createFrequencyTable())

            


