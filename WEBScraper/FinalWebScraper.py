from bs4 import BeautifulSoup
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.models import Word2Vec
from fpdf import FPDF
import webbrowser
import os

alreadyScraped = []

#---
#Key, ID, Files
#---
API_KEY = 'AIzaSyDzkZTYROdh9D-XvXNPzEab6HSQVCoAgAE'
SEARCH_ENGINE_ID = 'c5cb037ffe16c4fc0'
dataFile = open('dataTextFile', 'w')
scrapedImportantData = open('scrapedData', 'w')

#---
#Web Scraper
#---
def webScrape(user_search):
    dataFile = open('dataTextFile', 'a')
    search_query = user_search
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'q': search_query,
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID
    }

    response = requests.get(url, params=params)
    results = response.json()

    #print(results)
    if 'items' in results:
        url = results['items'][siteNum]['link']
        if (url in alreadyScraped):
            return
        print(url)
        alreadyScraped.append(url)

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    for data in soup.find_all('p')[0:100]:
        try:
            dataFile.write(data.text+"\n")
        except:
            continue


continSearch = True
siteNum = 0

#---
#Operation
#---
while continSearch:
    dataFile = open('dataTextFile', 'w')
    user_search = input("What information would you like to search for? ")
    for x in range(5):
        webScrape(user_search)
        siteNum+=1
    dataFile = open('dataTextFile', 'a')
    print(alreadyScraped)
    dataFile.write("\n\nSources\n")
    for x in alreadyScraped:
        dataFile.write(x+"\n")

    #---
    #Text Important Word Screening
    #---
    dataFile = open('dataTextFile', 'r')
    nltk.download("punkt")
    nltk.download("stopwords")

    def preprocess_text(text):
        sentences = sent_tokenize(text)
        stop_words = set(stopwords.words("english"))

        words = [word_tokenize(sentence.lower()) for sentence in sentences]
        words = [[word for word in sentence if word.isalnum() and word not in stop_words] for sentence in words]

        return sentences, words

    sentences, words = preprocess_text(dataFile.read())
    print(sentences)
    print(words)
    dataFile.close()
    
    #---
    #Putting Important Data In File
    #---
    scrapedImportantData = open('scrapedData', 'w')
    scrapedImportantData = open('scrapedData', 'a')
    for x in sentences:
        try:
            scrapedImportantData.write(x+"\n")
        except:
            continue
    
    scrapedImportantData.write("\nRelates Words:\n")
    for x in words:
        try:
            scrapedImportantData.write("[")
            for i in x:
                try:
                    scrapedImportantData.write(i+", ")
                except: 
                    continue
            scrapedImportantData.write("]\n")
        except:
            continue
    
    #---
    #PDF Converter
    #---
    newPDF = None
    def convert_file(file):
        pdf = FPDF()
        pdf.add_page()

        for text in file:
            try:
                if len(text) <= 20:
                    pdf.set_font("Arial","B",size=18)
                    pdf.add_font('Arial', '', 'c:/windows/fonts/arial.ttf', uni=True) 
                    pdf.cell(w=200,h=10,txt=text,ln=1,align="C")
                else:
                    pdf.set_font("Arial",size=15)
                    pdf.add_font('Arial', '', 'c:/windows/fonts/arial.ttf', uni=True) 
                    pdf.multi_cell(w=0,h=10,txt=text,align="L")
            except:
                continue
        os.remove("output.pdf")
        newPDF = pdf.output("output.pdf")
        print('Successfully converted!')
        
    scrapedImportantData = open('scrapedData', 'r')
    convert_file(scrapedImportantData)
    scrapedImportantData.close()
    webbrowser.open("output.pdf")

    #---
    #Ask another question
    #---
    stop = input("Would you like to search more? y or n? ")
    if(stop == 'y'): 
        alreadyScraped = []
        siteNum = 0
        continue 
    else: break