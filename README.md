<a className="gh-badge" href="https://datahub.io/core/population-city"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

# City population

Population of cities by year, for both sexes and for females and males, from the UN Statistics Division (UNSD Demographic Statistics). The figures come from national statistical offices through the UN Demographic Yearbook.

Column definitions and types are in `datapackage.json`.

## Data

* `data/unsd-citypopulation-year-both.csv` has the figures for both sexes.
* `data/unsd-citypopulation-year-fm.csv` has the figures for females and males, one row each.
* Each data file has a footnotes file next to it: `data/unsd-citypopulation-year-both-footnotes.csv` and `data/unsd-citypopulation-year-fm-footnotes.csv`.

Columns of the two data files:

| Column | Meaning |
|---|---|
| `Country or Area` | Country or area, as named by the UN, for example `Åland Islands` |
| `Year` | Reference year of the figure |
| `Area` | Part of the city covered, for example `Total` |
| `Sex` | `Both Sexes` in the first file; `Female` or `Male` in the second |
| `City` | City name as given by the UN, often in capitals, for example `MARIEHAMN` |
| `City type` | `City proper` or `Urban agglomeration` |
| `Record Type` | Kind of record, for example `Estimate - de jure` or `Census - de facto - complete tabulation` |
| `Reliability` | For example `Final figure, complete` or `Provisional figure` |
| `Source Year` | Year of the source the figure was taken from |
| `Value` | Population. A few figures have a decimal part, for example `11911.5` |
| `Value Footnotes` | Footnote numbers for the figure, separated by commas (for example `4,5`). Empty when there is none |

Columns of the footnotes files: `footnoteSeqID` (the footnote number) and `Footnote` (its text).

### Known limitations

* The same city can have several rows for the same year, from different sources. They differ in `Record Type`, `Reliability` or `Source Year`. Choose one before you count or compare.
* A city can be listed both as `City proper` and as `Urban agglomeration`. The agglomeration normally includes the city proper, so adding the two counts people twice.
* Footnote numbers belong to one file. Number `4` in the first file does not mean the same as number `4` in the second. The UN can also number its footnotes differently each time the data is exported, so a number can change when the data is rebuilt. Always use the footnotes file that was committed with the data file.
* `Value Footnotes` can hold several numbers in one cell (`4,5`). Split it on commas before you look the numbers up.
* All fields are in quotes and lines end with a carriage return and a line feed (`\r\n`), as in the UN export. Any CSV reader handles this.
* With pandas: `pd.read_csv("data/unsd-citypopulation-year-both.csv")`. `Year`, `Source Year` and `Value` are numbers.

## Data sources

* [UN data](https://data.un.org/legacy/Data.aspx?d=POP&f=tableCode:240): UNSD Demographic Statistics, table "City population by sex, city and city type". It provides all figures and footnotes. Licence: the [UN data conditions of use](https://data.un.org/legacy/Host.aspx?Content=UNdataUse). They say all data and metadata may be copied freely, duplicated and further distributed, provided UN data is cited as the reference.

Changes made to the source data: the UN export has a table of footnotes at its end. The update script moves that table into its own footnotes file. Nothing else in the figures is changed.

Not endorsed by, or affiliated with, the United Nations.

## Preparation

You need Python 3.12 or greater. To rebuild the data from the repository root:

```bash
pip install -r scripts/requirements.txt
python scripts/process.py
```

The script downloads the two tables from UN data, moves the footnotes into their own files and records the date of the last UN update in `last_updated` in `datapackage.json`. It stops with an error if the UN site does not return the files it expects.

A GitHub workflow runs the script on the first day of January, March, May, July, September and November, and when started by hand. It commits `data/` and `datapackage.json` if they changed.

The data is also published on [datahub.io](https://datahub.io/core/population-city).

## License

The UN data conditions of use allow the figures and footnotes to be copied, duplicated and further distributed free of charge, as long as UN data is cited as the reference. See [ATTRIBUTION.txt](ATTRIBUTION.txt).

The maintainers offer this package under the [Open Data Commons Public Domain Dedication and License][pddl] (PDDL) 1.0. That applies to their own work: the update script, the column definitions and the file layout. It does not replace the UN conditions of use.

[pddl]: https://opendatacommons.org/licenses/pddl/1.0/
