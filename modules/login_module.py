import asyncio

async def login_to_admissions(page, email, password):
    """Login to admissions.alxafrica.com"""
    login_url = "https://admissions.alxafrica.com/users/sign_in"
    
    print(f"Navigating to {login_url}...")
    await page.goto(login_url, wait_until="domcontentloaded")
    await asyncio.sleep(1)

    if "sign_in" in page.url:
        print("Admissions login page detected. Logging in...")
        
        await page.fill("#user_email", email)
        await page.fill("#user_password", password)
        await page.click("input[name='commit']")

        try:
            await page.wait_for_url(lambda url: "sign_in" not in url, timeout=30000)
            print(f"✓ Admissions login successful! Current URL: {page.url}")
            return True
        except Exception as e:
            print(f"✗ Admissions login failed: {e}")
            await page.screenshot(path="admissions_login_error.png")
            return False
    else:
        print(f"✓ Already logged into Admissions! Current URL: {page.url}")
        return True


async def login_to_ehub(page, email, password):
    """Login to ehub.alxafrica.com"""
    ehub_url = "https://ehub.alxafrica.com/login"
    
    print(f"\nNavigating to eHub: {ehub_url}...")
    await page.goto(ehub_url, wait_until="domcontentloaded")
    await asyncio.sleep(2)  # Wait for page to fully load

    # Check if we're on the login page
    if "login" in page.url:
        print("eHub login page detected. Logging in...")
        
        # Selectors for eHub login (based on the screenshot)
        email_input = "input[placeholder='Enter your email']"
        password_input = "input[placeholder='Enter your password']"
        signin_button = "button:has-text('Sign in')"
        
        try:
            await page.fill(email_input, email)
            await page.fill(password_input, password)
            await page.click(signin_button)

            # Wait for navigation away from login page
            await page.wait_for_url(lambda url: "login" not in url, timeout=30000)
            print(f"✓ eHub login successful! Current URL: {page.url}")
            return True
        except Exception as e:
            print(f"✗ eHub login failed: {e}")
            await page.screenshot(path="ehub_login_error.png")
            return False
    else:
        print(f"✓ Already logged into eHub! Current URL: {page.url}")
        return True
