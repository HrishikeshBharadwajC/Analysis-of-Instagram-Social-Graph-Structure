from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import json

class InstagramCrawler:
    BASE_URL = 'https://www.instagram.com/explore/locations/'

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def open_location(self, id):
        self.driver.get(self.BASE_URL+str(id)+'/media/')

        # wait for the login page to load
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]/section/')))

        location = self.driver.find_element_by_css_selector('main > article > header > div > h1').text
        posts = []
        for i in range(1,4):
            for j in range(1,4):
                try:
                    href = self.driver.find_element_by_css_selector('div > div > div > div:nth-child('+str(i)+') > div:nth-child('+str(j)+') > a').get_attribute("href")
                    # print('link:',href)
                    posts.append(href)
                except:
                    pass
        
        hashtags = []
        hashtags_list = []
        for post in posts:
            h = self.get_hashtags(post)
            if h:
                hashtags.append(h)
                hashtags_list += h['hashtags']

        print('Location ID:',id)
        print('Location:',location)
        print('Hashtags:',hashtags)

        obj = {}
        obj['location'] = location
        obj['hashtags'] = hashtags
        obj['hashtags_all'] = hashtags_list

        obj1 = {}
        with open('location_data.txt') as file:
            obj1 = json.load(file) # use `json.load` to do the reverse
        obj1[id] = obj

        with open('location_data.txt', 'w') as file:
            file.write(json.dumps(obj1)) # use `json.loads` to do the reverse
        

    def get_hashtags(self, link):
        # navigate to "post" page
        self.driver.get(link)
        # wait for the main page to load
        # time.sleep(1)

        try:
            e = self.driver.find_elements_by_css_selector('div > div > article > div > div > ul > li:nth-child(1) > div > div > div > span > a')
            e += self.driver.find_elements_by_css_selector('div > div > article > div > div > ul > li:nth-child(2) > div > div > div > span > a')
            e += self.driver.find_elements_by_css_selector('div > div > article > div > div > ul > li:nth-child(3) > div > div > div > span > a')
        except:
            pass

        hashtags = []

        for a in e:
            print
            if a.text.find("#")>=0:
                hashtags.append(a.text)
       
        timestamp = ''
        try:
            timestamp = self.driver.find_element_by_css_selector('div > div > article > div > div > a > time').get_attribute("datetime")
        except:
            pass
        obj = {}
        obj['time']=timestamp
        obj['hashtags']=hashtags

        return obj


if __name__ == '__main__':
    crawler = InstagramCrawler() 

    f = open('insta_loc_id.txt')
    lines = f.readlines()
    for line in lines:
        locid = line.strip()
        crawler.open_location(id=locid)