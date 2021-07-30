# scrapeAP

scrapeAP is a scraper to check CollegeBoard scores as scores get updated as 2021 Admin 3 AP Exam results come out. It uses your account to check for any updates along your scores.

Assuming the file is being ran uninterrupted throughout the day, this should send you a notification. You can check terminal to see what the scraper is doing at the moment.

## Requirements

In order to run, you should have Selenium, Beautiful Soup, and Webdriver Manager for Python installed, and have at least Python 3.8

## Usage

CollegeBoard usually updates scores during 12:30 AM EST from its original state as "--", or code 9.
Manually change the following for customization:

* line 82 to add your CollegeBoard username and password
* line 85 to add classes you'd like to check
* line 95 to change how quickly the scraper checks your account

The scraper is most efficient when it checks every 2-5 minutes at around 12:30 AM EST, and every 30-60 minutes at any other time. If CollegeBoard is down for maintenence, the scraper will run into errors and you'll have to restart it. The scraper won't stop unless all the scores you asked for go from code 9 to an actual score or you stop it yourself. This scraper should work on other codes as well.

Note that this only checks for classes that you add in line 95 in case for some reason the site changes but your score doesn't get added.

Cheers to the end of AP Season, cya next year!
