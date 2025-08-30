from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
import openpyxl

def initialize_driver():
    # Configure headless Chrome
    chrome_options = Options()
    #chrome_options.add_argument("--headless=new")  # New headless mode in Chrome 109+
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--lang=en-US")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    return driver

def scrape_twitter_comments(tweet_url, driver):
    driver.get(tweet_url)
    
    # Wait for the page to load
    time.sleep(5)  # Adjust delay if needed
    
    try:
        twit = driver.find_element(By.CLASS_NAME, 'css-175oi2r').text
                    
    except Exception as e:
        print(f"Error: {e}")
    
    return twit
    
def Clean_Twit(text):
    #trim_left = text.find("Conversation") + 13
    #text2 = text[trim_left:]
    
    #author_position = text2.find("@") - 1
    #author = text2[:author_position] #return

    #text3 = text2[author_position + 1 :]
    #linebreak = text3.find("\n")

    #text4 = text3[linebreak + 1 :]
    year = ", 2025" if text.find(", 2025") != -1 else ", 2024"
    date = text[text.find(year) - 6 : text.find(year) + 6]
    
    #time = " am " if text.find(" am ") != -1 else " pm "
    twit = text[text.find("Conversation") + 13 : text.find(date) - 10].lower().replace("\n", "").replace("translate post", "") #return
    #twit = text4[text4.find("Follow") + 5 :text4.find("Translate post") - 1].lower().replace("\n", "") #return

    #text5 = text4[len(twit):]
    #text6 = text5[text5.find("·") + 2:]
    
    #date = text6[:text6.find("·") - 1] #return

    #text7 = text6[text6.find("Views") + 5: text6.find("Read")] 
    #text8 = text7[1:]
    #comments = int(text8[:text8.find("\n")]) #return

    #text9 = text8[text8.find("\n"):]
    #text10 = text9[1:]
    #rt = int(text10[:text10.find("\n")]) #return
    
    #text11 = text10[text10.find("\n"):]
    #text12 = text11[1:]
    #likes = int(text12[:text12.find("\n")]) #return

    red_social = "Twitter/X"
    
    return twit, date, red_social

def get_links(link_path):
    links_df = pd.read_excel(link_path)
    length1 = len(links_df)
    links_df.drop_duplicates(subset=['Links'], keep='first', inplace=True)
    length2 = len(links_df)
    print(f"Removed {length1 - length2} duplicate links")
    links = links_df['Links'].tolist()
    status = links_df['Status'].tolist()
    return links, status

def generate_status_id(status, parent_count, child_count):
    if status == 1:
        stat_id = f"P-0{parent_count}"
    elif status == 0:
        stat_id = f"Ch-0{child_count}"
    return stat_id

def scrape_twitter(links, status, count):
    twits = []
    fechas = []
    plataformas = []
    links_scraped = []
    status_id = []
    status_id_parent = []
    parent_id = ""
    driver = None  # Initialize driver variable outside the loop
    driver_count = 0

    if count == 0:
        child_count = 1
        parent_count = 1

    for link in links:
        if count == 0:
            driver = initialize_driver()  # Initialize driver
        
        count += 1
        if count == 30:
            driver.quit()  # Close the driver after 40 iterations
            driver = initialize_driver()
            count = 1
            driver_count += 1
            print(f"Driver restarted after {30 * driver_count} iterations")

        try:
            twit = scrape_twitter_comments(link, driver=driver)
            twit, fecha, red_social = Clean_Twit(twit)
            stat_id = generate_status_id(status[links.index(link)], parent_count, child_count)

            if "P" in stat_id:
                parent_count += 1
                parent_id = stat_id
                stat_id_parent = parent_id
                twit_parent = twit
            else:
                child_count += 1
                stat_id_parent = parent_id
                if twit_parent in twit:
                    twit = twit.replace(twit_parent, "")
                
        except Exception as e:
            id = links.index(link)
            print(f"Error scraping ID: {id} --- {e}")
            continue

        #print(f"Scraped ID: {links.index(link)}")
        #print(link)

        twits.append(twit)
        fechas.append(fecha)
        plataformas.append(red_social)
        links_scraped.append(link)
        status_id.append(stat_id)
        status_id_parent.append(stat_id_parent)

    # Close the driver after all iterations are done
    if driver is not None:
        driver.quit()
        
    return twits, fechas, plataformas, links_scraped, status_id, status_id_parent