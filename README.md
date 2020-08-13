# Build a COVID-19 Dashboard With Fewer Than 40 Lines of Code

Lance Reinsmith, M.D. is a radiologist and programming hobbyist who lives and works in San Antonio, TX.  Dr. Reinsmith has seen and interpreted many radiologic exams performed on COVID-19 patients at varying stages of the disease.

#### Intro

One of the difficult parts of making sense of the COVID pandemic (caused by the SARS-CoV-2 virus) is sorting through all the myriad data coming at us from every direction.  In this tutorial, I will show you a fun way of manipulating some of these data to build your own dashboard to view United States COVID-19 statistics.  Afterward, you will hopefully be able to enhance your dashboard(s) to make unique visualizations.

This project uses [Streamlit](https://www.streamlit.io/), an exciting and relatively nascent open-source data visualization project.  It makes building beautiful data visualizations as easy as writing a Python script.  If you like what you see here, I suggest you read through their [documentation](https://docs.streamlit.io/en/stable/) and follow this project as it grows.

As stated above, there are many data sources for COVID-19.  We will be using [covidtracking.com](https://covidtracking.com/) as it has a simple [REST API](https://covidtracking.com/data/api).  However, there are many [other sources](https://data.world/resources/coronavirus/) available. I also recommend checking with your local municipality for public data sources.  Remember to be respectful and follow API guidelines.

Below is a screen shot of what the finished dashboard will look like, and [here is a link](https://examplecoviddashboard.herokuapp.com/) to a live demo.

#### Let's get started!

The recommended way to install Streamlit is via pip:

```
pip install streamlit
```

Open a new Python script (I called mine `covid_dashboard.py`), and begin by importing some libraries:

```python
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
```

Streamlit does not have its own graphing functionality.  Instead, we will use [Matplotlib's](https://matplotlib.org/) pyplot to make our plots.  We need [pandas](https://pandas.pydata.org/) to manipulate the data, and we will also be using Python's built-in datetime library.

Next, we need to define a function to retrieve data from the API.  

```python
def fetch_data():
    df = pd.read_json('https://covidtracking.com/api/v1/us/daily.json')
    df['date'] = pd.to_datetime(df['date'], format="%Y%m%d")
    df.set_index('date', inplace=True)
    df.sort_index(ascending=True, inplace=True)
    return df
```

The API output is in JSON format which we can read directly into a pandas DataFrame.  We now convert the 'date' column to datetime objects and reindex the DataFrame with these.  Finally, we sort the DataFrame by these dates.

As the user interacts with our dashboard, the script is frequently re-run.  However, we don't want to poll the API every time the user changes how he/she wants to view the same data.  Streamlit simplifies this by having a `@st.cache` decorator that we can place ahead of any API call.  This way, the API is only called once despite running the `fetch_data()` function multiple times.  (This is important not to overrun the API endpoint with unnecessary calls for the exact same data over and over again.)

Our decorated function and function call should look like this:

```python
@st.cache
def fetch_data():
    df = pd.read_json('https://covidtracking.com/api/v1/us/daily.json')
    df['date'] = pd.to_datetime(df['date'], format="%Y%m%d")
    df.set_index('date', inplace=True)
    df.sort_index(ascending=True, inplace=True)
    return df
    
df = fetch_data()
```

Again, the `fetch_data()` only triggers an API call once; from then on, the data are cached.

Next, we construct a dictionary of data descriptors and their corresponding columns in the DataFrame we just constructed from the API.

```python
options = {"Cumulative Positive Results": 'positive',
    "Daily Positive Tests": 'positiveIncrease',
    "Cumulative Deaths": 'death',
    "Daily Deaths": 'deathIncrease',
    "Current Hospitalizations": 'hospitalizedCurrently',
    "Daily Hospitalizations": 'hospitalizedIncrease',
    "Cumulative Hospitalizations": 'hospitalizedCumulative', 
    "Current ICU Patients": 'inIcuCurrently', 
    "Cumulative ICU Patients": 'inIcuCumulative',
    "Current Ventilator Patients": 'onVentilatorCurrently', 
    "Cumulative Ventilator Patients": 'onVentilatorCumulative', 
    "Recovered Patients": 'recovered',
    "Daily Tests Performed": 'totalTestResultsIncrease',
    "Cumulative Tests Performed": 'totalTestResults'}
```

Now that we have collected our data, we can start the fun part: making our dashboard!  Let's give it a title:

```python
st.title('COVID-19 Dashboard: US Data')
```

And, it is good practice to reference your data source:

```python
st.subheader('Source: https://covidtracking.com')
```

Streamlit features a collapsable sidebar where you can put options menus and other things you don't want cluttering your main window.  Most Streamlit components can be put in the sidebar by calling them as methods on the `st.sidebar` object.  Let's add some date pickers for the start and end dates of our visualization.  (I'll set an arbitrary initial start date of 1-Mar-2020 and an initial end date matching the latest date in the DataFrame.)

```python
start_date = st.sidebar.date_input("Start Date", value=datetime(2020,3,1))
end_date = st.sidebar.date_input("End Date", value=df.index.max())
```

We now need to have the user pick which visualizations they want to see.  Only seeing a single category or data is boring, so we should use a multi-select.

```python
charts = st.sidebar.multiselect("Select individual charts to display:",
                options=list(options.keys()),
                default=list(options.keys())[:1])
```

The first parameter is the caption, the options are the keys of our `options` dictionary defined above, and the default is the first of those options.  This returns a list of the chosen options which we store in `charts`.

In our main window, we now loop through the `charts` list and plot each one on a single axis.

```python
for chart in charts:
    df[options[chart]].loc[start_date : end_date + timedelta(days=1)].plot(label=chart, figsize=(8,6))
    plt.xlabel('Date')
    plt.legend(loc="upper left")
```

The first line in the loop selects the column in the DataFrame corresponding to the chosen option, filters out the dates chosen, and uses the pandas plot function to plot the data from that column.  The other lines are for formatting the axis; you can customize these to change the look of your charts.

Once all the plots are created, the `pyplot` object still resides in memory, we have to tell Streamlit to show it by calling:

```python
st.pyplot()
```

And that's it!

#### Entire script

```python
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

@st.cache
def fetch_data():
    df = pd.read_json('https://covidtracking.com/api/v1/us/daily.json')
    df['date'] = pd.to_datetime(df['date'], format="%Y%m%d")
    df.set_index('date', inplace=True)
    df.sort_index(ascending=True, inplace=True)
    return df

df = fetch_data()

options = {"Cumulative Positive Results": 'positive',
    "Daily Positive Tests": 'positiveIncrease',
    "Cumulative Deaths": 'death',
    "Daily Deaths": 'deathIncrease',
    "Current Hospitalizations": 'hospitalizedCurrently',
    "Daily Hospitalizations": 'hospitalizedIncrease',
    "Cumulative Hospitalizations": 'hospitalizedCumulative', 
    "Current ICU Patients": 'inIcuCurrently', 
    "Cumulative ICU Patients": 'inIcuCumulative',
    "Current Ventilator Patients": 'onVentilatorCurrently', 
    "Cumulative Ventilator Patients": 'onVentilatorCumulative', 
    "Recovered Patients": 'recovered',
    "Daily Tests Performed": 'totalTestResultsIncrease',
    "Cumulative Tests Performed": 'totalTestResults'}

## Build page
st.title('COVID-19 Dashboard: US Data')
st.subheader('Source: https://covidtracking.com')

start_date = st.sidebar.date_input("Start Date", value=datetime(2020,3,1))
end_date = st.sidebar.date_input("End Date", value=df.index.max())

charts = st.sidebar.multiselect("Select individual charts to display:",
                options=list(options.keys()),
                default=list(options.keys())[0:1])

for chart in charts:
    df[options[chart]].loc[start_date : end_date + timedelta(days=1)].plot(label=chart, figsize=(8,6))
    plt.xlabel('Date')
    plt.legend(loc="upper left")
st.pyplot()
```

#### Launching your dashboard

Once your script is saved, you can view your dashboard by running:

```bash
$ streamlit run covid_dashboard.py
```

A browser window should open to your new, fancy dashboard!  Try changing the dates and chart types in the sidebar.  

![Dashboard](dashboard.png)

This is just a starting point.  There is a lot you can do to make it more interactive and show data in different ways.

The source code is also available at [https://github.com/lancereinsmith/covid_dashboard](https://github.com/lancereinsmith/covid_dashboard).

#### Deploying your dashboard

If you would like others to be able to see your dashboard, deploy it to Heroku on a free tier!  The following is based on an [article by Gilbert Tanner](https://gilberttanner.com/blog/deploying-your-streamlit-dashboard-with-heroku).  You will need [git](https://git-scm.com/), a [Heroku](https://www.heroku.com) account and the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) for this.

Clone my repository from GitHub.  

```bash
$ git clone https://github.com/lancereinsmith/covid_dashboard.git

$ cd covid_dashboard
```
Replace the `covid_dashboard.py` script with yours.  (You must rename your file to 'covid_dashboard.py' or edit the `Procfile` with the name of your script.)  

Next, login to Heroku with your credentials if you have not already done so.

```bash
$ heroku login
```

Create a Heroku app.  This will automatically register a remote git repository called "heroku."

```bash
$ heroku create
```

Push your code to Heroku.  The `Procfile` and `setup.sh` script will do the necessary steps to deploy your site.

```bash
$ git push heroku master
```

When Heroku is finished processing your file, open your site from the command line.

```
$ heroku open
```

If there is a problem, make sure your dyno is scaled:

```bash
heroku ps:scale web=1
```

You now have a hosted dashboard!  Check out the example: [https://examplecoviddashboard.herokuapp.com/](https://examplecoviddashboard.herokuapp.com/). (Because free-tier dynos go to sleep when not used, it may take a while for a site to launch.)

But, you don't have to stop there.  Here are some other ideas:

* Source data from different [states](https://covidtracking.com/api/v1/states/daily.json) and chart comparisons between them.
* Try calculating functions on your data, such as moving averages ([hint](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rolling.html)), to make the plots more interesting.
* Try different chart types using [matplotlib](https://matplotlib.org/gallery.html) and [seaborn](https://seaborn.pydata.org/examples/index.html).
* Allow different user input to customize the views.

Stay safe and have fun!