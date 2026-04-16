from playwright.sync_api import sync_playwright

def test_google_homepage():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,slow_mo=2000)  # set True if you don't want UI
        page = browser.new_page()

        # Step 1: Open a website
        page.goto("https://www.google.com")

        # Step 2: Validate page title
        assert "Google" in page.title()

        # Step 3: Check if search box is visible
        search_box = page.locator("textarea[name='q']")
        assert search_box.is_visible()

        print("✅ Google homepage test passed")

        browser.close()

if __name__ == "__main__":
    test_google_homepage()