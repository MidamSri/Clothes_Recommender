from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
import os
import predicting

def main():
    # === Ask for image paths ===
    outfit = predicting.main()
    img1 = r'C:\Users\Lenovo\OneDrive\Desktop\Midam_codes\DIS_Modara\woman.png'
    img2 = f"C:\\Users\\Lenovo\\OneDrive\\Desktop\\Midam_codes\\DIS_Modara\\assets\\tops\\{outfit[0]}"
    img3 = f"C:\\Users\\Lenovo\\OneDrive\\Desktop\\Midam_codes\\DIS_Modara\\assets\\tops\\{outfit[1]}"
    # === Chrome setup ===
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)

    # === Load the site ===
    driver.get("https://kwai-kolors-kolors-virtual-try-on.hf.space")
    time.sleep(15)  # let the page load

    # === Find both file inputs ===
    file_inputs = driver.find_elements(By.CSS_SELECTOR, "input[data-testid='file-upload']")
    if len(file_inputs) < 2:
        print("❌ Could not find two file upload inputs.")
        driver.quit()
        exit()

    # === Upload the images ===
    file_inputs[0].send_keys(os.path.abspath(img1))
    file_inputs[1].send_keys(os.path.abspath(img2))
    print("✅ Images uploaded.")
    time.sleep(5)

    # === Click the 'Run' button ===
    try:
        run_button = driver.find_element(By.ID, "button")
        run_button.click()
        print("🚀 Run button clicked.")
    except Exception as e:
        print("❌ Could not click run button:", e)
        driver.quit()
        exit()

    # === Wait for the output image ===
    print("⏳ Waiting for output image...")
    image_url = None
    for _ in range(60):  # up to 90 seconds
        try:
            images = driver.find_elements(By.CSS_SELECTOR, ".image-frame img")
            if len(images) >= 3:  # output appears after 2 input previews
                src = images[-1].get_attribute("src")
                if src and src.startswith("http"):
                    image_url = src
                    break
        except:
            pass
        time.sleep(1)

    if not image_url:
        print("❌ Output image not found.")
        driver.quit()
        exit()

    # === Download the image ===
    try:
        r = requests.get(image_url)
        with open("result_image.webp", "wb") as f:
            f.write(r.content)
        print("✅ Saved image to result_image.webp")
    except Exception as e:
        print("❌ Failed to download image:", e)

    driver.quit()
