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
from win10toast import ToastNotifier

def createcollegeboarddriver(username, password):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get("https://www.collegeboard.org/")
    time.sleep(3)

    driver.find_element_by_xpath('//*[@id="view10_username"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="view10_password"]').send_keys(password) # locates elements and sends keys
    driver.find_element_by_xpath('//*[@id="profile"]/div/div[5]/div/div[2]/div/div/div/div/div[1]/form/div[3]/div[2]/button').click()
    time.sleep(5) #needed because collegeboard takes a while to load

    try:
        driver.find_element_by_xpath('//*[@id="profile"]/div/div[5]/div/div/div[2]/div/div/div/div/div/ul/li[3]/a').click()
    except:
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="profile"]/div/div[5]/div/div/div[2]/div/div/div/div/div/ul/li[3]/a').click()

    print("LOG: Logging into College Board") 
    time.sleep(2)

    try: #there might be an additional security check
        driver.find_element_by_xpath('//*[@id="security"]').send_keys(password)
        driver.find_element_by_xpath('//*[@id="securityCheckForm"]/div/div/span/button').click()
        print("LOG: Additional log-in needed, and was successful")
    except:
        print("LOG: Additional log-in not needed")
    time.sleep(3)

    return driver


def parsetext(driver = webdriver):
    a=driver.find_elements_by_class_name("year-scores")
    links = [elem.get_attribute('outerHTML') for elem in a]
    links = str(links)
    soup = BeautifulSoup(links, features="html.parser")

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    return "".join(chunk for chunk in chunks if chunk).replace("\\n", "")


def checktext(text = str, courses = list):
    notifier = ToastNotifier()
    coursestoremove = []
    for ap in courses:
        score = re.search(f"{ap}Your score:(.+?)", text) #checks for the score
        if score == None:
            continue
        score = score[0][-1:]
        if score!="-":
            print(f"Your {ap} score is {score}")
            coursestoremove.append(ap)
            notifier.show_toast("ScrapeAP", f"Your {ap} grades are up, you got a {score}!")
    for c in coursestoremove:
        courses.remove(c)


def main():
    # parameters should be (username, password), both in string format
    a = input("Username: ")
    b = input("Password: ")
    driver = createcollegeboarddriver(a, b)

    listofclasses = ["English Language and Composition", "Calculus BC"] #list of classes to check

    #The actual comparing
    while(1):
        driver.refresh()
        text = parsetext(driver)
        checktext(text, listofclasses)
        if (len(listofclasses)==0):
            break
        print("LOG: Finished checking, time to sleep")
        time.sleep(0)

    driver.close()


main()