from bs4 import BeautifulSoup
import os

def clean_html(input_file_path: str = "to_clean.html", output_file_path: str = 'to_scrape.html'):
    """
    Function to clean the HTML file by removing <script> tags and prettifying it.

    :param input_file_path: Path to the input HTML file to be cleaned.
    :param output_file_path: Path to the output file to save the cleaned HTML. Default is 'to_scrape.html'.
    """
    # Step 1: Open the file and read its content
    with open(input_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Step 2: Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Step 3: Remove all <script> tags from the parsed HTML
    for script in soup.find_all('script'):
        script.decompose()  # Removes the <script> tag and its content

    # Step 4: Prettify the cleaned HTML (format it with proper indentation)
    cleaned_html = soup.prettify()

    # Step 5: Save the cleaned and prettified HTML to a new file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_html)
    print(f"HTML saved as '{output_file_path}'")

    # Step 6: Remove the original file after cleaning
    os.remove(input_file_path)
    print(f"Original file '{input_file_path}' removed.")

# Entry point for running the script directly (optional)
# if __name__ == "__main__":
#     input_file = "to_clean.html"
#     clean_html(input_file)
