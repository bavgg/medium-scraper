from bs4 import BeautifulSoup
import json
import os
from openpyxl import Workbook

def get_number_claps(component):
    """
    Function to get the number of claps from each component.
    """
    svgs = component.find_all("svg")
    for svg in svgs:
        path = svg.find('path', {'d': 'm3.672 10.167 2.138 2.14h-.002c1.726 1.722 4.337 2.436 5.96.81 1.472-1.45 1.806-3.68.76-5.388l-1.815-3.484c-.353-.524-.849-1.22-1.337-.958-.49.261 0 1.56 0 1.56l.78 1.932L6.43 2.866c-.837-.958-1.467-1.108-1.928-.647-.33.33-.266.856.477 1.598.501.503 1.888 1.957 1.888 1.957.17.174.083.485-.093.655a.56.56 0 0 1-.34.163.43.43 0 0 1-.317-.135s-2.4-2.469-2.803-2.87c-.344-.346-.803-.54-1.194-.15-.408.406-.273 1.065.11 1.447.345.346 2.31 2.297 2.685 2.67l.062.06c.17.175.269.628.093.8-.193.188-.453.33-.678.273a.9.9 0 0 1-.446-.273S2.501 6.84 1.892 6.23c-.407-.406-.899-.333-1.229 0-.525.524.263 1.28 1.73 2.691.384.368.814.781 1.279 1.246m8.472-7.219c.372-.29.95-.28 1.303.244V3.19l1.563 3.006.036.074c.885 1.87.346 4.093-.512 5.159l-.035.044c-.211.264-.344.43-.74.61 1.382-1.855.963-3.478-.248-5.456L11.943 3.88l-.002-.037c-.017-.3-.039-.71.203-.895'})
        if path:
            span_clap = svg.find_next('span')
            num_claps = span_clap.text
            return num_claps.strip()

    return "0"

def get_title(component):
    """
    Function to get the title from each component.
    """
    h2_title = component.find("h2", class_="bf ki kj kk kl km kn ko kp kq kr ks it iu kt ku iv kv kw kx ky kz la lb lc ld le ih ig jr jt jv bk")
    title = (h2_title.text).strip()
    return title

def get_url(component):
    """
    Function to get the URL from each component.
    """
    div_tag = component.find("div", class_="jy jz ka kb kc kd ke kf kg kh")
    a_tag = div_tag.find("a", class_="af ag ah ai aj ak al am an ao ap aq ar as at")

    href_value = a_tag.get("href")
    clean_url = href_value.split("?")[0]
    return "https://medium.com" + clean_url

def scrape_to_json_and_excel(input_file_path = "to_scrape.html", json_output_path='data.json', excel_output_path='data.xlsx'):
    """
    Function to scrape HTML content and save to JSON and Excel.
    """
    # Step 1: Open the HTML file and read its contents
    with open(input_file_path, "r") as file:
        html_content = file.read()

    # Step 2: Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Step 3: Find all the relevant components in the HTML
    components = soup.find_all("div", class_=["l es jx"])

    # Step 4: Initialize an Excel workbook
    wb = Workbook()
    ws = wb.active

    # Step 5: Initialize a list for storing the JSON data
    jason_list = []

    # Step 6: Iterate over each component to extract the data
    for component in components:
        # Find the number of claps
        num_claps = get_number_claps(component)
        
        # Find the title
        title = get_title(component)
        
        # Find the URL link
        link = get_url(component)
        
        # Add the data to the JSON list
        row = {"num_claps": num_claps, "title": title, "link": link}
        jason_list.append(row)
        
        # Add the data to the Excel sheet
        row_excel = [num_claps, title, link]
        ws.append(row_excel)
    
    # Step 7: Write the data to a JSON file
    with open(json_output_path, 'w') as json_file:
        json.dump(jason_list, json_file, indent=4)
    
    # Step 8: Save the Excel file
    wb.save(excel_output_path)
    print(f"Data saved to {json_output_path} and {excel_output_path}")

# Optional entry point for direct execution
# if __name__ == "__main__":
#     input_file = "to_scrape.html"
#     scrape_to_json_and_excel(input_file)
