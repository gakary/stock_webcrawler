import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Fetch webpage content
url = 'https://stockanalysis.com/markets/gainers/'
response = requests.get(url)

# Parse the HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table with stock gainers, assuming it's the first table in the page
table = soup.find('table')

# Find all rows, skip the header row with [1:]
rows = table.find_all('tr')[1:]

# Extract company names from each row
company_names = [row.find_all('td')[1].text for row in rows]

# Get today's date
today = datetime.now().strftime('%Y-%m-%d')

# Create DataFrame with new data
new_data_df = pd.DataFrame({
    'Company Name': company_names,
    'Date': today
})

# Define the filename
filename = 'stock_gainers.xlsx'

# Check if the file exists
try:
    # If the file exists, read the existing data
    existing_data_df = pd.read_excel(filename)

    # Add a blank row if last date in existing data is not today
    if existing_data_df['Date'].iloc[-1] != today:
        blank_row = pd.DataFrame([['', '']], columns=existing_data_df.columns)
        existing_data_df = existing_data_df.append(blank_row, ignore_index=True)

    # Append new data
    updated_data_df = pd.concat([existing_data_df, new_data_df], ignore_index=True)

except FileNotFoundError:
    # If the file does not exist, use new data
    updated_data_df = new_data_df

# Export to Excel, without the index
updated_data_df.to_excel(filename, index=False)
