import sqlite3

def initializeTables():
    with sqlite3.connect("cell-count.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample TEXT NOT NULL,
            sample_type TEXT,
            time_from_treatment_start INTEGER,
            b_cell INTEGER,
            cd8_t_cell INTEGER,
            cd4_t_cell INTEGER,
            nk_cell INTEGER,
            monocyte INTEGER,
            project TEXT NOT NULL,
            subject_id INTEGER NOT NULL,
            FOREIGN KEY (subject_id) REFERENCES subjects(id)
        )
        """)


def addItemToSubjects(subject, project, condition, age, sex, treatment, response):
    with sqlite3.connect("cell-count.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT subject, project FROM subjects WHERE subject = ?", (subject,))
        output = cursor.fetchone()
        if output is not None:
            dbSubject, dbProject = output
        else:
            dbSubject, dbProject = None, None
        
        # we are ok with subjects reoccuring in different projects, but not with the same subject/project combination
        if dbSubject == subject and dbProject == project:
            return  # subject already exists in the database, do not insert again  
        
        cursor.execute("INSERT INTO subjects (subject, project, condition, age, sex, treatment, response) VALUES (?, ?, ?, ?, ?, ?, ?)", (subject, project, condition, age, sex, treatment, response))
        conn.commit()


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
        cursor.execute("SELECT sample, project FROM samples WHERE sample = ?", (sample,))
        output = cursor.fetchone()
        if output is not None:
            dbSample, dbProject = output
        else:
            dbSample, dbProject = None, None

        # we are ok with sample numbers reoccuring in different projects, but not with the same sample/project combination
        if dbSample == sample and dbProject == project:
            return  # sample already exists in the database, do not insert again
        
        # resolve the surrogate id for the subject
        cursor.execute("SELECT id FROM subjects WHERE subject = ?", (subject,))
        row = cursor.fetchone()
        if row is None:
            raise ValueError(f"Subject '{subject}' not found in subjects table")
        subject_id = row[0]
        cursor.execute(
                "INSERT INTO samples (sample, sample_type, time_from_treatment_start, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte, subject_id, project) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                (sample, sampleType, time_from_treatment_start, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte, subject_id, project))
        conn.commit()


def getAllSampleRows():
    with sqlite3.connect("cell-count.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT s.sample, s.sample_type, s.time_from_treatment_start, "
            "       s.b_cell, s.cd8_t_cell, s.cd4_t_cell, s.nk_cell, s.monocyte, "
            "       s.project, sub.subject "
            "FROM samples s JOIN subjects sub ON s.subject_id = sub.id"
        )
        return list(cursor.fetchall())


# TODO: rename this function to something better
def getTargetSamples():
    with sqlite3.connect("cell-count.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT s.sample
                    FROM samples s
                    JOIN subjects sub ON s.subject_id = sub.id
                    WHERE s.sample_type = 'PBMC'
                        AND sub.condition = 'melanoma'
                        AND sub.treatment = 'miraclib'
                        AND sub.response = 'yes';
        """) 
        yes_responders = list(cursor.fetchall())
        cursor.execute("""
                    SELECT s.sample
                    FROM samples s
                    JOIN subjects sub ON s.subject_id = sub.id
                    WHERE s.sample_type = 'PBMC'
                        AND sub.condition = 'melanoma'
                        AND sub.treatment = 'miraclib'
                        AND sub.response = 'no';
        """) 
        no_responders = list(cursor.fetchall())

        return yes_responders, no_responders

def getTargetSamplesAtBaseline():
    """Return all melanoma / PBMC / miraclib / time=0 rows with subject metadata."""
    with sqlite3.connect("cell-count.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.sample, s.project, sub.subject, sub.response, sub.sex
            FROM samples s
            JOIN subjects sub ON s.subject_id = sub.id
            WHERE s.sample_type = 'PBMC'
              AND sub.condition = 'melanoma'
              AND sub.treatment = 'miraclib'
              AND s.time_from_treatment_start = 0;
        """)
        return list(cursor.fetchall())
            


def answerQuestion():
    """wrote this function to answer the question in the interview prompt, 
    isnt really needed for the rest of the project, but I thought it would 
    be a good idea to include it for transparency."""
    with sqlite3.connect("cell-count.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT AVG(s.b_cell) AS avg_b_cells
                    FROM samples s
                    JOIN subjects sub ON s.subject_id = sub.id
                    WHERE s.time_from_treatment_start = 0
                    AND sub.sex = 'M'
                    AND sub.condition = 'melanoma'
                    AND sub.response = 'yes';
                    """)
        return cursor.fetchone()[0]

if __name__ == "__main__":
    print(answerQuestion())

