from bs4 import BeautifulSoup
import os

# Step 1: Define the input file path
input_file_path = "to_clean.html"

# Step 2: Open the file and read its content
with open(input_file_path, "r") as file:
    html_content = file.read()

# Step 3: Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Step 4: Remove all <script> tags from the parsed HTML
for script in soup.find_all('script'):
    script.decompose()  # Removes the <script> tag and its content

# Step 5: Prettify the cleaned HTML (format it with proper indentation)
cleaned_html = soup.prettify()

# Step 6: Save the cleaned and prettified HTML to a new file
with open('to_scrape.html', 'w', encoding='utf-8') as file:
    file.write(cleaned_html)
print("HTML saved as 'to_scrape.html'")

# Step 7: Remove the original file after cleaning
os.remove(input_file_path)
print(f"Original file '{input_file_path}' removed.")
