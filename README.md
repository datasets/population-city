<a className="gh-badge" href="https://datahub.io/core/population-city"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

UNSD Demographic Statistics: City population by sex, city and city type.

## Data
Source: [UNData. UNSD Demographic Statistics](http://data.un.org/Data.aspx?d=POP&f=tableCode:240).

Contains two CSV datasets:
  1. unsd-citypopulation-year-both.csv. Size: 4.4 MB
  2. unsd-citypopulation-year-fm.csv. Size: 6.8 MB

Final 222 lines in both datasets contain original notes.

#### Updates
Last update in UNdata: 17 Sep 2024

Next update in UNdata: 01 Feb 2025

#### About the United Nations Statistics Division
The United Nations Statistics Division collects, compiles and disseminates official demographic and social statistics on a wide range of topics. Data have been collected since 1948 through a set of questionnaires dispatched annually to over 230 national statistical offices and have been published in the Demographic Yearbook collection. The Demographic Yearbook disseminates statistics on population size and composition, births, deaths, marriage and divorce, as well as respective rates, on an annual basis. The Demographic Yearbook census datasets cover a wide range of additional topics including economic activity, educational attainment, household characteristics, housing characteristics, ethnicity, language, foreign-born and foreign population. The available Population and Housing Censuses' datasets reported to UNSD for the censuses conducted worldwide since 1995, are now available in UNdata.

## Preparation

Run the requirements through `pip` in order to install all required packages to run the script.

`pip install -r scripts/requirements.txt`

The process is recorded and automated in a Python script:

`scripts/process.py`

## Automation

Up-to-date (auto-updates each 2 month) population-city dataset could be found on the datahub.io:
https://datahub.io/core/population-city

## License
This data package is licensed under a [ODC Public Domain Dedication and Licence (PDDL)](http://opendatacommons.org/licenses/pddl/1.0/).


