from pyppeteer import launch
from pyppeteer_stealth import stealth
import asyncio
import random

async def scroll_to_bottom(page, max_scrolls=2):
    """Scroll to the bottom of the page to load more content."""
    previous_height = await page.evaluate("document.body.scrollHeight")
    scrolls = 0

    while scrolls < max_scrolls:
        await asyncio.sleep(1)  # Wait before scrolling
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(random.uniform(8, 12))  # Wait randomly before next scroll

        current_height = await page.evaluate("document.body.scrollHeight")

        if current_height == previous_height:
            break

        previous_height = current_height
        scrolls += 1
        print(f"Scrolled {scrolls} times.")

async def scrape_page(url, output_file="to_clean.html"):
    """Main scraping function to fetch and save the page content."""
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
    await stealth(page)
    await page.setViewport({"width": 1280, "height": 720})
    await page.setUserAgent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )

    await page.goto(url, waitUntil="networkidle2")
    await scroll_to_bottom(page)

    html = await page.content()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML saved to {output_file}")

    await browser.close()

# Entry point for running the script directly
# if __name__ == "__main__":
#     asyncio.run(scrape_page("https://medium.com/tag/webrtc/recommended"))
