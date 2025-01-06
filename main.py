from extract_html import scrape_page
from clean_html import clean_html
from scrape import scrape_to_json_and_excel
import asyncio
import sys
import tkinter as tk
from tkinter import simpledialog


def show_dialogbox():
  global url
  root = tk.Tk()
  root.withdraw()  # Hide the main window

  # Make the dialog float
  root.attributes("-topmost", True)

  # Show an input dialog
  user_input = simpledialog.askstring("Scraper", "Enter URL:")
  url = user_input

# if len(sys.argv) > 1:
#   url = sys.argv[1]
# else:
#   print("Missing url argument")


# url = "https://medium.com/tag/webrtc/recommended"
show_dialogbox()
asyncio.run(scrape_page(url))

clean_html()

scrape_to_json_and_excel()


  