from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from openpyxl import Workbook
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium WebDriver
driver = webdriver.Chrome()

# Open the website
# prod url
url = "https://frontend-harmonia-vs-b-plus.vercel.app/"
# dev url
# url = "http://localhost:5173/"  
driver.get(url)

# Create Excel workbook and sheet
workbook = Workbook()
sheet = workbook.active
sheet.append(['key' ,'time_harmonia', 'time_bplus'])  # Header row

# Function to perform the actions on the website and record times
def record_times(key ):
    # access the dropdown to switch to 'search' operation
    dropdown = driver.find_element(By.ID , "action_selector") 
    dropdown.click();
    driver.find_element(By.ID ,"search_option").click();

    # locate the 'key' input field
    key_field = driver.find_element(By.ID, 'key_input')  

    # put the key value
    key_field.clear()
    key_field.send_keys(key)

    # Submit the form
    submit_button = driver.find_element(By.ID , 'submit_button')  # Adjust the locator accordingly
    submit_button.click()

    # wait till the request is resolved 
    while(submit_button.text != "SUBMIT"):
        status = "waiting" # doing nothing
    
    # Get and record the times
    time1 = driver.find_element(By.ID, 'time_harmonia').text  # Adjust the locator accordingly
    time2 = driver.find_element(By.ID, 'time_bplus').text  # Adjust the locator accordingly

    # store data to excel sheet
    sheet.append([key ,time1, time2])

for key in range(101 , 201):
    record_times(key);


# Save the Excel file
workbook.save('harmonia_vs_bplus_search.xlsx')

# Close the browsers
driver.quit()
