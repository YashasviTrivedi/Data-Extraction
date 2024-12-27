import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Disable for debugging
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up WebDriver
service = Service("/usr/local/bin/chromedriver-linux64/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open CSV file to store the data
with open('VP_data.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    try:
        # Open the Vidyut Pravah website
        driver.get("https://vidyutpravah.in/")
        wait = WebDriverWait(driver, 30)

        # Debugging: Print page source
        print(driver.page_source)

        # Check for the presence of elements in the page source
        if 'spanAllIndiaSurplus' in driver.page_source:
            print("Element spanAllIndiaSurplus is present.")
        else:
            print("Element spanAllIndiaSurplus is NOT present.")

        # Extract the data using CSS Selectors
        surplus_power = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#spanAllIndiaSurplus'))).text
        avg_mcp = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#UMCP'))).text
        demand_met_current = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#CurrentDemandMET'))).text
        demand_met_yesterday = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#PrevDemandMET'))).text
        peak_shortage = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#spanPeak'))).text
        energy = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#spanEnergy'))).text
        unconstrained_price = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#CongestionToday'))).text

        # Get the current timestamp
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        # Write the data to CSV
        writer.writerow([timestamp, surplus_power, avg_mcp, demand_met_current, demand_met_yesterday,
                         peak_shortage, energy, unconstrained_price])

        print("Data recorded at", timestamp)

    finally:
        # Close the WebDriver
        driver.quit()
