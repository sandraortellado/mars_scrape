# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd
from splinter import Browser
import time


def scrape():
    url = 'https://mars.nasa.gov/news/'
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    time.sleep(3)
    browser.find_by_xpath('//div[@class="content_title"][1]').click()

    url=browser.url
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')

    results=soup.find('h1','article_title')
    news_title = results.text.strip()
    results = soup.find_all('p')
    news_lede=results[1].text[1:]
    news_lede



    # executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    # browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('article', class_='carousel_item')['style']


    featured_image_url = 'https://www.jpl.nasa.gov' + img[23:75]


    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')

    results = soup.find('p',class_='js-tweet-text')
    mars_weather = results.text


    res = requests.get("https://space-facts.com/mars/")
    soup = BeautifulSoup(res.content,'html')
    table = soup.find_all('table')[0] 
    df = pd.read_html(str(table))
    df = df[0]
    df = df.rename(index=str, columns={0: '', 1: ""})
    facts_table_html = df.to_html()
    facts_table_html = BeautifulSoup(facts_table_html, 'html.parser')
    facts_table_html = facts_table_html.prettify()



    # executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    # browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.find_all('h3')
    pages=[]
    items=soup.find_all('div',class_='item')
    [pages.append(item.find('a')['href']) for item in items] 
    titles=[title.text for title in titles]
    img_urls=[]


    for page in pages:
        url = 'https://astrogeology.usgs.gov'+page
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find('a',target='_blank')['href']
        img_urls.append(img_url)


    hemisphere_image_urls = []
    entry={}
    for i in range(len(img_urls)):
        entry['title']=titles[i]
        entry['img_url']=img_urls[i]
        hemisphere_image_urls.append(entry)
        entry={}
    browser.quit()

    final_dict={
        'news title':news_title,
        'news lede':news_lede,
        'featured image url':featured_image_url,
        'mars weather tweet':mars_weather,
        'facts table (html)':facts_table_html,
        'hemisphere image urls':hemisphere_image_urls

    }
    return final_dict






