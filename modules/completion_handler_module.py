# modules/completion_handler_module.py
from playwright.async_api import Page

async def handle_completion(page: Page):
    """
    Handles the process of marking a lesson as complete, including the
    confirmation modal.
    """
    print("\n⚙️ Handling lesson completion...")
    
    # Click the "Set as Complete" button
    set_as_complete_button = page.get_by_role('link', name='Set as Complete')
    if await set_as_complete_button.is_visible():
        print("   ► Clicking 'Set as Complete' button...")
        await set_as_complete_button.click()
    else:
        # Sometimes the button is a regular button, not a link
        set_as_complete_button = page.get_by_role('button', name='Set as Complete')
        if await set_as_complete_button.is_visible():
            print("   ► Clicking 'Set as Complete' button (as button)...")
            await set_as_complete_button.click()
        else:
            print("   ✗ 'Set as Complete' button not found.")
            return

    # Handle the confirmation modal
    yes_button = page.locator('#lightbox-body').get_by_text('Yes')
    try:
        await yes_button.wait_for(state='visible', timeout=5000)
        print("   ► Clicking 'Yes' in confirmation modal...")
        await yes_button.click()
        print("   ✓ Lesson marked as complete.")
    except Exception:
        print("   ✓ No confirmation modal found, or it timed out. Assuming completion was successful.")

async def click_next_lesson(page: Page):
    """
    Clicks the 'Next ⇒' button to proceed to the next lesson.
    """
    next_lesson_button = page.get_by_role('link', name='Next ⇒')
    if await next_lesson_button.is_visible():
        print("\n   ► Clicking 'Next ⇒' to proceed to the next lesson...")
        await next_lesson_button.click()
        await page.wait_for_load_state("domcontentloaded")
        print(f"   ✓ Navigated to next lesson. Current URL: {page.url}")
        return True
    else:
        print("\n   ✗ 'Next ⇒' button not found. End of lessons or navigation issue.")
        return False
