from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import pytesseract
import ssl
from PIL import Image
import time
import io

def extract_webpage_text(url, debug=False):
    # Bypass SSL certificate verification (not secure)
    ssl._create_default_https_context = ssl._create_unverified_context

    # Set Chrome options for mobile emulation
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Set window size for mobile (optional but useful)
    chrome_options.add_argument('--window-size=375,812')

    # Add a mobile user-agent to force mobile view
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    )

    try:
        print(f"Attempting to load: {url}")
        driver = uc.Chrome(options=chrome_options)
        driver.get(url)

        # Wait for page load
        print("Waiting for page to load...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        print("Waiting additional time for content...")
        time.sleep(10)  # Increased wait time

        # Get page title for verification
        page_title = driver.title
        print(f"Page title: {page_title}")

        # Scroll and capture the full page screenshot
        total_height = driver.execute_script("return document.body.scrollHeight")
        viewport_height = driver.execute_script("return window.innerHeight")
        num_scrolls = total_height // viewport_height

        # Container to merge images
        screenshots = []

        for scroll in range(num_scrolls + 1):
            print(f"Scrolling: {scroll + 1}/{num_scrolls + 1}")
            driver.execute_script(f"window.scrollTo(0, {scroll * viewport_height});")
            time.sleep(2)  # Allow time for the page to load after each scroll

            # Capture screenshot
            screenshot = driver.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot))
            screenshots.append(image)

        # Stitch images together vertically
        total_image_height = sum(img.size[1] for img in screenshots)
        stitched_image = Image.new('RGB', (screenshots[0].size[0], total_image_height))

        y_offset = 0
        for img in screenshots:
            stitched_image.paste(img, (0, y_offset))
            y_offset += img.size[1]

        if debug:
            stitched_image.save("full_page_screenshot.png")
            print("Saved full-page screenshot to full_page_screenshot.png")

        # Perform OCR
        print("Performing OCR...")
        extracted_text = pytesseract.image_to_string(
            stitched_image,
            config='--psm 1 --oem 3 -l eng'  # Explicit English language setting
        )

        driver.quit()

        if debug:
            print("\nExtracted text:")
            print("-" * 50)
            print(extracted_text)
            print("-" * 50)

        return extracted_text.strip()

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        if 'driver' in locals():
            driver.quit()
        raise

# Test with a simple, public website
if __name__ == "__main__":
    try:
        # Test with a reliable public website
        test_url = "https://news.google.com/home"  # or try "https://google.com"
        text = extract_webpage_text(test_url, debug=True)

        # gives to gemini, gets a summary back


        # Save extracted text to a text file
        with open("extracted_text.txt", "w") as file:
            file.write(text)
        print("Extracted text saved to extracted_text.txt")
        print("\nFinal extracted text:")
        print(text)
    except Exception as e:
        print(f"Failed to extract text: {str(e)}")
