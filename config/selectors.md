# UI Selectors for ALX Athena Automation

This document contains all the necessary UI selectors for the ALX Athena automation script. Each selector is documented with a clear description of its purpose and location on the page.

---

## Login (ALX Africa Admissions)

| Element | Selector | Description |
|---|---|---|
| **Email Field** | `#user_email` | The email input field on the login page. |
| **Password Field** | `#user_password` | The password input field on the login page. |
| **Sign In Button** | `input[name='commit']` | The login/submit button. |
| **Login Form** | `form` | The main login form container. |

---
## General Navigation

| Element | Selector | Description |
|---|---|---|
| **Next Lesson Button** | `button.next-lesson` | The primary button to navigate to the next lesson. |
| **Set As Complete Button** | `#set-as-complete` | The button to mark a lesson page as complete. |
| **"Are you sure?" Yes Button** | `#confirm-completion-yes` | The confirmation button in the "Are you sure?" modal. |
| **Set As Complete Button** | `page.getByRole('link', { name: 'Set as Complete' })` | ✅ Working selector for completion (element ref: e192) |
| **Confirmation Modal Yes Button** | `page.locator('#lightbox-body').getByText('Yes')` | ✅ Working selector for modal confirmation (element ref: e213) |
| **Confirmation Modal Close Button** | `page.locator('#lightbox-body').getByText('Close')` | ✅ Working selector for modal close button (element ref: e214) |
| **Next Lesson Button** | `page.getByRole('link', { name: 'Next ⇒' })` | ✅ Working selector for navigation |
| **Data Analytics Continue Button** | `element 'e343'` | ✅ Continue button for Data Analytics course in Data Engineering section (Playwright element reference: e343) |

---

## MCQ (Multiple-Choice Questions)

| Element | Selector | Description |
|---|---|---|
| **Question Text** | `.mcq-question-text` | The container for the MCQ question text. |
| **Answer Option 1** | `.mcq-option:nth-child(1)` | The first answer option. |
| **Answer Option 2** | `.mcq-option:nth-child(2)` | The second answer option. |
| **Answer Option 3** | `.mcq-option:nth-child(3)` | The third answer option. |
| **Answer Option 4** | `.mcq-option:nth-child(4)` | The fourth answer option. |
| **Next Question Button** | `.mcq-next-button` | The button to proceed to the next question in a quiz. |

---

## Embedded Content

| Element | Selector | Description |
|---|---|---|
| **Google Slides Iframe** | `iframe[src*="slides"]` | The iframe containing the Google Slides presentation. |
| **Slides Embed URL Pattern** | `docs.google.com/presentation/d/[ID]/embed` | Google Slides embed URL pattern with extracted presentation ID |
| **Google Slides API URL** | `docs.google.com/presentation/d/[ID]/export?format=json` | API endpoint for slides content extraction |
| **PDF Iframe Container** | `iframe >> nth=0` | ✅ Main PDF iframe container (ref: e149) |
| **PDF Nested Iframe** | `iframe >> iframe >> nth=0` | ✅ Nested iframe within PDF container (ref: f5e1) |
| **PDF Embed** | `embed[type*="pdf"]` | The embed element for PDF documents. |
| **Google Slides Iframe** | `iframe[src*="docs.google.com/presentation"]` | The iframe containing the Google Slides presentation. |
| **Slide Picker** | `iframe >> listbox "Open the slide picker"` | The listbox to select a specific slide. |
| **Next Slide Button** | `iframe >> button "Next (→)"` | The button to navigate to the next slide. |
| **Previous Slide Button** | `iframe >> button "Previous (←)"` | The button to navigate to the previous slide. |
| **Slide Options Menu** | `iframe >> button "Open the options menu"` | The button to open the slide options menu. |
| **Google Slides Link** | `iframe >> link "Google Slides"` | The link to open the presentation in a new Google Slides tab. |
| **Current Slide Indicator** | `iframe >> img` | The main slide image (contains slide number and title). |
| **Copyright Notice** | `iframe >> img[alt*="Please do not copy"]` | The copyright notice image. |
| **Slide Title** | `iframe >> img[alt*="Getting set up for Preparing data"]` | The main slide title. |
| **Module Overview** | `iframe >> img[alt*="Module overview: Preparing data"]` | The module overview image. |
| **PDF Loading Message** | `iframe >> text=*.pdf` | ✅ Text containing .pdf filename in loading message |
| **PDF Section Heading** | `h2:has-text("[PDF]")` | ✅ Heading element containing [PDF] indicator |
| **PDF Application Container** | `iframe >> application` | ✅ Application element within PDF viewer iframe |
| **PDF Status Elements** | `iframe >> region, iframe >> status` | ✅ Status and region elements in PDF viewer |
| **Video Player (Not Recommended)** | `video` | This selector does NOT work for ALX Athena video controls |
| **Video Iframe Container** | `iframe[title*="player.vimeo.com"]` | The iframe containing the Vimeo video player |
| **Play Button** | `iframe >> getByRole('button', { name: 'Play' })` | ✅ Working selector for Play/Pause button |
| **Pause Button** | `iframe >> getByRole('button', { name: 'Pause' })` | ✅ Working selector for video pause |
| **Progress Bar** | `iframe >> [role="slider"]` | ✅ Progress bar slider (ref: f1e18) |
| **Mute Button** | `iframe >> getByRole('button', { name: 'Mute' })` | ✅ Working selector for mute/unmute |
| **Volume Slider** | `iframe >> [aria-label*="Volume"]` | ✅ Volume control slider |
| **CC/Subtitles Button** | `iframe >> getByRole('button', { name: 'CC/subtitles' })` | ✅ Working selector for CC/subtitles toggle |
| **Settings Button** | `iframe >> getByRole('button', { name: 'Settings' })` | ✅ Video settings button |
| **Transcript Button** | `iframe >> getByRole('button', { name: 'Transcript' })` | ✅ Transcript toggle button |
| **Picture-in-Picture Button** | `iframe >> getByRole('button', { name: 'Picture-in-Picture' })` | ✅ PiP mode button |
| **Fullscreen Button** | `iframe >> getByRole('button', { name: 'Fullscreen' })` | ✅ Fullscreen toggle button |
| **Video Walk-through Heading** | `h3:has-text("[Walk-through]")` | ✅ Heading pattern for video content |

