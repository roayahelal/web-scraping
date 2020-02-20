import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path':'/Users/roayahelal/Desktop/COLUMBIA UNIVERSITY/WEEK 12/12-Web-Scraping-and-Document-Databases/chromedriver'}
    return  Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {}

    # news scrape
    url_news = "https://mars.nasa.gov/news/"
    html_news = requests.get(url_news)
    html_news = html_news.text
    soup_news = bs(html_news, 'html.parser')

    mars_data["news_title"] = soup_news.find(class_="content_title").text.strip("\n")
    mars_data["news_peragraph"] = soup_news.find(class_="rollover_description_inner").text.strip("\n")

    # featured image scrape
    url_feature_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_feature_img)
    browser.click_link_by_partial_text("FULL IMAGE")
    browser.click_link_by_partial_text("more info")
    html_feature_img = browser.html
    soup_feature_img = bs(html_feature_img, 'html.parser')
    featured_img = soup_feature_img.select_one("figure.lede a img").get("src")
    mars_data["featured_img"] = 'https://www.jpl.nasa.gov' + featured_img
   
   # latest weather tweet scrape
    url_weather_tweet = 'https://twitter.com/MarsWxReport'
    html_weather_tweet = requests.get(url_weather_tweet)
    html_weather_tweet = html_weather_tweet.text
    soup_weather_tweet = bs(html_weather_tweet, 'html.parser')
    mars_data["weather_tweet"] = soup_weather_tweet.find('p', class_='tweet-text').text

    # facts table scrape
    mars_df = pd.read_html("https://space-facts.com/mars/")[0]
    mars_df.columns=["Description", "Value"]
    mars_data["facts_table"] = mars_df

    # hemisphere images scrape
    url_hemisphere_img = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemisphere_titles = ['Cerberus Hemisphere Enhanced',
    'Schiaparelli Hemisphere Enhanced',
    'Syrtis Major Hemisphere Enhanced',
    'Valles Marineris Hemisphere Enhanced']
    hemisphere = []
    for i in hemisphere_titles:
        browser.visit(url_hemisphere_img)
        browser.click_link_by_partial_text(i)
        html_hemisphere_img = browser.html
        soup_hemisphere_img = bs(html_hemisphere_img, 'html.parser')
        hemisphere_img = soup_hemisphere_img.select_one("img.wide-image").get("src")
        hemisphere_img_url = 'https://astrogeology.usgs.gov' + hemisphere_img
        hemisphere.append({"title": i,"img-url": hemisphere_img_url}) 
        mars_data["hemisphere"] = hemisphere
   

    return mars_data
