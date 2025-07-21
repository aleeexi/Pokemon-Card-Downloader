from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import requests
import time
import urllib

options = Options()
options.headless = True # Set to True to enable headless mode (no window pop-up)
options.add_argument("--headless")

driver = webdriver.Chrome(options = options)
# Navigate webdriver to database of Rare Pokemon cards
driver.get("https://pkmncards.com/?s=type%3Apokemon+rarity%3Arare&sort=abc&ord=auto&display=full")

# Navigate page of Pokemon cards and download all card images with name-energy-id.jpg file name formatting
def navigate_page():
    # Load images on page
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.entry-content")))

    # Find card content elements
    cards = driver.find_elements(By.CSS_SELECTOR, "div.entry-content")

    for card in cards:
        # Get name of Pokemon in card
        name_element = card.find_element(By.CSS_SELECTOR, "span.pokemon")
        name = name_element.text

        # Get energy type of Pokemon in card
        energy_element = card.find_element(By.CSS_SELECTOR, "abbr.ptcg-font.ptcg-symbol-name")
        energy = energy_element.get_attribute("title")

        # Get id number of Pokemon card
        id_parent = card.find_element(By.CSS_SELECTOR, "span.number")
        id_element = id_parent.find_element(By.TAG_NAME, "a")
        id = id_element.text

        # Download Pokemon card image
        # Image download code from https://plainenglish.io/blog/web-scraping-images-with-python-and-selenium-792e452abd70
        image = card.find_element(By.CSS_SELECTOR, "img.card-image")
        url = image.get_attribute("src")
        urllib.request.urlretrieve(str(url), "images/rare/" + name + "-" + energy + "-" + id + ".jpg")
    
    # Navigate to next page using right arrow key shortcut
    actions = ActionChains(driver)
    actions.send_keys(Keys.RIGHT)
    actions.perform()

# Navigate all search result pages of Rare Pokemon cards
while True:
    navigate_page()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.after-content")))
    try:
        next_link = driver.find_element(By.CSS_SELECTOR, "li.next-link")
    except:
        break
driver.quit()