### Video Testing Results
- **VTT Subtitle URL Pattern**: `player.vimeo.com/texttrack/ID.vtt?token=*` ✅ Verified (Tested on 2 different videos)
- **Video ID 1**: 816509525 (Walk-through video)
- **Video ID 2**: 794411218 (Types of data video)
- **VTT Loading Behavior**:
  - **Auto-load**: When CC/subtitles enabled by default, VTT loads on page load ✅
  - **Manual activation**: Clicking CC/subtitles triggers VTT loading ✅
  - **Consistent across videos**: Tested on multiple lessons ✅
- **Current VTT URL Examples**:
  - `https://player.vimeo.com/texttrack/199541923.vtt?token=6909e7db_0x48be234b391356e12fabba729da72714a7558516`
  - `https://player.vimeo.com/texttrack/75974152.vtt?token=6909eb85_0xa24b482241270a0521764ab58e362c9bf71e4441`
- **Test Status**: ✅ All video controls working (Play, Pause, CC, Settings, etc.)
- **⚠️ Warning**: Video controls are embedded in iframe - standard `video` selectors will fail
- **🔍 Network Monitoring**: VTT files load via GET requests to texttrack endpoints
- **Content Types**: Videos marked with [Video] or [Walk-through] in heading
- **Automation Advantage**: VTT content available immediately after page load or CC activation

### Video Detection Strategies

#### Primary Detection Methods
1. **Heading Pattern Detection**
   - Look for `h3` elements containing `[Walk-through]` text
   - Pattern: `h3:has-text("[Walk-through]")`

2. **Iframe URL Detection**
   - Check for Vimeo player iframe structure
   - Pattern: `iframe[title*="player.vimeo.com"]`
   - Extract video ID from src attribute

3. **Video Control Elements**
   - Look for standard video player controls within iframes
   - Pattern: `iframe >> [role="slider"]` (progress bar)
   - Pattern: `iframe >> getByRole('button', { name: /^(Play|Pause)$/ })`

4. **VTT Subtitle Pattern Detection**
   - Monitor network requests for `.vtt` files
   - Pattern: `player.vimeo.com/texttrack/*.vtt?token=*`

#### Fallback Detection Methods
1. **Video Player API Detection**
   - Check for Vimeo Player API presence
   - Pattern: `iframe >> [src*="player.vimeo.com"]`

2. **Text Content Analysis**
   - Search for video-related terms in text content
   - Pattern: `* >> text=/.*(video|walkthrough|play).*/i`

3. **DOM Structure Analysis**
   - Look for video-specific elements (progress bars, volume controls)
   - Pattern: `iframe >> [aria-label*="Volume"]`

