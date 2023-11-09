
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_parking_availability():
    print('parking availability')

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome("/chromedriver", options=chrome_options)
    url = "https://parkingavailability.charlotte.edu/"
    
    driver.get(url)
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    allTags = soup.find_all('app-list-item')

    parkingDecks = []

    for tag in allTags:
        deckInfo = {}
        percentTag = tag.find('app-percentage')
        percent = percentTag.find('div')
        text = percent.text.strip()
        deckInfo['percent'] = text
        deckInfo['percent_number'] = text.replace('%', '')

        deck = tag.find('span', class_='deck-name')
        deckInfo['name'] = deck.text.strip()
        parkingDecks.append(deckInfo)
        
    driver.quit()

    return parkingDecks