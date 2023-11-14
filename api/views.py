from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from rest_framework.response import Response
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as e
import os
import time
from datetime import date
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re

from pytrends.request import TrendReq

class prod(APIView):
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


    def get_reviews(self, sorted_prod):
      reviews=[]
      for i in sorted_prod:
        productid=i[4]
        self.get_review_url(product_id)
        reviews = []
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        listr = soup.find_all('div', {'class': 'user-review-reviewTextWrapper'})
        for review in listr:
            review_text = review.text.strip()
            reviews.append(review_text)
        return reviews
      
     
  

    def summary(self,text):
      
        nlp = spacy.load('en_core_web_sm')
        doc= nlp(e)
        per=0.5
        tokens=[token.text for token in doc]
        word_frequencies={}
        for word in doc:
            if word.text.lower() not in list(STOP_WORDS):
                if word.text.lower() not in punctuation:
                    if word.text not in word_frequencies.keys():
                        word_frequencies[word.text] = 1
                    else:
                        word_frequencies[word.text] += 1
        max_frequency=max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word]=word_frequencies[word]/max_frequency
        sentence_tokens= [sent for sent in doc.sents]
        sentence_scores = {}
        for sent in sentence_tokens:
            for word in sent:
                if word.text.lower() in word_frequencies.keys():
                    if sent not in sentence_scores.keys():                            
                        sentence_scores[sent]=word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent]+=word_frequencies[word.text.lower()]
        select_length=int(len(sentence_tokens)*per)
        summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
        final_summary=[word.text for word in summary]
        summary=''.join(final_summary)
        
    def sortprod(self,record,text):
        f=e()
        l=record
        
        te=text.split()
        c=0
        data=[]
        for i in l:
            for j in range(0,len(i)):
                t=l[3].split()
                for  ff in te:
                    if ff in t:
                        data+=[i]
                        if len(data)==5:
                            break
        return data
    def sortreviews(self,data):
        f=e()
        for i in data:
          if f.polarity_scores(i[2])['compound']<0:
            e+=i[2]
    def get(self,request,format=None):
      return Response("hi")
  

    def post(self,request,format=None):
        product=request.data["productname"]
        productn=self.get_category_url(product)
        wp_info = self.extract_webpage_information()
        records = self.extract_product_information(wp_info)
        similar=self.sortprod(records,product)
        reviews=self.get_reviews(similar)
        suma=self.sortreviews(reviews)
        gov={}
        gov["summary"]=suma
        gov["data"]=similar
        return Response(gov)


class comp(APIView):
    def post(self,request,format=None):
        nlp=spacy.load("en_core_web_Ig")
        doc="i love you"
        doc2="l like you"
        return Response(doc.similaririty(doc2))
        
     

