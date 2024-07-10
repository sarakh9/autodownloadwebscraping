from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import pandas as pd


# Initialize WebDriver
try:
    # installing chrome webdriver
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    # getting the url
    url = "https://data.gov.au/dataset/ds-dga-f1a2c3d5-98d0-46b7-8b8c-742e65c6afa7/details?q="
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # clean download links
    download_tags = soup.find_all("a", {"class": "download-button"})
    download_links = []
    
    for tag in download_tags:
        download_links.append(tag['href'])
        
    download_list = []

    for link in download_links:
        if link[-5:] == ".xlsx":
            download_list.append(link)

    test = download_links[0]
    file_name = test.split('/')[-1]

    # downloading excel file
    response = requests.get(test)

    # saving excel file
    with open(file_name, 'wb') as f:
        f.write(response.content)
    # pd.read_excel(file_name)


except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
