import time
from multiprocessing import Pool
from random import choice

import requests
from pynator import EmailNator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium_authenticated_proxy import SeleniumAuthenticatedProxy

PROXY = "http://gqnuguju-ZA-rotate:670myl2p6d9f@p.webshare.io:80/"
PROXY_ENABLED = True
EXTENSIONS = [
    "/Users/simonferns/Downloads/CRX Extractor Extension (1).crx",
    "/Users/simonferns/Downloads/CRX Extractor Extension (1).crx",
    "/Users/simonferns/Downloads/CRX Extractor Extension (1).crx",
]
HEADLESS = False
TOTAL_RETRIES = 30
NUM_PROFILES = len(EXTENSIONS)


def get_chrome_options(extension_path):
    chrome_options = Options()

    # Add the extension
    chrome_options.add_extension(extension_path)

    if HEADLESS:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--allow-running-insecure-content")

    if PROXY_ENABLED:
        proxy_helper = SeleniumAuthenticatedProxy(proxy_url=PROXY)
        proxy_helper.enrich_chrome_options(chrome_options)

    return chrome_options


def run_profile(extension_path):
    while True:
        try:
            print(f"Running Extension: {extension_path}")
            client = EmailNator()
            print("Setting Up Emailnator")
            email = ""
            while True:
                email = client.generate_email()
                print("Email Generation: ", email)
                if "googlemail" in email:
                    break

            # Initialize WebDriver for this extension
            chrome_options = get_chrome_options(extension_path)
            driver = webdriver.Chrome(service=Service(), options=chrome_options)
            actions = ActionChains(driver)

            driver.get("https://serper.dev/signup")
            time.sleep(5)

            names = [
                "Bill",
                "Serenity",
                "Juliet",
                "Karina",
                "Aila",
                "Alaia",
                "Dariel",
                "Blaine",
            ]
            surnames = [
                "Gould",
                "Gonzales",
                "Davenport",
                "Dawson",
                "Yang",
                "Bass",
                "Hull",
                "Bailey",
            ]

            name = choice(names)
            surname = choice(surnames)

            # Fill out the signup form
            driver.find_element(By.CSS_SELECTOR, "#firstName1").send_keys(name)
            driver.find_element(By.CSS_SELECTOR, "#lastName1").send_keys(surname)
            driver.find_element(By.CSS_SELECTOR, "#email1").send_keys(email)
            driver.find_element(By.CSS_SELECTOR, "input[name='password']").send_keys(
                email
            )
            driver.find_element(By.XPATH, "//button[text()='Create account']").click()

            count = TOTAL_RETRIES
            has_url = False
            while count > 0:
                time.sleep(1)
                count -= 1
                messages = client.get_messages(email)

                for message in messages:
                    content = client.get_message(email, message.message_id)
                    if "serper.dev" in content:
                        if content.splitlines()[6]:
                            driver.get(content.splitlines()[6])
                            time.sleep(4)
                            has_url = True

                if has_url:
                    break

            if not has_url:
                driver.quit()
                return

            driver.get("https://serper.dev/api-key")
            time.sleep(3)

            input_field = driver.find_element(By.CSS_SELECTOR, "input[name='api-key']")
            value = input_field.get_attribute("value")

            print(value)
            with open("keys.txt", "a+") as f:
                f.write(value + "\n")

            json_data = {"apiKey": value}
            response = requests.post(
                "https://serpapi-shy-breeze-5598.fly.dev/add-api-key",
                json=json_data,
            )
            print(response.json())

            driver.quit()
        except Exception as e:
            print(f"Error with Extension {extension_path}: {e}")
            try:
                driver.quit()
            except:
                pass


if __name__ == "__main__":
    while True:
        with Pool(NUM_PROFILES) as p:
            p.map(run_profile, EXTENSIONS)
