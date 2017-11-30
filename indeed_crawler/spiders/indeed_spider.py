from bs4 import BeautifulSoup
import os
import requests
import scrapy
from time import sleep
import urllib.request

# run this to save to csv => scrapy crawl indeed -t csv -o file.csv
class QuotesSpider(scrapy.Spider):

    name = "indeed"

    # paste urls list produced from concat_scarper_urls.py here
    start_urls = ['https://www.indeed.com/jobs?q=react+developer&l=NEW+YORK%2C+NY&sort=date&start=10', 'https://www.indeed.com/jobs?q=react+developer&l=NEW+YORK%2C+NY&sort=date&start=20', 'https://www.indeed.com/jobs?q=python+developer&l=NEW+YORK%2C+NY&sort=date&start=10', 'https://www.indeed.com/jobs?q=python+developer&l=NEW+YORK%2C+NY&sort=date&start=20', 'https://www.indeed.com/jobs?q=java+developer&l=NEW+YORK%2C+NY&sort=date&start=10', 'https://www.indeed.com/jobs?q=java+developer&l=NEW+YORK%2C+NY&sort=date&start=20']

    def parse(self, response):

        job_urls = response.xpath('//*[contains(@class, "jobtitle")]//a/@href').extract()
        job_name = response.xpath('//*[contains(@class, "jobtitle")]//a/@title').extract()
        job_companies = response.xpath('//*[contains(@class, "  row  result")]//*[contains(@class, "company")]//text()').extract()
        job_companies[:] = [i.strip() for i in job_companies if len(i) != 5]

        # scrape job dates with bs4
        current_url = response.request.url
        r = requests.get(current_url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"})
        soup = BeautifulSoup(r.content, "html5lib")
        date = [i.get_text() for i in soup.find_all('span', {'class': 'date'})]

        # show data in terminal 
        for idx, u in enumerate(zip(job_urls,job_name, job_companies, date)):
            url = 'https://www.indeed.com' + u[0]
            scraped_info  = {}
            scraped_info["url"] = url
            scraped_info["name"] = u[1]
            scraped_info["company"] = u[2]
            scraped_info["date"] = u[3]
            yield scraped_info

        print('\n\n\n\n\n{}\n\n\n\n\n'.format(response.url))