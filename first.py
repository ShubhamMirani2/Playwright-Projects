from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:

    browser = playwright.chromium.launch(headless=False,slow_mo=2000) #lanuch Browser
    page = browser.new_page() #Create new page 
    page.goto("https://playwright.dev/python/")

    docs_button = page.get_by_role('button', name="log Out")
    docs_button.click()

    

    browser.close()

