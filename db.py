import sqlite3

def initializeTables():
    with sqlite3.connect("cell-count.db") as conn:
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
    with sqlite3.connect("cell-count.db") as conn:
        cursor = conn.cursor()
        #TODO: check if the subject already exists and get rid of this ugly try/except block
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
    with sqlite3.connect("cell-count.db") as conn:
        cursor = conn.cursor()
        #TODO: check if the sample already exists and get rid of this ugly try/except block
        try:
            cursor.execute(
                    "INSERT INTO samples (sample, sample_type, time_from_treatment_start, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte, subject, project) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                    (sample, sampleType, time_from_treatment_start, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte, subject, project))
            conn.commit()
        except sqlite3.IntegrityError:
            print("a duplicate entry was added")


def getAllSampleRows():
    with sqlite3.connect("cell-count.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM samples")
        return list(cursor.fetchall())


# TODO: rename this function to something better
def getTargetSamples():
    with sqlite3.connect("cell-count.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT s.sample
                    FROM samples s
                    JOIN subjects sub ON s.subject = sub.subject
                    WHERE s.sample_type = 'PBMC'
                        AND sub.condition = 'melanoma'
                        AND sub.treatment = 'miraclib'
                        AND sub.response = 'yes';
        """) 
        yes_responders = list(cursor.fetchall())
        cursor.execute("""
                    SELECT s.sample
                    FROM samples s
                    JOIN subjects sub ON s.subject = sub.subject
                    WHERE s.sample_type = 'PBMC'
                        AND sub.condition = 'melanoma'
                        AND sub.treatment = 'miraclib'
                        AND sub.response = 'no';
        """) 
        no_responders = list(cursor.fetchall())

        return yes_responders, no_responders

def answerQuestion():
    '''wrote this function to answer the question in the interview prompt, 
    isnt really needed for the rest of the project, but I thought it would 
    be a good idea to include it for transparency.'''
    with sqlite3.connect("cell-count.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT AVG(s.b_cell) AS avg_b_cells
                    FROM samples s
                    JOIN subjects sub ON s.subject = sub.subject
                    WHERE s.time_from_treatment_start = 0
                    AND sub.sex = 'M'
                    AND sub.condition = 'melanoma'
                    AND sub.response = 'yes';
                    """)
        return cursor.fetchone()[0]

if __name__ == "__main__":
    print(answerQuestion())

