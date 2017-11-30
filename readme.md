how to use this thing & what it is: 

1) download webdriver 
	> https://sites.google.com/a/chromium.org/chromedriver/downloads

	> note the full path of where it's installed to 


2) install all dependencies
	> pip3 install beautifulsoup4 selenium requests pandas 


3) concatenate urls to crawl on indeed.com for multiple job titles & how many pages for each job title 
    > cd ./indeed_crawler

    > python3 concat_scraper_urls.py

    > follow prompts & copy script output to empty file


4) run scrapy crawler & save output to csv
    > cd ./indeed_crawler/indeed_crawler/spiders

    > open indeed_spider.py in text editor

    > copy urls from step 3 into start_urls variable & save 

    > scrapy crawl indeed -t csv -o file.csv


5) filter job urls that were crawled by date and by word(s) in job title, remove duplicates, check against database, & show urls 
   in a new tab in the same chromedriver window 
    > cd ./indeed_crawler

    > python3 db_and_selenium_urls.py

    > need webdriver path (e.g. /Users/Anthony/Desktop/chromedriver)

    > need sqlite DB path (e.g. /Users/Anthony/Desktop/python_projects/databases/test_db.sqlite)