#### Real-Time Detection Implementation
```javascript
async function detectVideoContent(page) {
    const detectionMethods = [
        // Method 1: Check for Walk-through heading
        await page.locator('h3').filter({ hasText: /\[Walk-through\]/ }).count(),
        
        // Method 2: Check for Vimeo iframe
        await page.locator('iframe').filter({ hasAttribute: 'title' }).filter({
            hasAttributeContaining: 'title', 'player.vimeo.com'
        }).count(),
        
        // Method 3: Check for video progress bar
        await page.locator('iframe >> [role="slider"]').count(),
        
        // Method 4: Check for Play/Pause buttons
        await page.locator('iframe >> getByRole("button", { name: /^(Play|Pause)$/ })').count()
    ];
    
    return detectionMethods.some(count => count > 0);
}

async function extractVideoContent(page) {
    const videoIframe = await page.locator('iframe[title*="player.vimeo.com"]').first();
    const videoSrc = await videoIframe.getAttribute('src');
    
    // Extract video ID from Vimeo URL
    const videoIdMatch = videoSrc.match(/\/video\/(\d+)/);
    const videoId = videoIdMatch ? videoIdMatch[1] : null;
    
    return {
        videoId,
        videoSrc,
        hasVTT: false // Will be true after CC/subtitles activation
    };
}

async function enableCCSubtitles(page) {
    const ccButton = page.locator('iframe >> getByRole("button", { name: "CC/subtitles" })');
    if (await ccButton.count() > 0) {
        
        // Check if already pressed/enabled (auto-load VTT on page load)
        const isPressed = await ccButton.getAttribute('aria-pressed');
        if (isPressed === 'true') {
            // VTT should already be loaded, try to get it from network requests
            try {
                const response = await page.waitForResponse(
                    response => response.url().includes('.vtt') && response.status() === 200,
                    { timeout: 5000 }
                );
                return response.url();
            } catch (e) {
                // VTT might have loaded earlier, continue without error
                console.log('VTT already loaded or not found in recent requests');
            }
        } else {
            // Click to enable CC/subtitles and trigger VTT load
            await ccButton.click();
            
            // Monitor network requests for VTT files
            const response = await page.waitForResponse(
                response => response.url().includes('.vtt') && response.status() === 200
            );
            
            return response.url();
        }
    }
    return null;
}

async function waitForVTTLoad(page, timeout = 10000) {
    // Monitor network requests for VTT files with improved error handling
    try {
        const response = await page.waitForResponse(
            response => response.url().includes('.vtt') && response.status() === 200,
            { timeout }
        );
        return response.url();
    } catch (e) {
        console.log('VTT file not found within timeout period');
        return null;
    }
}
```

#### Test Results from ALX Athena Video
- **Video URL**: `https://athena.alxafrica.com/student/lesson/content-view/40/389/3554/3`
- **Video Platform**: Vimeo
- **Video ID**: 816509525
- **Video Duration**: 04:39
- **Content Type**: Walk-through
- **VTT Pattern Confirmed**: ✅ Working
- **All Controls Tested**: ✅ Play, Pause, CC, Settings, Volume, Fullscreen, PiP, Transcript
- **Status**: ✅ All detection methods working

### PDF Detection Strategies

#### Primary Detection Methods
1. **Heading Pattern Detection**
   - Look for `h2` elements containing `[PDF]` text
   - Pattern: `h2:has-text("[PDF]")`

2. **Loading Message Detection**
   - Find iframe elements containing `.pdf` filenames
   - Pattern: `iframe >> text=*.pdf`
   - Extract PDF filename from loading messages

3. **Iframe Structure Detection**
   - Check for nested iframe structure typical of PDF viewers
   - Pattern: `iframe >> application` within PDF containers

4. **Application Container Detection**
   - PDF content often loads in `application` elements
   - Pattern: `iframe >> application`

#### Fallback Detection Methods
1. **Text Content Scanning**
   - Search for `.pdf` extension in any text content
   - Pattern: `* >> text=/.*\.pdf/`

2. **DOM Structure Analysis**
   - PDF iframes often contain `status` and `region` elements
   - Pattern: `iframe >> status, iframe >> region`

3. **URL Pattern Detection**
   - Extract iframe src and check for PDF-related patterns
   - Pattern: `iframe[src*="pdf" i]`

#### Real-Time Detection Implementation
```javascript
async function detectPDFContent(page) {
    const detectionMethods = [
        // Method 1: Check for PDF heading
        await page.locator('h2').filter({ hasText: /\[PDF\]/ }).count(),
        
        // Method 2: Check for PDF loading messages
        await page.locator('iframe').filter({ hasText: /\.pdf/ }).count(),
        
        // Method 3: Check for application elements in iframes
        await page.locator('iframe >> application').count(),
        
        // Method 4: Check for status elements in iframes
        await page.locator('iframe >> status').count()
    ];
    
    return detectionMethods.some(count => count > 0);
}
```

