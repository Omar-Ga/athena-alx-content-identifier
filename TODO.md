# ATHENA AUTOMATION - TODO

This file tracks the implementation progress based on the `implementation-plan.md`. Our strategy is to build and integrate each module iteratively, testing the `main.py` script at each stage.

## Phase 1: Project Setup & Core Login

- [x] Create `.env` file for credentials.
- [x] Create `config.py` to load environment variables.
- [x] Implement initial browser setup and login logic.
- [x] Modularize login logic into `modules/login_module.py`.
- [x] Create `main.py` as the entry point.
- [x] Implement logic in `main.py` to perform login and then prompt user for the first lesson URL.

## Phase 2: Navigator Module

- [x] Create `modules/navigator_module.py`.
- [x] Implement function to detect content type on a page (`detect_content_type`).
    - [x] Detect `iframe[src*="slides"]` for Google Slides.
    - [x] Detect `iframe[src*="pdf"]` or `embed[type*="pdf"]` for PDF.
    - [x] Detect `video` or `iframe[src*="youtube" or "video"]` for Video.
- [x] Implement functions to find key buttons:
    - [x] Find "Set As Complete" button.
    - [x] Find "Next" button.
- [x] Integrate `navigator_module.py` into `main.py` to be called after navigating to the lesson URL.

## Phase 3: Content Processor Module

- [x] Create `modules/content_processor_module.py`.
- [x] Implement PDF handling (do nothing, return `None`).
- [ ] Implement Google Slides handling:
    - [x] Set up Google Slides API credentials.
    - [x] Implement function to extract text from a presentation URL.
- [ ] Implement Video handling:
    - [ ] Implement network interception to find `.vtt` file URLs.
    - [ ] Implement function to download and parse `.vtt` file into text.
- [ ] Integrate `content_processor_module.py` into `main.py`.

## Phase 4: MCQ Handler Module

- [ ] Create `modules/mcq_handler_module.py`.
- [ ] Implement function to detect if MCQs are present.
- [ ] Implement function to extract question and answer options.
- [ ] Set up Google Gemini SDK.
- [ ] Implement function to call Gemini API with context, question, and options.
- [ ] Implement logic to parse Gemini's JSON response and click the correct answer.
- [ ] Implement loop to handle all questions in a quiz.
- [ ] Integrate `mcq_handler_module.py` into `main.py`.

## Phase 5: Completion Handler & Main Loop

- [ ] Create `modules/completion_handler_module.py`.
- [ ] Implement function to handle the "Are you sure?" confirmation modal.
- [ ] Implement the main automation loop in `main.py`:
    - [ ] Call Navigator to identify content.
    - [ ] Call Content Processor to get context.
    - [ ] Click "Set As Complete".
    - [ ] Call MCQ Handler if questions appear.
    - [ ] Call Completion Handler to confirm.
    - [ ] Click "Next".
    - [ ] Implement `MAX_PAGES` limit.

## Phase 6: Final Testing & Refinements

- [ ] Conduct end-to-end testing on a full course section.
- [ ] Add error handling and retry logic.
- [ ] Refine logging and user feedback.
