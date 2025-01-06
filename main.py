from extract_html import scrape_page
from clean_html import clean_html
from scrape import scrape_to_json_and_excel
import asyncio
import sys

url = "https://medium.com/tag/webrtc/recommended"
asyncio.run(scrape_page(url))

clean_html()

scrape_to_json_and_excel()

# if len(sys.argv) > 1:
#   url = sys.argv[1]
# else:
#   print("Missing url argument")
  