import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--no-sandbox")  # Required in some CI environments
chrome_options.add_argument("--disable-dev-shm-usage")  # Handle shared memory issues

service = Service("/usr/local/bin/chromedriver-linux64/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

with open('VP_data.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    try:
        # Open the Vidyut Pravah website
        driver.get("https://vidyutpravah.in/")
        driver.maximize_window() # For maximizing window
        driver.implicitly_wait(100) # gives an implicit wait for 100 seconds

        # Extract the data
        surplus_power = driver.find_element(By.XPATH, '//*[@id="spanAllIndiaSurplus"]').text
        avg_mcp = driver.find_element(By.XPATH, '//*[@id="UMCP"]').text
        demand_met_current = driver.find_element(By.XPATH, '//*[@id="CurrentDemandMET"]').text
        demand_met_yesterday = driver.find_element(By.XPATH, '//*[@id="PrevDemandMET"]').text
        peak_shortage = driver.find_element(By.XPATH, '//*[@id="spanPeak"]').text
        energy = driver.find_element(By.XPATH, '//*[@id="spanEnergy"]').text
        unconstrained_price = driver.find_element(By.XPATH, '//*[@id="CongestionToday"]').text

        # Get the current timestamp
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        # Write the data to CSV
        writer.writerow([timestamp, surplus_power, avg_mcp, demand_met_current, demand_met_yesterday,
                             peak_shortage, energy, unconstrained_price])

        print("Data recorded at", timestamp)

    finally:
        # Close the WebDriver
        driver.quit()


