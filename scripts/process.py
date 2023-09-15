from scraper import download_data
import pandas as pd
import sqlite3
import csv
import os


def load_to_DB():
    """
    Creates a table and loads the preprocessed data into the database table staged for transform.
    Args:
        None
    """
    df = pd.read_csv("./output.csv")

    # define the sqlite database path
    db_file = "population-cities.sqlite"

    # Createdatabase connection
    conn = sqlite3.connect(db_file)

    table_name = "population"
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

    print("Data successfully loaded")


def update_data():
    """Fetches each of the transformed data from the DB and updates the files"""
    # transform and update unsd-citypopulation-year-fm.csv
    OUTFILE = "./data/unsd-citypopulation-year-fm.csv"
    DBFILE = "population-cities.sqlite"
    HEADERS = [
        "Country or Area",
        "Year",
        "Area",
        "Sex",
        "City",
        "City Type",
        "Record Type",
        "Reliability",
        "Source Year",
        "Value",
        "Value Footnotes",
    ]
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    sql = """SELECT * FROM population
             WHERE sex = 'Male' OR sex = 'Female'
             """
    with open(OUTFILE, "a", newline="") as outcsv:
        writer = csv.writer(outcsv, lineterminator="\n")
        # writer.writerow(HEADERS)
        for row in c.execute(sql):
            writer.writerow(row)

    # transform and update unsd-citypopulation-year-both.csv
    OUTFILE = "./data/unsd-citypopulation-year-both.csv"
    c = conn.cursor()
    sql = """SELECT * FROM population
             WHERE sex = 'Both Sexes'
             """
    with open(OUTFILE, "a", newline="") as outcsv:
        writer = csv.writer(outcsv, lineterminator="\n")
        # writer.writerow(HEADERS)
        for row in c.execute(sql):
            writer.writerow(row)
    print("files have been successfully updated")


def remove_duplicates_in_csv(file_path: str):
    """
    Checks and remove duplicates from the last 100 row records as file keeps
    populating.

    Args:
        file_path: directory path to the file to update
    """
    df = pd.read_csv(file_path)

    # Get the last 100 rows
    last_100_rows = df.iloc[-100:]

    # Remove any duplicate rows from the last 100 rows
    df = df.drop_duplicates(subset=last_100_rows.columns)

    # update file
    df.to_csv(file_path, index=False)

    print(f"Duplicate records removed from the last 100 rows of {file_path}.")


def run():
    # Download data
    download_data()

    # load preprocessed data to DB
    load_to_DB()

    # update the UN data
    update_data()

    # check and remove any duplicated records from the last 100 records of unsd-citypopulation-year-fm.csv
    remove_duplicates_in_csv("./data/unsd-citypopulation-year-fm.csv")

    # check and remove any duplicated records from unsd-citypopulation-year-both.csv
    remove_duplicates_in_csv("./data/unsd-citypopulation-year-both.csv")

    # clear preprocessed csv file and db file for next run
    os.remove("./output.csv")
    os.remove("./population-cities.sqlite")


if __name__ == "__main__":
    run()
