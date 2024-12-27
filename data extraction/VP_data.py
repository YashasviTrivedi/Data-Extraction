import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--no-sandbox")  # Required in some CI environments
chrome_options.add_argument("--disable-dev-shm-usage")  # Handle shared memory issues

# Set up WebDriver
# Use the ChromeDriver from the system path
service = Service("/usr/local/bin/chromedriver-linux64/chromedriver")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

#driver_path = "C:/Users/Yashashvi/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"  # Replace with the correct path
#service = Service(driver_path)
#driver = webdriver.Chrome(service=service)

# Open CSV file to store the data
with open('VP_data.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    try:
        # Open the Vidyut Pravah website
        driver.get("https://vidyutpravah.in/")

        with open("page_source.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)


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


