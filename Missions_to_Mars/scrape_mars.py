from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import re
import requests
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    # Visit NASA
    nasa_url ="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(nasa_url)
    time.sleep(1)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    # Get the Mars News and Details
    content = soup.find('div', class_='content_title')
    news_title=content.find('a').get_text()
    news_p =soup.find('div',class_='article_teaser_body').get_text()


    jpl_url ="https://www.jpl.nasa.gov/spaceimages/details.php?id=PIA23656"
    browser.visit(jpl_url)
    final=jpl_url.split('/')
    final_url=final[0]+"//"+final[2]
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")  
    img_path_1=soup.find_all('figure',class_='lede')

    for img_path in img_path_1:
        img_url = img_path.find('a')['href']

    img_url_final=final_url+img_url


    twitter_url="https://twitter.com/marswxreport?lang=en"
    data=requests.get(twitter_url)

    time.sleep(1)

    soup = bs(data.text, "html.parser")

    tweet = soup.find('div',class_='js-tweet-text-container')
    weather_tweet=tweet.find('p',class_='TweetTextSize').get_text()
    weather_tweet_split=weather_tweet.split()
    len1 = len(weather_tweet_split)

    weather_tweet_split_new = ""
    for i in range(len1):
        if i == 0 or i==28:
            continue
        else:
            if i==1:
                weather_tweet_split_new=weather_tweet_split_new+" "+weather_tweet_split[i].capitalize()
            else:    
                weather_tweet_split_new = weather_tweet_split_new+" "+weather_tweet_split[i]

    mars_weather= weather_tweet_split_new+"hPa"       

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df=tables[0]
    mars_facts={}
    for column,value in df.values: 
        mars_facts[column]=value


    mars_url_list=["https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced",
              "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced",
              "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced",
              "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"]


    hemisphere_image_urls=[]
    dict1={}
    final=mars_url_list[0].split('/',-1)
    final_url=final[0]+"//"+final[2]


    for i in range(4):
        browser.visit(mars_url_list[i])

        time.sleep(1)

        html_i = browser.html
        soup_i = bs(html_i, "html.parser")

        title_search_i = soup_i.find('div',class_='content')
        title_i = title_search_i.find('h2',class_='title').get_text()

        image_loc_i=soup_i.find('div',id='wide-image')
        image_path_i=image_loc_i.find('img',class_='wide-image')['src']

        image_url_i=final_url+image_path_i
        dict_i={"title":title_i,"img_url":image_url_i}
        hemisphere_image_urls.append(dict_i)

    

    mars_data={
        "news_title": news_title,
         "news_para": news_p,
        "mars_image": img_url_final,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "mars_hemi": hemisphere_image_urls
        }



    # Close the browser after scraping
    browser.quit()   
    return mars_data