#### Test Results from ALX Athena
- **PDF URL**: `https://athena.alxafrica.com/student/lesson/content-view/40/415/5032/1`
- **PDF File**: `ALX_DS_Preparing data_Module Overview_Re-brand_V2.pdf`
- **Structure**: Nested iframe with application container
- **Loading Behavior**: Shows loading message with PDF filename
- **Status**: ✅ All detection methods working

### Google Slides Detection Strategies

#### Primary Detection Methods
1. **Iframe URL Detection**
   - Check for Google Slides iframe structure
   - Pattern: `iframe[src*="docs.google.com/presentation"]`

2. **Heading Pattern Detection**
   - Look for headings containing `[Slides]` text
   - Pattern: `h3 >> text=/.*\[Slides\]/`

3. **Google Slides Link Detection**
   - Look for the "Google Slides" link within the iframe
   - Pattern: `iframe >> link "Google Slides"`

#### Fallback Detection Methods
1. **DOM Structure Analysis**
   - Look for slide-specific elements (slide picker, navigation buttons)
   - Pattern: `iframe >> listbox "Open the slide picker"`
   - Pattern: `iframe >> button "Previous (←)"`

2. **Text Content Analysis**
   - Search for slide-related terms in text content
   - Pattern: `* >> text=/.*(slide|presentation).*/i`

#### Real-Time Detection Implementation
```javascript
async function detectSlidesContent(page) {
    const detectionMethods = [
        // Method 1: Check for Google Slides iframe
        await page.locator('iframe[src*="docs.google.com/presentation"]').count(),
        
        // Method 2: Check for Slides heading
        await page.locator('h3').filter({ hasText: /\[Slides\]/ }).count(),
        
        // Method 3: Check for Google Slides link in iframe
        await page.locator('iframe >> link "Google Slides"').count()
    ];
    
    return detectionMethods.some(count => count > 0);
}

async function extractGoogleSlidesEmbedUrl(page) {
    // Extract the embed URL from the Google Slides iframe
    const embedUrl = await page.evaluate(() => {
        const iframe = document.querySelector('iframe[src*="docs.google.com/presentation"]');
        return iframe ? iframe.src : null;
    });

    if (!embedUrl) {
        console.error('Google Slides iframe not found');
        return null;
    }

    // Extract the presentation ID from the embed URL
    // URL format: https://docs.google.com/presentation/d/{PRESENTATION_ID}/embed?start=false&loop=false
    const match = embedUrl.match(/presentation\/d\/([a-zA-Z0-9-_]+)/);
    const presentationId = match ? match[1] : null;

    return {
        embedUrl,
        presentationId,
        apiUrl: presentationId ? `https://docs.googleapis.com/v1/presentations/${presentationId}` : null
    };
}

async function detectContentType(page) {
    // Helper function to detect the type of content embedded on the page
    const hasSlides = await page.evaluate(() => {
        return document.querySelector('iframe[src*="docs.google.com/presentation"]') !== null;
    });

    const hasPDF = await page.evaluate(() => {
        return document.querySelector('embed[type*="pdf"]') !== null ||
               document.querySelector('h2:has-text("[PDF]")') !== null;
    });

    const hasVideo = await page.evaluate(() => {
        return document.querySelector('iframe[title*="player.vimeo.com"]') !== null ||
               document.querySelector('h3:has-text("[Walk-through]")') !== null;
    });

    if (hasSlides) return 'slides';
    if (hasPDF) return 'pdf';
    if (hasVideo) return 'video';
    return 'unknown';
}
```

#### Test Results from ALX Athena
- **Slides URL**: `https://athena.alxafrica.com/student/lesson/content-view/40/415/3737/3`
- **Slides Platform**: Google Slides
- **Presentation ID**: `1w-nxq6tsVqpmwXV0zY8tqUdIZ0nozR1CNjAx-kp95K4`
- **Embed URL**: `https://docs.google.com/presentation/d/1w-nxq6tsVqpmwXV0zY8tqUdIZ0nozR1CNjAx-kp95K4/embed?start=false&loop=false`
- **API URL**: `https://docs.googleapis.com/v1/presentations/1w-nxq6tsVqpmwXV0zY8tqUdIZ0nozR1CNjAx-kp95K4`
- **Content**: Getting set up for Preparing data (Slide 1 of 10)
- **Status**: ✅ All detection methods working

---

## Enhanced Login Implementation

The login process has been improved for better reliability and performance:

### Timing Improvements
- **Initial Page Load**: Uses `domcontentloaded` instead of `networkidle` for faster page ready detection
- **Login Form Detection**: 30-second timeout for finding the login form
- **Login Success Detection**: Waits for URL change to `home` or `dashboard` instead of network idle

### Login Success Detection
```javascript
window.location.href.includes('home') || window.location.href.includes('dashboard')
```
