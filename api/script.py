import os
import time
from datetime import date
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re


class MyntraProductScraper:
    def __init__(self):
        self.driver = None
        self.category_name = None
        self.formatted_category_name = None

    def open_browser(self):

        opt = Options()

        opt.add_argument("--disable-infobars")
        opt.add_argument('--log-level=OFF')
        opt.add_experimental_option('excludeSwitches', ['enable-logging'])

        url = "https://www.myntra.com"
        self.driver = webdriver.Firefox()
        # Website URL
        self.driver.get(url)

        # Wait till the page has been loaded
        time.sleep(3)
    def get_category_url(self, searchQuery):

        # This is the product url format for all products
        category_url = "https://www.myntra.com/{}?rawQuery={}"

        category_url = category_url.format(searchQuery,searchQuery)

        print(">> Category URL: ", category_url)

        # Go to the product webpage
        self.driver.get(category_url)
        # To be used later while navigating to different pages
        return category_url


    def get_review_url(self, product_id):


        # This is the product url format for all products
        review_url = "https://www.myntra.com/reviews/{}"

        review_url = review_url.format(product_id)

        print(">> Category URL: ", review_url)

        # Go to the product webpage
        self.driver.get(review_url)
        # To be used later while navigating to different pages
        return review_url
    
    

    def extract_webpage_information(self):
        # Parsing through the webpage
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        # List of all the html information related to the product
        page_results = soup.find_all('li', {'class': 'product-base'})
        return page_results

    


    @staticmethod
    def extract_product_information(page_results):
        records = []

        for i in range(len(page_results)):
            item = page_results[i]

            producer = item.h3.text
            description = item.h4.text

            try:

                product_url = item.a['href']
                reg = re.findall(r'\d+', product_url)
                product_id = list(map(int, reg))

                product_price_txt = item.find('span', {'class':'product-strike'}).text.strip()
                product_price_ls = [int(word) for word in product_price_txt.split() if word.isdigit()]
                product_price = product_price_ls[0]
                
                product_information = [producer, description, product_price, product_url, product_id[0]]
                records.append(product_information)
            except:
                continue
        return records


    def get_reviews(self, product_id):
        self.get_review_url(product_id)
        reviews = []
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        listr = soup.find_all('div', {'class': 'user-review-reviewTextWrapper'})
        for review in listr:
            review_text = review.text.strip()
            reviews.append(review_text)
        return reviews



        
        
        


    
    
if __name__ == "__main__":
    myntra_bot = MyntraProductScraper()

    myntra_bot.open_browser()

    category_details = myntra_bot.get_category_url('oversized t shirts')
    wp_info = myntra_bot.extract_webpage_information()
    records = myntra_bot.extract_product_information(wp_info)
    print(records)

