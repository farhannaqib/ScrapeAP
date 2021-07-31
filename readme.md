# scrapeAP

scrapeAP is a scraper to check 2021 AP Exam results for Administration 3. It uses your account to check for any updates along your scores.

Assuming the file is run uninterrupted throughout the day, this should send you a notification. You can check terminal to see what the scraper is doing at the moment.

## Requirements

In order to run, you should have Selenium, Beautiful Soup, and Webdriver Manager for Python installed, and have at least Python 3.8

## Usage

CollegeBoard usually updates scores during 12:30 AM EST from its original state as "--", or code 9.
Manually change the following for customization:

* line 83 to add classes you'd like to check
* line 93 to change how quickly the scraper checks your account

The scraper is most efficient when it checks every 2-5 minutes at around 12:30 AM EST, and every 30-60 minutes at any other time. If CollegeBoard is down for maintenence, the scraper will likely run into errors and you'll have to restart it. The scraper won't stop unless all the scores you asked for have an actual score or you stop it yourself. This scraper should work on other codes as well.

Cheers to the end of AP Season, cya next year!
