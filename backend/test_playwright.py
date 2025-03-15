from playwright.sync_api import sync_playwright


def test_playwright():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://example.com")
        title = page.title()
        print("Page title:", title)
        browser.close()


if __name__ == "__main__":
    test_playwright()
