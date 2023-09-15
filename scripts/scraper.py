from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd


# Set up the Selenium webdriver for Chrome
chromeOptions = Options()
chromeOptions.headless = True
driver = webdriver.Chrome(options=chromeOptions)

# website url
url = "http://data.un.org/Data.aspx?d=POP&f=tableCode:240"


def download_data():
    print("Downloading Data...")
    try:
        # Open the website
        driver.get(url)

        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )

        # Get the page source after it's fully loaded
        page_source = driver.page_source

        # Find all table elements on the webpage
        tables = driver.find_elements(By.TAG_NAME, "table")

        dataframes = []
        for table in tables:
            table_html = table.get_attribute("outerHTML")
            df = pd.read_html(table_html, flavor="bs4")[0]
            print(df)
            dataframes.append(df)

        combined_df = pd.concat(dataframes, ignore_index=True)

        # cleaning the data to remove rows with no information
        rows_to_delete = [0, 1, 2]
        # Delete selected rows
        combined_df = combined_df.drop(rows_to_delete)
        # rename the "Unnamed" field to "Value Footnotes"
        combined_df.rename(columns={"Unnamed: 10": "Value Footnotes"}, inplace=True)
        # # convert some fields to the appropriate datatype
        combined_df[["Year", "Source Year", "Value Footnotes"]] = combined_df[
            ["Year", "Source Year", "Value Footnotes"]
        ].astype("Int64")
        # select final preprocessed data
        final_df = combined_df[
            [
                "Country or Area",
                "Year",
                "Area",
                "Sex",
                "City",
                "City type",
                "Record Type",
                "Reliability",
                "Source Year",
                "Value",
                "Value Footnotes",
            ]
        ]
        # Save the DataFrame to a CSV file
        csv_filename = "./output.csv"
        final_df.to_csv(csv_filename, index=False)
        print(f"DataFrame saved to {csv_filename}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the WebDriver
        driver.quit()
