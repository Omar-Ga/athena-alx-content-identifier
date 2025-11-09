import asyncio
import os
from datetime import datetime
from playwright.async_api import async_playwright
from modules.login_module import login_to_admissions, login_to_ehub
from config import ALX_EMAIL, ALX_PASSWORD, MAX_PAGES
from modules.navigator_module import detect_content_type
from modules.content_processor_module import process_content
from modules.mcq_handler_module import handle_mcq_quiz
from modules.completion_handler_module import handle_completion, click_next_lesson

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
                await page.get_by_role('link', name=course_link_text).click(timeout=7000)

            athena_page = await new_page_info.value
            print("✓ New course tab detected and captured.")
            
            await athena_page.wait_for_load_state("domcontentloaded")
            await athena_page.bring_to_front()
            print(f"✓ Switched to new tab. Current URL: {athena_page.url}")
            page = athena_page

        except Exception as e:
            print(f"✗ Could not automatically navigate by clicking the link: {e}")
            print("   The script will continue on the current page. Please provide the lesson URL directly.")

        # Get the first lesson URL from the user
        start_url = input("\nEnter the first lesson URL to begin automation (or 'q' to quit): ")
        if start_url.lower() == 'q':
            return

        print(f"Navigating to starting URL: {start_url}...")
        await page.goto(start_url, wait_until="domcontentloaded")
        print(f"✓ Successfully navigated to {page.url}")

        # Main automation loop
        extracted_content_for_mcq = ""
        for i in range(MAX_PAGES):
            print(f"\n" + "="*60)
            print(f"Processing page {i+1}/{MAX_PAGES}...")
            print(f"Current URL: {page.url}")
            print("="*60)

            try:
                # === AUTOMATION STARTS HERE ===
                content_type = await detect_content_type(page)
                
                if content_type == "mcq":
                    await handle_mcq_quiz(page, extracted_content_for_mcq)
                else:
                    extracted_content, content_type_processed = await process_content(page, content_type)
                    if extracted_content:
                        extracted_content_for_mcq = extracted_content
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

                    # Handle lesson completion for non-mcq pages
                    await handle_completion(page)

                # Navigate to the next lesson
                if not await click_next_lesson(page):
                    break # Exit loop if no "Next" button is found

            except Exception as e:
                print(f"An error occurred on page {page.url}: {e}")
                print("Attempting to continue to the next lesson...")
                if not await click_next_lesson(page):
                    break

        print("\n" + "="*60)
        print("Automation loop finished.")
        print("="*60)
        
        print("\nClosing browser...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nScript terminated by user.")
