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
time_from_treatment
b_cell
cd8_t_cell
cd4_t_cell
nk_cell
monocyte


depending on where this data is coming from and that sort of a thing, I would maybe 
"""

import csv
import sqlite3

conn = sqlite3.connect("cell-count.db")

def initializeTables():
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        subject TEXT PRIMARY KEY,
        project TEXT NOT NULL,
        condition TEXT NOT NULL,
        age INTEGER,
        sex TEXT,
        treatment TEXT NOT NULL,
        response TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS samples (
        sample TEXT PRIMARY KEY,
        sample_type TEXT,
        time_from_treatment_start INTEGER,
        b_cell INTEGER,
        cd8_t_cell INTEGER,
        cd4_t_cell INTEGER,
        nk_cell INTEGER,
        monocyte INTEGER,
        project TEXT NOT NULL,
        subject TEXT NOT NULL,
        FOREIGN KEY (subject) REFERENCES subjects(subject)
    )
    """)


def addItemToSubjects(subject, project, condition, age, sex, treatment, response):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO subjects (subject, project, condition, age, sex, treatment, response) VALUES (?, ?, ?, ?, ?, ?, ?)", (subject, project, condition, age, sex, treatment, response))
        conn.commit()
    except sqlite3.IntegrityError:
        print("a duplicate subject was added")


def addItemToSamples(sample, 
                     sampleType, 
                     time_from_treatment_start, 
                     b_cell, 
                     cd8_t_cell, 
                     cd4_t_cell, 
                     nk_cell, 
                     monocyte, 
                     subject, 
                     project):
    cursor = conn.cursor()
    try:
        cursor.execute(
                "INSERT INTO samples (sample, sample_type, time_from_treatment_start, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte, subject, project) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                (sample, sampleType, time_from_treatment_start, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte, subject, project))
        conn.commit()
    except sqlite3.IntegrityError:
        print("a duplicate entry was added")


def getAllSampleRows():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM samples")
    return cursor.fetchall()



if __name__ == "__main__":
    initializeTables()

    with open("cell-count.csv", 'r') as infile:
        inDict = csv.DictReader(infile)
        
        for row in inDict:
            addItemToSubjects(row["subject"],
                              row["project"],
                              row["condition"],
                              row["age"],
                              row["sex"],
                              row["treatment"],
                              row["response"])



            addItemToSamples(row["sample"], 
                             row["sample_type"],
                             row["time_from_treatment_start"],
                             row["b_cell"],
                             row["cd8_t_cell"],
                             row["cd4_t_cell"],
                             row["nk_cell"],
                             row["monocyte"],
                             row["subject"],
                             row["project"])

    print(getBcellColumn("b_cell", "samples"))


