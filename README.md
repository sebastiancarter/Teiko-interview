# Loblaw bio analysis

### setup / usage guide

```
make setup
```
This will install all dependencies using pip.

Then run

```
make pipeline
```

This will create and populate the sql database needed for this project.

Finally, run

```
make dashboard
```
To create the streamlit dashboard you can use to view the analysis. This should run out of `http://localhost:8501`. To see the different steps in the analysis, click on different pages in the sidebar



## design rationale
### schema
I chose to split the Data between samples and subjects because it seemed like the simplest and most open ended way of doing things. I like to think that generally speaking simple is good, and the way I've set up this database is simple enough you can do sample level analysis pretty easily, but also lets you focus on subjects just by themselves, which seems to me like the two most important areas in the dataset. I tried future proofing by setting up unique IDs for every entry, which lets us have duplicate subject and sample values as long as they are in different projects. This could be important: its possible that some results from a subject are so peculiar that more data is needed to understand why they are the way they are, and without the ID the dataset used, that may be pretty difficult. I also did error correction so multiple entries cant be made from the same ID in the same project

I think the biggest thing that can be done for scalability is using sqlalchemy, which would allow for any sql database to be used, which is nice given sqlite is pretty small, but full disclosure this is my first technical interview involving sql and after googling it, I found a bunch of people saying not to use sqlalchemy because the point is to show understanding of sql commands, so I decided to just use sqlite3 instead.

### code design
I very much like to structure my code in a kind of task oriented way. I have db.py to handle almost all interactions with the database, including the creation and populating of the database, but also database calls that need to be made for analysis to get data. load_data essentially just runs the functions in db.py necessary to setup and populate the database. I like my db functions to be pretty much hardcoded to avoid any kind of sql injection attacks.

Analysis.py is where I create all tables and plots that are to be shown on the dashboard. Originally, I was going to have the dashboard call functions in analysis.py, as I like things to be live and I think having the capability to update your dashboard as data flows in is pretty neat. I later realized after looking carefully at the instructions that the generated tables and plots are supposed to be saved off in an output folder, and then loaded into the dashboard, so I switched things around to do that.

Finally, my dashboard is using streamlit. I really like streamlit, I've been using it for maybe 4 or 5 years now, and it's awesome for any kind of prototyping or quick sketch ups you might like, so it seemed like a pretty good fit for this. I added an option to filter for the cell type frequency analysis, just to mess around a bit.