from playwright.sync_api import sync_playwright, TimeoutError

URL = "https://www.1stopbedrooms.com/customer/account/login"


def close_popups(page):
    """
    Close any popup/overlay if it appears.
    Safe to call anytime.
    """
    popup_selectors = [
        "button:has-text('No Thanks')",
        "button:has-text('No, thanks')",
        "button:has-text('Close')",
        "button[aria-label='Close']",
        "text=×",
        ".modal-close",
        ".close"
    ]

    for selector in popup_selectors:
        try:
            btn = page.locator(selector).first
            if btn.is_visible():
                btn.click(force=True)
                page.wait_for_timeout(800)
                print("⚠️ Popup closed")
        except:
            pass


def safe_click(page, locator, description):
    """
    Ensures element is visible, clickable, and not blocked.
    """
    close_popups(page)
    locator.wait_for(state="visible", timeout=15000)
    locator.scroll_into_view_if_needed()
    locator.click(force=True)
    print(f"✅ {description}")


def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=700   # 👈 visible & human-like
        )

        context = browser.new_context()
        page = context.new_page()

        # -------------------------------------------------
        # STEP 1: Open page
        # -------------------------------------------------
        page.goto(URL, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)
        close_popups(page)

        # -------------------------------------------------
        # STEP 2: Wait for login form (CRITICAL FIX)
        # -------------------------------------------------
        email = page.locator("input[type='email']")
        password = page.locator("input[type='password']")
        sign_in = page.locator("button:has-text('Sign In')")

        email.wait_for(state="visible", timeout=20000)
        password.wait_for(state="visible", timeout=20000)
        sign_in.wait_for(state="visible", timeout=20000)

        print("✅ Login form detected")

        # -------------------------------------------------
        # TEST 1: Empty submit
        # -------------------------------------------------
        safe_click(page, sign_in, "Clicked Sign In (empty form)")
        page.wait_for_timeout(1500)

        # -------------------------------------------------
        # TEST 2: Invalid email format
        # -------------------------------------------------
        close_popups(page)
        email.fill("invalidemail")
        password.fill("test123")
        safe_click(page, sign_in, "Submitted invalid email")
        page.wait_for_timeout(1500)

        # -------------------------------------------------
        # TEST 3: Wrong credentials
        # -------------------------------------------------
        close_popups(page)
        email.fill("wronguser@test.com")
        password.fill("wrongpassword")
        safe_click(page, sign_in, "Submitted wrong credentials")
        page.wait_for_timeout(2000)

        # -------------------------------------------------
        # TEST 4: Password masking
        # -------------------------------------------------
        assert password.get_attribute("type") == "password"
        print("✅ Password field is masked")

        # -------------------------------------------------
        # TEST 5: Forgot Password
        # -------------------------------------------------
        forgot = page.locator("text=Forgot Your Password?")
        safe_click(page, forgot, "Opened Forgot Password page")

        page.wait_for_load_state("networkidle")
        print("✅ Forgot Password navigation successful")

        page.wait_for_timeout(5000)
        browser.close()


if __name__ == "__main__":
    run_test()