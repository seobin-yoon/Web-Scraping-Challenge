# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager



def scrape():
    Mars_News_data = Mars_News()
    Mars_Featured_Image_data = Mars_Featured_Image()
    Mars_Fact_data = Mars_Fact()
    Mars_Hemispheres_data = Mars_Hemispheres()

    mars_data = {**Mars_News_data, **Mars_Featured_Image_data, **Mars_Fact_data, **Mars_Hemispheres_data}

    return mars_ddata


def Mars_News():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    # Retrieve all elements that contain book information
    articles = soup.find_all('article', class_='product_pod')


    result = soup.find_all('div', class_='list_text')[0]

    news_title = result.find('div', class_='content_title').text.strip()
    news_p = result.find('div', class_='article_teaser_body').text.strip()

    try:
    browser.links.find_by_partial_text('next').click()


    except: 
    print("")
    

    Mars_News_data = {}
    Mars_News_data['news_title'] = news_title
    Mars_News_data['news_paragraph'] = news_paragraph



    return Mars_News_data


def Mars_Featured_Image():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    browser.links.find_by_partial_text('FULL IMAGE').click()

    html = browser.html
    soup = bs(html, 'html.parser')
    photo_url = soup.find("img", class_="headerimage fade-in")['src']

    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + photo_url

    Mars_Featured_Image_data = {}
    Mars_Featured_Image_data['featured_image_url'] = featured_image_url

    return Mars_Featured_Image_data



def Mars_Fact():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    soup = bs(browser.html, 'html.parser')
    tables = pd.read_html(url)

    mars_facts = tables[0]

    table_html = mars_facts.to_html(index=False, classes = "table table-striped")
    Mars_Fact_data= {'table_html': table_html}

return Mars_Fact_data



def Mars_Hemispheres():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    soup = bs(browser.html, 'html.parser')

    hemisphere_image_urls = []

    hemispheres = soup.find_all('div', class_='item')

    for hemisphere in hemispheres:
        
        hemisphere_url = {}
        
        title = hemisphere.find('div', class_='description').h3.text
        hemisphere_url['title'] = title

        browser.find_by_text(title).click()
    
        soup = bs(browser.html, 'html.parser')
        
        downloads = soup.find("div", class_='downloads')
        down_link = downloads.find('a')
        
        if down_link.text == 'Sample':
            img_url = soup.find("img", class_= "thumb")['src']
            hemisphere_url['img_url'] = 'https://astrogeology.usgs.gov' + img_url
 
        hemisphere_image_urls.append(hemisphere_url)
    
        browser.back()

    Mars_Hemispheres_data = {}
    Mars_Hemispheres_data['image_url'] = hemisphere_image_urls
    
    return Mars_Hemispheres_data   