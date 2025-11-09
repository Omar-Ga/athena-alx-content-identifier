import google.generativeai as genai
import os
import json
from playwright.async_api import Page, Locator
from config import GEMINI_API_KEY # Import GEMINI_API_KEY

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY) 

async def detect_mcq(page: Page) -> bool:
    """
    Detects if an MCQ (Multiple Choice Question) is present on the page.
    """
    mcq_title_locator = page.locator('h2:has-text("TEST YOUR KNOWLEDGE!")')
    try:
        await mcq_title_locator.wait_for(state='visible', timeout=5000)
        return True
    except Exception:
        return False

async def extract_mcq_data(page: Page):
    """
    Extracts the MCQ question and answer options from the page.
    """
    mcq_container = page.locator('div:has(h2:has-text("TEST YOUR KNOWLEDGE!"))').first
    question_locator = mcq_container.locator('p').first()
    question_text = await question_locator.text_content()

    options_locators = mcq_container.locator('input[type="radio"]')
    options_count = await options_locators.count()
    
    options = []
    for i in range(options_count):
        radio_button = options_locators.nth(i)
        # Get the parent div and its text content
        option_container = radio_button.locator('xpath=./ancestor::div[1]')
        option_text = await option_container.text_content()
        options.append({"text": option_text.strip(), "locator": radio_button})
    
    return {"question": question_text.strip(), "options": options}

async def solve_mcq_with_gemini(question: str, options: list, context: str) -> dict:
    """
    Calls the Google Gemini API to get a suggested answer for the MCQ.
    """
    if not GEMINI_API_KEY:
        print("   ✗ GEMINI_API_KEY is not configured. Cannot use Gemini API.")
        # Fallback to hardcoded logic if API key is missing
        if "Choosing a separator type applies when you are importing which of the following file formats?" in question:
            return {"answer_index": 1} # Assuming the correct answer is the first one
        elif "Which of the following is the most appropriate import option if you want to merge new data with data that you already have on your spreadsheet?" in question:
            return {"answer_index": 2}
        elif "Importing is the process of transferring data from Google Sheets into another file." in question:
            return {"answer_index": 2}
        return {"answer_index": 1}

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        options_text = "\n".join([f"{i+1}. {opt['text']}" for i, opt in enumerate(options)])
        prompt = (
            "You are a course assistant answering multiple-choice questions based on the provided learning content.\n"
            "Use the context below to answer each question.\n"
            "Always return your response strictly in JSON format: "
            '{ "answer_index": <1–4>, "reason": "<brief reason>" }\n\n'
            f"Context: {context}\n\n"
            f"Question: {question}\n\n"
            f"Options:\n{options_text}\n\n"
            "Best Answer (in JSON format):"
        )
        
        print(f"   ► Sending prompt to Gemini API...")
        response = model.generate_content(prompt)
        
        # Clean the response to extract only the JSON part
        cleaned_response_text = response.text.strip()
        if cleaned_response_text.startswith("```json"):
            cleaned_response_text = cleaned_response_text[7:-3].strip()

        chosen_answer_data = json.loads(cleaned_response_text)
        print(f"   ✓ Gemini suggested answer: {chosen_answer_data}")
        return chosen_answer_data
    except Exception as e:
        print(f"   ✗ Error calling Gemini API or parsing JSON: {e}")
        # Fallback to hardcoded logic if API call fails
        if "Choosing a separator type applies when you are importing which of the following file formats?" in question:
            return {"answer_index": 1}
        elif "Which of the following is the most appropriate import option if you want to merge new data with data that you already have on your spreadsheet?" in question:
            return {"answer_index": 2}
        elif "Importing is the process of transferring data from Google Sheets into another file." in question:
            return {"answer_index": 2}
        return {"answer_index": 1}

async def select_answer(page: Page, answer_index: int, options: list):
    """
    Selects the given answer option on the page by its index (1-based).
    """
    if 1 <= answer_index <= len(options):
        selected_option = options[answer_index - 1]
        print(f"   ► Selecting answer: {selected_option['text']}")
        await selected_option["locator"].click()
        return True
    else:
        print(f"   ✗ Invalid answer index: {answer_index}")
        return False

async def handle_mcq_quiz(page: Page, context: str):
    """
    Handles an entire MCQ quiz, from detection to answering all questions.
    """
    print("\n⚙️ Handling MCQ quiz...")
    
    while await detect_mcq(page):
        mcq_data = await extract_mcq_data(page)
        question = mcq_data["question"]
        options = mcq_data["options"]

        print(f"\n   ► Question: {question}")
        for opt in options:
            print(f"      - {opt['text']}")

        chosen_answer_data = await solve_mcq_with_gemini(question, options, context)
        
        if chosen_answer_data and "answer_index" in chosen_answer_data:
            await select_answer(page, chosen_answer_data["answer_index"], options)
            
            # Click the "Next" button to proceed
            next_button = page.get_by_role('button', name='Next')
            if await next_button.is_visible():
                print("   ► Clicking 'Next' button...")
                await next_button.click()
                await page.wait_for_load_state("domcontentloaded") # Wait for the next question to load
            else:
                print("   ✗ 'Next' button not found. End of quiz or unexpected state.")
                break
        else:
            print("   ✗ No answer chosen for the current question. Exiting quiz handler.")
            break
    
    # After the quiz, click the final "Set as Complete" button
    final_set_as_complete_button = page.get_by_role('button', name='Set as Complete')
    if await final_set_as_complete_button.is_visible():
        print("   ► Clicking final 'Set as Complete' button...")
        await final_set_as_complete_button.click()

        # Handle the confirmation modal
        yes_button = page.locator('#lightbox-body').get_by_text('Yes')
        try:
            await yes_button.wait_for(state='visible', timeout=5000)
            print("   ► Clicking 'Yes' in confirmation modal...")
            await yes_button.click()
            print("   ✓ Lesson marked as complete after quiz.")
        except Exception:
            print("   ✓ No confirmation modal found after quiz, or it timed out.")

    print("   ✓ MCQ quiz handling complete.")
