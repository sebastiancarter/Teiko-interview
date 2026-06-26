"""
this file is designed to create and populate a sqlite database with data from cell-count.csv, using a schema that is left up to me to decide.

my schema is essentially as follows

table 1: subjects
subject
project
condition
age
sex
treatment
response

table 2: samples
sample
subject
sample_type
time_from_treatment_start
b_cell
cd8_t_cell
cd4_t_cell
nk_cell
monocyte

for further reference, see db.py, which contains the functions 
that create the tables and insert data into them.
"""
import db
import csv




if __name__ == "__main__":
    db.initializeTables()

    with open("cell-count.csv", 'r') as infile:
        inDict = csv.DictReader(infile)
        
        for row in inDict:
            db.addItemToSubjects(row["subject"],
                            row["project"],
                            row["condition"],
                            row["age"],
                            row["sex"],
                            row["treatment"],
                            row["response"])



            db.addItemToSamples(row["sample"], 
                            row["sample_type"],
                            row["time_from_treatment_start"],
                            row["b_cell"],
                            row["cd8_t_cell"],
                            row["cd4_t_cell"],
                            row["nk_cell"],
                            row["monocyte"],
                            row["subject"],
                            row["project"])

    print("done loading data")