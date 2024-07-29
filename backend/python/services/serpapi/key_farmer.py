from random import choice

from pynator import EmailNator

PROXY = ""
CHROME_BASE_DIR = "/Users/simonferns/Library/Application Support/Google/Chrome"
CHROME_PROFILE_NAME = "Profile 1"

while True:
    client = EmailNator()
    email = ""
    while True:
        email = client.generate_email()
        if "googlemail" in email:
            break

    printed_mails = []

    import time

    from helium import *
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium_authenticated_proxy import SeleniumAuthenticatedProxy
    from webdriver_manager.chrome import ChromeDriverManager

    # Initialize Chrome options
    chrome_options = webdriver.ChromeOptions()
    user_data_dir = CHROME_BASE_DIR
    profile_directory = CHROME_PROFILE_NAME

    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"profile-directory={profile_directory}")

    # provide the profile name with which we want to open browser
    # chrome_options.add_argument(r"--profile-directory=Profile 1")

    proxy_helper = SeleniumAuthenticatedProxy(proxy_url=PROXY)

    proxy_helper.enrich_chrome_options(chrome_options)

    start_chrome(options=chrome_options)

    go_to("https://serper.dev/signup")

    time.sleep(1)

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

    write(name, S("#firstName1"))

    write(surname, S("#lastName1"))

    write(email, S("#email1"))

    write(email, S("input[name='password']"))

    click(Button("Create account"))

    count = 30
    has_url = False
    while count > 0:
        time.sleep(1)
        count -= 1
        messages = client.get_messages(email)

        for message in messages:
            content = client.get_message(email, message.message_id)
            if "serper.dev" in content:
                if content.splitlines()[6]:
                    go_to(content.splitlines()[6])
                    time.sleep(4)
                    has_url = True

        if has_url:
            break

    if not has_url:
        kill_browser()
        continue

    go_to("https://serper.dev/api-key")

    time.sleep(3)

    input_field = S("input[name='api-key']")
    value = input_field.web_element.get_attribute("value")

    print(value)
    with open("keys.txt", "a+") as f:
        f.write(value + "\n")

    kill_browser()
