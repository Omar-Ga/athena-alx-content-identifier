import asyncio
import os
from datetime import datetime
from playwright.async_api import async_playwright
from modules.login_module import login_to_admissions, login_to_ehub
from config import ALX_EMAIL, ALX_PASSWORD
from modules.navigator_module import detect_content_type, find_set_as_complete_button, find_next_lesson_button, find_confirmation_yes_button
from modules.content_processor_module import process_content

async def main():
    async with async_playwright() as p:
        # Launch browser with persistent profile
        user_data_dir = "C:\\temp\\chrome_profile"
        
        print("Launching browser...")
        browser_context = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            args=['--start-maximized'],
            viewport={'width': 1920, 'height': 1080},
            channel="chrome"
        )

        page = browser_context.pages[0] if browser_context.pages else await browser_context.new_page()

        # Credentials
        email = ALX_EMAIL
        password = ALX_PASSWORD

        # Login to Admissions portal
        print("="*60)
        print("STEP 1: Logging into Admissions Portal")
        print("="*60)
        await login_to_admissions(page, email, password)

        # Login to eHub
        print("\n" + "="*60)
        print("STEP 2: Logging into eHub")
        print("="*60)
        await login_to_ehub(page, email, password)

        print("\n" + "="*60)
        print("Both logins complete!")
        print("STEP 3: Navigating to Athena Course")
        print("="*60)

        # Using the selector name provided in config/selectors.md
        course_link_text = 'Data Analytics'

        try:
            # Start waiting for the new page to open *before* clicking.
            async with browser_context.expect_page() as new_page_info:
                print(f"Attempting to click the '{course_link_text}' course link...")
                # Using get_by_role is a robust way to find links by their accessible name.
                await page.get_by_role('link', name=course_link_text).click(timeout=7000)

            athena_page = await new_page_info.value
            print("✓ New course tab detected and captured.")
            
            # Wait for the new page to load and switch focus to it.
            await athena_page.wait_for_load_state("domcontentloaded")
            await athena_page.bring_to_front()
            print(f"✓ Switched to new tab. Current URL: {athena_page.url}")

            # Overwrite the 'page' variable to ensure all subsequent commands use the new tab.
            page = athena_page

        except Exception as e:
            print(f"✗ Could not automatically navigate by clicking the link: {e}")
            print("   The script will continue on the current page. Please provide the lesson URL directly.")

        # Prompt for URL and start the automation loop
        while True:
            try:
                target_url = input("\nEnter the lesson URL to begin automation (or 'q' to quit): ")
                if target_url.lower() == 'q':
                    break
                if target_url:
                    print(f"Navigating to {target_url}...")
                    await page.goto(target_url, wait_until="domcontentloaded")
                    print(f"✓ Successfully navigated to {page.url}")
                    
                    # === AUTOMATION STARTS HERE ===
                    content_type = await detect_content_type(page)
                    extracted_content, content_type_processed = await process_content(page, content_type)

                    if extracted_content:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        if content_type_processed == 'slides':
                            filename = f"slides/extracted_slides_{timestamp}.txt"
                        elif content_type_processed == 'video':
                            filename = f"transcripts/extracted_transcript_{timestamp}.txt"
                        else:
                            filename = None
                        
                        if filename:
                            os.makedirs(os.path.dirname(filename), exist_ok=True)
                            with open(filename, "w", encoding="utf-8") as f:
                                f.write(extracted_content)
                            print(f"✓ Extracted content saved to {filename}")


                    # Find key buttons
                    print("\n🔍 Finding key buttons...")
                    await find_set_as_complete_button(page)
                    await find_next_lesson_button(page)
                    await find_confirmation_yes_button(page)


            except Exception as e:
                print(f"An error occurred: {e}")
        
        print("\nClosing browser...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nScript terminated by user.")