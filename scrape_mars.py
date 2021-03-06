#Dependencies
from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import os
import pandas as pd
import time as tm

def init_browser():
    executable_path = {"executable_path": "c:/Users/Aaron/chromedriver_win32/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless = False)
    

def scrape():
    browser = init_browser()
    mars_facts = {}

    nasa = "https://mars.nasa.gov/news/"
    browser.visit(nasa)

    

    html = browser.html
    bsoup = bs(html,"html.parser")

    #Scrape newest news
    news_title = bsoup.find("div",class_="content_title").text
    news_paragraph = bsoup.find("div", class_="article_teaser_body").text

    # Store data
    mars_facts['news_title'] = news_title
    mars_facts['news_paragraph'] = news_paragraph 
    
    ### Image
    #Define URL
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    #Visit URL 
    browser.visit(url_image)
    

    #Get HTML codes 
    html_image = browser.html
    #Parse codes
    bsoup = bs(html_image, "html.parser")
    #Find image url
    featured_image_url  = bsoup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    #Define url
    base_url = 'https://www.jpl.nasa.gov'
    #Combine two urls 
    full_img_url = base_url + featured_image_url

    # Store Data
    mars_facts["featured_image"] = full_img_url
    
    ### Weather

    #Find latest tweet 
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html_weather = browser.html

    # Parse HTML
    bsoup = bs(html_weather, 'html.parser')

    # Find elements with tweets
    latest_tweets = bsoup.find_all('div', class_='js-tweet-text-container')
    # Loop through
    for tweets in latest_tweets: 
        weather_tweet = tweets.find('p').text
        if 'Sol' and 'hPa' in weather_tweet:
            print(weather_tweet)
            break
        else: 
            pass
    
    # Store Data
    mars_facts["mars_weather"] = weather_tweet

    ### Facts

    url_facts = "https://space-facts.com/mars/"
    
    table = pd.read_html(url_facts)
    table[0]

    mars_df = table[0]
    mars_df.columns = ["Parameter", "Values"]
    clean_table = mars_df.set_index(["Parameter"])
    mars_table = clean_table.to_html()
    mars_table = mars_table.replace("\n", "")

    # Store Data
    mars_facts["mars_facts_table"] = mars_table

    ### Hemisperes

    return mars_facts