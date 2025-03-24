from selenium import webdriver
import pickle
import time

# Set up Chrome WebDriver
driver = webdriver.Chrome(executable_path='C:/Program Files/Google/chromedriver-win64/chromedriver.exe')

# Manually log in to Google Voice
driver.get('https://voice.google.com/')
time.sleep(60)  # Allow time for manual login

# Save cookies to a file
pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

# Close the browser after saving cookies
driver.quit()
