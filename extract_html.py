from pyppeteer import launch
from pyppeteer_stealth import stealth
import asyncio
import random

# Step 1: Define the function to scroll to the bottom of the page
async def scroll_to_bottom(page, max_scrolls=80):
    """Scroll to the bottom of the page to load more content."""
    
    # Get the initial scroll height of the page
    previous_height = await page.evaluate("document.body.scrollHeight")
    scrolls = 0

    while scrolls < max_scrolls:
        
        # Wait for a second before scrolling
        await asyncio.sleep(1)
        
        # Scroll to the bottom
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        # Wait for a random period between 8 to 12 seconds before next action
        await asyncio.sleep(random.uniform(8, 12)) 

        # Get the new height of the page
        current_height = await page.evaluate("document.body.scrollHeight")

        # If the page height hasn't changed, stop scrolling
        if current_height == previous_height:
            break

        # Update the previous height and increment scroll count
        previous_height = current_height
        scrolls += 1
        print(f"Scrolled {scrolls} times.")

# Step 2: Define the main function to launch the browser and scrape the page
async def main():
    # Launch the browser with specified arguments
    browser = await launch(
        headless=False,  # Run the browser in non-headless mode
        args=[
            "--no-sandbox",  # Disable sandboxing for security reasons
            "--disable-setuid-sandbox",  # Disable setuid sandbox
            "--disable-dev-shm-usage",  # Disable /dev/shm usage
            "--disable-blink-features=AutomationControlled",  # Avoid detection of automation
            "--disable-infobars",  # Hide info bars
            "--ignore-certificate-errors",  # Ignore certificate errors
            "--ignore-certificate-errors-spki-list",  # Ignore certificate errors related to SPKI
        ],
    )

    # Create a new page in the browser
    page = await browser.newPage()
    
    # Apply stealth techniques to avoid detection as a bot
    await stealth(page)

    # Set the viewport size for the browser
    await page.setViewport({"width": 1280, "height": 720})

    # Set a custom user agent for the browser to simulate a real user
    await page.setUserAgent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )
    
    # Navigate to the target URL and wait until the page is fully loaded
    await page.goto(
        "https://medium.com/tag/webrtc/recommended", waitUntil="networkidle2"
    )

    # Step 3: Scroll to the bottom to load more content
    await scroll_to_bottom(page)
    
    # Step 4: Get the page's content after scrolling
    html = await page.content()

    # Step 5: Save the content to a file
    with open("to_clean.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("HTML saved to to_clean.html")

    # Step 6: Close the browser after scraping
    await browser.close()

# Step 7: Run the main function using asyncio
asyncio.run(main())
