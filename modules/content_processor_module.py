import asyncio
import os
import re
import webvtt
from io import StringIO
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/presentations.readonly"]

async def extract_slides_text(page, slides_url):
    """
    Extracts text content from a Google Slides presentation.
    """
    print(f"   ↳ Extracting text from Google Slides: {slides_url}")

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("slides", "v1", credentials=creds)

        # Extract presentation ID from the URL
        match = re.search(r"presentation\/d\/([a-zA-Z0-9-_]+)", slides_url)
        if not match:
            print("   ✗ Could not extract presentation ID from the URL.")
            return None
        presentation_id = match.group(1)

        # Call the Slides API
        presentation = (
            service.presentations()
            .get(presentationId=presentation_id)
            .execute()
        )
        slides = presentation.get("slides")

        full_text = []
        if not slides:
            print("   ↳ No slides found in the presentation.")
            return None

        for i, slide in enumerate(slides):
            slide_text = f"--- Slide {i + 1} ---\n"
            for element in slide.get("pageElements", []):
                if "shape" in element and "text" in element["shape"]:
                    text_content = element["shape"]["text"]["textElements"]
                    for text_element in text_content:
                        if "textRun" in text_element:
                            slide_text += text_element["textRun"]["content"]
            full_text.append(slide_text)
        
        print(f"   ✓ Successfully extracted text from {len(slides)} slides.")
        return "\n".join(full_text)

    except HttpError as err:
        print(f"   ✗ An error occurred with the Google Slides API: {err}")
        return None
    except Exception as e:
        print(f"   ✗ An unexpected error occurred during slides text extraction: {e}")
        return None

async def extract_vtt_transcript(page):
    """
    Extracts text transcript from a video by intercepting VTT files.
    """
    print("   ↳ Looking for video transcript (VTT file)...")
    
    try:
        # Find the video iframe
        video_iframe_selector = 'iframe[title*="player.vimeo.com"]'
        video_iframe_locator = page.locator(video_iframe_selector)
        if await video_iframe_locator.count() == 0:
            print("   ✗ Video iframe not found.")
            return None
        
        video_frame = page.frame_locator(video_iframe_selector)

        async with page.expect_response(lambda response: ".vtt" in response.url, timeout=30000) as response_info:
            print("   ... Waiting for VTT file response...")

            # Click the play button to ensure video starts and loads all assets
            play_button = video_frame.get_by_role('button', name='Play')
            if await play_button.count() > 0:
                print("   ► Clicking play button...")
                await play_button.click()

            # Explicitly wait for the CC button to be visible
            cc_button = video_frame.get_by_role('button', name='CC/subtitles')
            try:
                print("   ... Waiting for CC button to become visible...")
                await cc_button.wait_for(state='visible', timeout=10000)
                print("   ✓ CC button is visible.")
                
                is_pressed = await cc_button.get_attribute('aria-pressed')
                if is_pressed != 'true':
                    print("   ► Clicking CC button to enable subtitles...")
                    await cc_button.click()
                else:
                    print("   ✓ CC/subtitles already enabled.")
            
            except Exception as e:
                print(f"   ✗ Could not click CC button: {e}")

        response = await response_info.value
        vtt_content = await response.text()
        print(f"   ✓ VTT file found: {response.url}")

        if vtt_content:
            # Parse the VTT content
            transcript = ""
            for caption in webvtt.read_buffer(StringIO(vtt_content)):
                transcript += caption.text.strip() + " "
            print(f"   ✓ Successfully extracted transcript.")
            return transcript.strip()
        else:
            print("   ✗ VTT content was not captured.")
            return None

    except Exception as e:
        print(f"   ✗ An error occurred during VTT extraction: {e}")
        return None


async def process_content(page, content_type):
    """
    Processes the learning material based on embed type.
    """
    print(f"\n⚙️ Processing content of type: {content_type}")

    if content_type == "pdf":
        print("   ↳ PDF content detected. No specific processing needed at this stage.")
        return None, None
    elif content_type == "slides":
        # For slides, we need to get the actual slides URL from the iframe
        slides_iframe = page.locator('iframe[src*="docs.google.com/presentation"]').first
        if await slides_iframe.is_visible():
            slides_url = await slides_iframe.get_attribute('src')
            if slides_url:
                content = await extract_slides_text(page, slides_url)
                return content, 'slides'
            else:
                print("   ✗ Could not get slides URL from iframe.")
                return None, None
        else:
            print("   ✗ Google Slides iframe not found.")
            return None, None
    elif content_type == "video":
        content = await extract_vtt_transcript(page)
        return content, 'video'
    else:
        print("   ↳ Unknown content type. No processing performed.")
        return None, None
