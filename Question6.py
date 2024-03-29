import requests 
from threading import Thread 
import time
import re
import os


from models import Apartment

class Scraping:
    def __init__(self, targetURL) -> None:
        self.targetURL = targetURL
        self.apartments = list()

    def get_advertisement(self):
        try:
            siteInfo = requests.get(self.targetURL, timeout=10)
            siteInfo.raise_for_status()
            return siteInfo
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def extraction_advertisement(self, htmlContent):
        title_pattern = re.compile(r'<h2 class="kt-post-card__title">([^<]+)<\/h2>')
        price_pattern = re.compile(r'<div class="kt-post-card__description">([^<]+)<\/div>')
        link_pattern = re.compile(r'<a class="" href="([^"]+)">')

        title_matches = title_pattern.finditer(htmlContent)
        price_mathces = price_pattern.finditer(htmlContent)
        link_matches = link_pattern.finditer(htmlContent)

        for title_match, price_match, link_match in zip(title_matches, price_mathces, link_matches):
           self.add_apartment(title_match.group(1), price_match.group(1),"https://divar.ir"+ link_match.group(1))
            

    def add_apartment(self, title, price, link):
        newApartment = Apartment(title, price, link)  
        self.apartments.append(newApartment) 

    def save_to_file(self, filePath):
        try:
            self.delete_file(filePath)
            with open(filePath, 'a', encoding='utf-8') as file:
                if self.apartments:  # Check if the list is not empty
                    for ad in self.apartments:
                        file.write(f"Title: {ad.title}\nPrice: {ad.price}\nLink: {ad.link}\n\n")
                    self.apartments = []  # Clear the list after saving
                else:
                    print("No ads found.")
        except IOError as e:
            print(f"Error: {e}")
    def delete_file(self,filePath):
        if os.path.exists(filePath):
            os.remove(filePath)


def scrape_divar(targetURL, filePath):
    print("Starting Scrape Your Site")
    divar = Scraping(targetURL=targetURL)
    siteInfo = divar.get_advertisement()

    if siteInfo and siteInfo.status_code == 200:
        divar.extraction_advertisement(siteInfo.text)
        divar.save_to_file(filePath)
    else:
        print("Failed to retrieve HTML content.")

if __name__ == "__main__":
    targetURL = "https://divar.ir/s/tehran/buy-residential"
    filePath = "ScrapDivar.txt"

    while True:
        ThreadReceiveNewAdvertisement = Thread(target=scrape_divar, args=(targetURL, filePath))
        ThreadReceiveNewAdvertisement.start()
        time.sleep(1800)  
