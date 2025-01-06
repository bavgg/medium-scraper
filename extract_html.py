from pyppeteer import launch
from pyppeteer_stealth import stealth
import asyncio

import random

from pyppeteer.errors import TimeoutError


async def wait_for_network_idle(page, timeout=5000):
    try:
        await page.waitForFunction(
            """() => {
                const performance = window.performance.getEntriesByType('resource');
                return performance.every(r => r.responseEnd < performance[performance.length - 1].responseEnd);
            }""",
            timeout=timeout,
        )
    except TimeoutError:
        print("Network idle check timed out. Continuing without waiting further.")


async def scroll_to_bottom(page, scroll_pause_time=8, max_scrolls=80):
    """Scroll to the bottom of the page to load more content."""
    previous_height = await page.evaluate("document.body.scrollHeight")
    scrolls = 0

    no_load_count = 0
    while scrolls < max_scrolls:
        # Scroll to the bottom
        await asyncio.sleep(1)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        await asyncio.sleep(random.uniform(8, 12))  # Pause to allow content to load

        # Check the new scroll height
        current_height = await page.evaluate("document.body.scrollHeight")
        print(current_height)

        if current_height == previous_height:
            break
        # if current_height == previous_height:
        #     print("No more content to load.")
        #     await asyncio.sleep(10)
        #     no_load_count += 1
        # if no_load_count == 10:
        #     break
        previous_height = current_height
        scrolls += 1
        print(f"Scrolled {scrolls} times.")


async def main():
    # # Set the path to Google Chrome
    # chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # Replace with your Chrome path
    # browser = await launch(headless=False, executablePath=chrome_path)  # Use Google Chrome
    # # Launch browser with headless mode disabled
    browser = await launch(
        headless=False,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--ignore-certificate-errors",
            "--ignore-certificate-errors-spki-list",
        ],
    )
    page = await browser.newPage()
    await stealth(page)  # Enable stealth mode
    # Set a realistic viewport
    await page.setViewport({"width": 1280, "height": 720})

    # Set a realistic User-Agent
    await page.setUserAgent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )
    await page.goto(
        "https://medium.com/tag/webrtc/recommended", waitUntil="networkidle2"
    )

    # Scroll to load all content
    await scroll_to_bottom(page)

    # Take a screenshot after loading all content
    await page.screenshot({"path": "example.png"})

    # Get the full HTML content
    html = await page.content()
    with open("medium_page_full.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("HTML saved to medium_page_full.html")

    await browser.close()


# Run the event loop
asyncio.run(main())
