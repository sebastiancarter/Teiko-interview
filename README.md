### Loblaw bio analysis

___
first run

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