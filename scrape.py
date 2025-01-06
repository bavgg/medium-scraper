from bs4 import BeautifulSoup

# Open the HTML file and read its contents
with open("your_file.html", "r") as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Now you can work with the 'soup' object
print(soup.prettify())  # Pretty print the HTML content
