import time
from random import choice

import bs4
import requests
from helium import (Button, S, click, get_driver, go_to, kill_browser,
                    set_driver, start_chrome, write)
from pynator import EmailNator
from selenium import webdriver
from selenium_authenticated_proxy import SeleniumAuthenticatedProxy

PROXY = "http://gqnuguju-ZA-rotate:670myl2p6d9f@p.webshare.io:80/"
PROXY_ENABLED = True
CHROME_BASE_DIR = "/Users/simonferns/Library/Application Support/Google/Chrome"
CHROME_PROFILE_NAME = "Profile 1"
CHROME_PROFILE_ENABLED = True
HEADLESS = False
TOTAL_RETRIES = 30

COUNT_TRY = 130
while COUNT_TRY > 0:
    try:
        print(f"Iterations Left {COUNT_TRY}")
        COUNT_TRY -= 1

        print("Setting Up Emailnator")
        client = EmailNator()
        print("Done Setting Up Emailnator")

        email = ""
        while True:
            email = client.generate_email()
            print("Email Generation: ", email)
            if "googlemail" in email:
                break

        printed_mails = []
        # Initialize Chrome options
        chrome_options = webdriver.ChromeOptions()
        if CHROME_PROFILE_ENABLED:
            user_data_dir = CHROME_BASE_DIR
            profile_directory = CHROME_PROFILE_NAME

            chrome_options.add_argument(f"user-data-dir={user_data_dir}")
            chrome_options.add_argument(f"profile-directory={profile_directory}")

        if HEADLESS:
            chrome_options.add_argument("--headless=true")
            user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument(f"user-agent={user_agent}")

        if PROXY_ENABLED:
            proxy_helper = SeleniumAuthenticatedProxy(proxy_url=PROXY)

            proxy_helper.enrich_chrome_options(chrome_options)

        start_chrome(options=chrome_options)

        go_to("https://scrapeops.io/app/register/main")

        time.sleep(90)

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

        write(name, S("#mat-input-0"))

        write(surname, S("#mat-input-1"))

        write(email, S("#mat-input-2"))

        write("!2#" + email, S("#mat-input-3"))
        write("!2#" + email, S("#mat-input-4"))

        click(Button("Create Free Account"))

        count = TOTAL_RETRIES
        has_url = False
        while count > 0:
            time.sleep(1)
            count -= 1
            messages = client.get_messages(email)

            for message in messages:
                if has_url:
                    break

                content = client.get_message(email, message.message_id)
                soup = bs4.BeautifulSoup(content)
                urls = soup.find_all("a")
                for url in urls:
                    print(url)
                    if "email-confirmation" in url.get_text():
                        go_to(url.get_text())
                        time.sleep(5)
                        has_url = True
                        break

            if has_url:
                break

        if not has_url:
            kill_browser()
            continue

        time.sleep(5)

        go_to("https://scrapeops.io/app/settings")

        time.sleep(5)

        value = S("pre").web_element.get_attribute("innerText")

        print(value)
        with open("scrapeops_keys.txt", "a+") as f:
            f.write(value + "\n")

        json_data = {"apiKey": value}

        response = requests.post(
            "https://scrapeopsproxyapi-shy-breeze-5598.fly.dev/add-api-key",
            json=json_data,
        )
        print(response.json())

        kill_browser()
    except Exception as e:
        print(e)
        print("ERROR")
        kill_browser()

    time.sleep(30)
