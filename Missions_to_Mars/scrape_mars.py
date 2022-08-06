#Dependencies
from cgitb import html
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
from selenium import webdriver

def scrape():

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Nasa Mars news
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)

    news_html = browser.html
    news_soup = bs(news_html, 'html.parser')

    results = news_soup.find_all('div', class_ = 'col-md-8')

    for result in results:
        try:
            news_title = result.find('div', class_='content_title').text
            news_para = result.find('div', class_='article_teaser_body').text
        except AttributeError as e:
            print(e)

    # JPL Mars Space Images - Featured Image
    fimg_url = 'https://spaceimages-mars.com/'
    browser.visit(fimg_url)
    fimg_html = browser.html
    fimg_soup = bs(fimg_html,"html.parser")

    results = fimg_soup.find_all('div', class_ = 'floating_text_area')
    for result in results:
        try:
            url = result.a['href']
        except AttributeError as e:
            print(e)
    featured_image_url = fimg_url + url

    
    # Mars facts
    mf_url = 'https://galaxyfacts-mars.com'
    tables = pd.read_html(mf_url)
    mf_df = tables[0]
    mf_df = mf_df.iloc[1: , :]
    mf_df.columns = ['Description', 'Mars', 'Earth']
    mf_df = mf_df.to_html()


    # Mars Hemispheres
    mh_url = 'https://marshemispheres.com'
    browser.visit(mh_url)  

    hemisphere_image_urls = []

    for i in range(1,5):

        x_path = '//*[@id="product-section"]/div[2]/div['+ str(i) + ']/div/a/h3'
        browser.find_by_xpath(x_path).click()

        img_url = browser.find_by_xpath('//*[@id="wide-image"]/div/ul/li[1]/a') ['href']
        title = browser.find_by_xpath('//*[@id="results"]/div[1]/div/div[3]/h2').text
        title = title[0:-9]
        hem_dict = {"title": title , "img_url": img_url}       
        hemisphere_image_urls.append(hem_dict)
            
        browser.back()
  

    mars_data = []

    mars_data ={
		'news_title' : news_title,
		'news_para': news_para,
        'featured_image_url': featured_image_url,
		'mf_df': mf_df,
		'hemisphere_image_urls': hemisphere_image_urls,
        'news_url': news_url,
        'fimg_url': fimg_url,
        'mf_url': mf_url,
        'mh_url': mh_url,
        }

    # Close the browser after scraping
    browser.quit()
    return mars_data


