from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests
import urllib.request
import re
from html.parser import HTMLParser
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

global i
i=1

def dostuff():
    global i
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get("https://www.collegeboard.org/")
    time.sleep(3)

#enter username and password here
    username=""
    password=""

    driver.find_element_by_xpath('//*[@id="view10_username"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="view10_password"]').send_keys(password) # locates elements and sends keys
    driver.find_element_by_xpath('//*[@id="profile"]/div/div[5]/div/div[2]/div/div/div/div/div[1]/form/div[3]/div[2]/button').click()

    time.sleep(5) #needed because collegeboard takes a while to load

    try:
        driver.find_element_by_xpath('//*[@id="profile"]/div/div[5]/div/div/div[2]/div/div/div/div/div/ul/li[3]/a').click()
    except:
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="profile"]/div/div[5]/div/div/div[2]/div/div/div/div/div/ul/li[3]/a').click()

    print("got past this part 1")
    #there might be an additional security check

    time.sleep(2)

    try:
        driver.find_element_by_xpath('//*[@id="security"]').send_keys(password)
        driver.find_element_by_xpath('//*[@id="securityCheckForm"]/div/div/span/button').click()
    except:
        print("That step wasn't needed")

    time.sleep(3)

    print("got here 2")

    a=driver.find_elements_by_class_name("year-scores")
    links = [elem.get_attribute('outerHTML') for elem in a]
    links=str(links)
    #print(links)
    soup = BeautifulSoup(links, features="html.parser")

        # get text
    text = soup.get_text()

        # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text=str(text)
    text = text.replace('\n','')

    print(text)
    #this is the part you need to change to generalize it, I reccomend iterating through the first time and saving it to historyvar, then reiterating to text
    historyvar=['\n\n2021\n\n\n\nAwards:\n\nAP Scholar\n\n\n\n\nPrint your award certificate(s) (Opens a\nnew window)\n\n\n\n\n\n\n\n\n\n\n\n\n\nEnglish Language and Composition\n\n\n\n\nYour score:\n--\n\n\n\n\nScore delayed - will be reported as soon as possible (code 9)\n\n\n\n\n\n\n\nAbout your score\n\n\nUnderstanding your score\n\n\n\n\n\n\n\n\n\nPhysics 1\n\n\n\n\nYour score:\n4\n\n\n\n\n\n\n\n\n\nAbout your score\n\n\nUnderstanding your score\n\n\n\n\n\n\n\n', '\n\n2020\n\n\n\n\n\n\n\n\n\n\n\nWorld History: Modern\n\n\n\n\nYour score:\n4\n\n\n\n\n\n\n\n\n\nAbout your score\n\n\nUnderstanding your score\n\n\n\n\n\n\n\n']

    historyvar=str(historyvar)

    print(historyvar)

    if text != historyvar:
        i=2
        print("oh shit")
        text=str(text)
        m = re.search("English Language and Composition\n\n\n\n\nYour score:\n(.+?)\n", text) #you will also need to change this to capture all AP scores, not just for Lang
        print(m)
        if m=="5":
            print("lets fucking GOOOOOOOOOOOOOO")
        if m=="4":
            print("nice homie")
        if m=="--":
            print("codes broken or apush\psych is up")
        else:
            print("get wrecked")
    else:
        print("its all good homie")

    driver.close()


while i==1:
    dostuff()
    print("sleeping for an hour now")
    time.sleep(60*60)
