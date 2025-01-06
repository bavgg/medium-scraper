from bs4 import BeautifulSoup
import os

# file name
input_file_path = "to_clean.html"
with open(input_file_path, "r") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Remove all <script> tags
for script in soup.find_all('script'):
    script.decompose()

# Prettify the HTML
cleaned_html = soup.prettify()

# Save the prettified HTML to a file
with open('to_scrape.html', 'w', encoding='utf-8') as file:
    file.write(cleaned_html)

print("HTML saved as 'to_scrape.html'")

# Remove the original file
os.remove(input_file_path)
print(f"Original file '{input_file_path}' removed.")
