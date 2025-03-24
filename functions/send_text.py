from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Disable GPU to prevent GPU warnings
options = Options()
options.add_argument('--disable-gpu')  # Disable GPU acceleration

# Set up Chrome WebDriver using Service class
service = Service('C:/Program Files/Google/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

# Go to Google Voice login page
driver.get('https://voice.google.com/')

# Give time to log in manually, handle 2FA or Captcha if needed
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/md-toolbar/div/md-nav-bar/div[1]/md-nav-item[2]/a')))

# Click on the "Messages" tab
messages_tab = driver.find_element(By.XPATH, '//*[@id="app"]/div/md-toolbar/div/md-nav-bar/div[1]/md-nav-item[2]/a')
messages_tab.click()

# Wait for the new message button to appear
new_message_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[1]/md-fab/md-button'))
)
new_message_button.click()

# Wait for the phone number input field to appear
phone_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="input_0"]'))
)
phone_input.send_keys('1234567890')  # Replace with the recipient's phone number
phone_input.send_keys(Keys.RETURN)

# Wait for the message input field to appear
message_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="input_1"]'))
)
message_input.send_keys('Hello from Selenium!')  # Replace with your message

# Wait for the send button and click it
send_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/md-content/md-card/div/md-input-container[2]/md-button'))
)
send_button.click()

# Wait for a bit to ensure the message is sent
time.sleep(5)

# Close the browser
driver.quit()
