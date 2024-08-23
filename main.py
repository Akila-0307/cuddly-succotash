import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import streamlit as st
import pandas as pd

# MySQL database connection settings
username = 'root'
password = 'root'
host = '127.0.0.1'
database = 'scraping'

# Establish a connection to the MySQL database
cnx = mysql.connector.connect(
    user='root',
    password='root',
    host='127.0.0.1',
    database='scraping'
)

# Create a cursor object to execute SQL queries
cursor = cnx.cursor()

# Redbus website URL
url = "(link unavailable)"

# Set up Selenium webdriver
driver = webdriver.Chrome()

# Navigate to Redbus website
driver.get("(link unavailable)")

# Wait for the page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="homeV2-root"]/div[3]/div[1]/div[1]')))

# Get bus routes data
bus_routes = driver.find_elements(By.XPATH, '//*[@id="toc_id_3"]')

# Create a list to store data
data = []

# Extract data from each bus route
for route in bus_routes:
    route_name = route.find_element(By.XPATH, './/*[@id="root"]/div/div[4]/div[2]/div[1]/a').text
    route_link = route.find_element(By.XPATH, './/*[@id="fixer"]/div/div/div[1]/div/span[2]').get_attribute('href')
    bus_name = route.find_element(By.XPATH, './/span[@id="26348503"]/div/div[1]/div[1]/div[1]/div[1]').text
    bus_type = route.find_element(By.XPATH, './/span[@id="26348503"]/div/div[1]/div[1]/div[1]/div[2]').text
    departing_time = route.find_element(By.XPATH, './/span[@id="26348503"]/div/div[1]/div[1]/div[2]/div[1]').text
    duration = route.find_element(By.XPATH, './/span[@id="26348503"]/div/div[1]/div[1]/div[3]/div').text
    reaching_time = route.find_element(By.XPATH, './/span[@id="26348503"]/div/div[1]/div[1]/div[4]/div[1]').text
    star_rating = route.find_element(By.XPATH, './/span[@id="26348503"]/div/div[1]/div[1]/div[5]/div[1]/div/span').text
    price = route.find_element(By.XPATH, './/span[@id="26348503"]/div/div[1]/div[1]/div[6]/div/div[2]/span').text
    seats_available = route.find_element(By.XPATH, './/span[@id="26348503"]/div/div[1]/div[1]/div[7]/div[1]/span').text

# Append data to the list
    data.append({
        'route_name': route_name.strip(),
        'route_link': route_link,
        'bus_name': bus_name.strip(),
        'bus_type': bus_type.strip(),
        'departing_time': departing_time.strip(),
        'duration': duration.strip(),
        'reaching_time': reaching_time.strip(),
        'star_rating': star_rating.strip(),
        'price': price.strip(),
        'seats_available': seats_available.strip()
    })
# Convert data to Pandas dataframe
df = pd.DataFrame(data)

# Insert data into MySQL database
query = "INSERT INTO bus_routes (route_name, route_link, bus_name, bus_type, departing_time, duration, reaching_time, star_rating, price, seats_available) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
cursor.executemany(query, data)
cursor.executemany(query, [
    (
        row['route_name'],
        row['route_link'],
        row['bus_name'],
        row['bus_type'],
        row['departing_time'],
        row['duration'],
        row['reaching_time'],
        row['star_rating'],
        row['price'],
        row['seats_available']
    ) for row in data
])

# Commit changes
cnx.commit()

# Streamlit application
st.title('Redbus Data Scraping and Filtering')

# Filter options
bus_type_options = ['Sleeper', 'Seater', 'AC', 'Non-AC', 'Clear']
bus_type = st.sidebar.selectbox('Bus Type', bus_type_options)
route_name = st.sidebar.text_input('Route Name')
price_range
