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
    driver.get("https://apscore.collegeboard.org/scores/#m=signin-form&scores")

    driver.find_element_by_xpath('//*[@id="inputUsername"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="inputPassword"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="signInForm"]/div[3]/div/div/button').click()
    time.sleep(5) #needed because collegeboard takes a while to load

    print("LOG: Logging into College Board") 

    try: #there might be an additional security check
        driver.find_element_by_xpath('//*[@id="security"]').send_keys(password)
        driver.find_element_by_xpath('//*[@id="securityCheckForm"]/div/div/span/button').click()
        print("LOG: Additional log-in needed, and was successful")
        time.sleep(3)
    except:
        print("LOG: Additional log-in not needed")

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

    listofclasses = ["English Language and Composition", "Calculus BC", "Computer Science A"] #list of classes to check

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