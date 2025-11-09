import asyncio

async def detect_content_type(page):
    """Detects the type of content on the page (video, slides, or pdf)."""
    print("\n🔍 Detecting content type...")
    
    # Using selectors from config/selectors.md
    # Use asyncio.gather to check for all selectors concurrently for efficiency.
    
    is_video_list = await asyncio.gather(
        page.locator('iframe[title*="player.vimeo.com"]').count(),
        page.locator('h3:has-text("[Walk-through]")').count()
    )
    if any(count > 0 for count in is_video_list):
        print("   ↳ Content type: Video")
        return "video"

    is_slides_list = await asyncio.gather(
        page.locator('iframe[src*="docs.google.com/presentation"]').count(),
        page.locator('h3:has-text("[Slides]")').count()
    )
    if any(count > 0 for count in is_slides_list):
        print("   ↳ Content type: Slides")
        return "slides"

    is_pdf_list = await asyncio.gather(
        page.locator('h2:has-text("[PDF]")').count(),
        page.locator('embed[type*="pdf"]').count()
    )
    if any(count > 0 for count in is_pdf_list):
        print("   ↳ Content type: PDF")
        return "pdf"

    # Detect MCQ content
    is_mcq = await page.locator('.mcq-question-text').count()
    if is_mcq > 0:
        print("   ↳ Content type: MCQ")
        return "mcq"

    print("   ↳ Content type: Unknown")
    return "unknown"

async def find_set_as_complete_button(page):
    """Finds the 'Set as Complete' button on the page."""
    button = page.get_by_role('link', name='Set as Complete')
    if await button.is_visible():
        print("✓ 'Set as Complete' button found.")
    else:
        print("✗ 'Set as Complete' button not found.")
    return button

async def find_next_lesson_button(page):
    """Finds the 'Next ⇒' button on the page."""
    button = page.get_by_role('link', name='Next ⇒')
    if await button.is_visible():
        print("✓ 'Next ⇒' button found.")
    else:
        print("✗ 'Next ⇒' button not found.")
    return button

async def find_confirmation_yes_button(page):
    """Finds the 'Yes' button in the confirmation modal."""
    button = page.locator('#lightbox-body').get_by_text('Yes')
    if await button.is_visible():
        print("✓ 'Yes' confirmation button found.")
    else:
        print("✗ 'Yes' confirmation button not found.")
    return button
