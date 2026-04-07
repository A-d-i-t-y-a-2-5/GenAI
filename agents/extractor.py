import json
import os
import time

from playwright.sync_api import sync_playwright
from langchain_core.documents import Document


def get_linkedin_page(
    url: str, cookies: list[dict], password: str, scroll_duration: int = 30
) -> Document:

    with sync_playwright() as p:

        browser = p.firefox.launch(
            headless=False,
        )
        context = browser.new_context()

        # Load playwright cookies if they exist (after initial login)
        playwright_cookie_path = os.path.join(os.curdir, "playwright_cookies.json")
        if os.path.exists(playwright_cookie_path):
            with open(playwright_cookie_path, "r") as f:
                playwright_cookies = json.load(f)
                context.add_cookies(playwright_cookies)
                print(f"Loaded cookies from {playwright_cookie_path}")

        # Add browser cookies to context (this will override any saved cookies with same name)
        context.add_cookies(cookies)

        page = context.new_page()
        page.goto("https://www.linkedin.com/login")

        if "feed" in page.url:
            print("Already logged in via cookies.")
            page.goto(url)
        else:
            page.fill("input[name='session_password']", password, timeout=5000)
            page.click("button[type='submit']")

            if "checkpoint" in page.url:
                print(
                    "Checkpoint detected. Please complete the verification in the opened browser window."
                )

                page.wait_for_function(
                    """() => !['checkpoint','challenge','verify','captcha','security-verification']
                .some(s => window.location.href.includes(s))""",
                    timeout=60 * 1000,
                )

            playwright_cookies = page.context.cookies()
            with open(os.path.join(os.curdir, "playwright_cookies.json"), "w") as f:
                json.dump(playwright_cookies, f)
            print(
                f"Cookies saved to {os.path.join(os.curdir, 'playwright_cookies.json')}"
            )
            # wait for login to complete - adjust as needed

            page.goto(url)

        start = time.monotonic()
        while (time.monotonic() - start) < scroll_duration:
            page.click("body")
            page.keyboard.press("End")
            page.wait_for_timeout(2500)  # wait for new content to load

        content = page.inner_text("body")
        browser.close()

    return Document(page_content=content, metadata={"source": url})
