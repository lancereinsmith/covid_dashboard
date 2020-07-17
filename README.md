# Make Your Own COVID-19 Dashboard in Less Than 40 Lines of Code

One of the difficult parts of making sense of the SARS-CoV-2 pandemic is making sense of all the myriad data flying from every corner.  In this tutorial, I will show you a fun way of manipulating some of these virus data to build your own Dashboard to view United States COVID-19 statistics.  

This project uses [Streamlit](https://www.streamlit.io/), which is an exciting and relatively nascent project as of this writing.  It makes building beautiful app websites for displaying data visualizations as easy as writing a single Python script.  If you like what you see here, I suggest you read through their [documentation](https://docs.streamlit.io/en/stable/) and follow this project as it grows.

As stated above, there are many data sources for COVID-19.  We will be using [covidtracking.com](https://covidtracking.com/) as it has a simple [REST API](https://covidtracking.com/data/api).  However, I have seen [other sources](https://covid19api.com/), and I also recommend checking with your local municipality for pubic datasources.

Install streamlit using pip:

```
pip install streamlit
```

Open a new script, and begin by importing some packages:

```
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
```

Streamlit allows you to 











https://gilberttanner.com/blog/deploying-your-streamlit-dashboard-with-heroku

```
$ git clone https://github.com/lancereinsmith/covid_dashboard.git

$ cd covid_dashboard
```
```
$ heroku login

$ heroku create

$ git push heroku master

$ heroku open
```

heroku ps:scale web=1