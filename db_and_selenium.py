import os
import pandas as pd
from selenium import webdriver
import sqlite3
import re

def csv_to_df(scrapy_csv, search_int):
    """
    given a path to csv from scrapy crawl,
    turns into data frame & filters by job title & date
    """

    df = pd.DataFrame.from_csv(scrapy_csv)
    dates = df['date'].tolist()

    dates_stripped = []
    for i in dates:
        repl = i.replace('Just posted', '1 day ago').replace('Today', '1 day ago').replace('+', '')
        sp = repl.split(' ')
        dates_stripped.append(sp[0])

    df['date'] = dates_stripped

    df['date'] = df['date'].astype(int)

    df1 =  df[df['date'] < int(search_int)].reset_index().sort_values(by='date')
    
    jobs = df1['name'].tolist()

    remove_jobs = []
    for i in jobs:
        lower = i.lower()
        if 'senior' in lower:
            remove_jobs.append(i)

    df2 = df1[~df1['name'].isin(remove_jobs)]#.set_index(keys=['url'])
    return df2.drop_duplicates()


def create_db_table(full_path_to_db):
    """
    create database table & names columns
    """

    conn = sqlite3.connect(full_path_to_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE indeed_jobs
        (id integer primary key, data, 
        job_title text,
        url text)''')

    conn.commit()
    conn.close()
    print('DB created at {}'.format(full_path_to_db))


def write_to_db(db_path, df):
    """
    turn data frame to dict & write urls & job titles to DB if not already there.
    returns urls not found in database but writes them there first.
    """

    df_dict = df.to_dict(orient='list')
    
    url = []
    name = []
    for k,v in df_dict.items():
        if k == 'url':
            url.extend(v)
        if k == 'name':
            name.extend(v)
   
    unique_urls = []
    count=  0
    for u, n in zip(url, name):
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute('SELECT * FROM indeed_jobs WHERE (url=? AND job_title=?)', (u, n))
        entry = c.fetchone()

        if entry is None:
            c.execute("insert or ignore into indeed_jobs (url, job_title) values (?, ?)", (u, n))
            conn.commit()
            unique_urls.append(u)
            count+=1
            print('\n{} || New Entry added\n{} - {}'.format(count, u, n))
        else:
            print ('\n>>>>>>>>>Entry found<<<<<<<<<\n', u, n)
            
    return unique_urls


def setup_webdriver(path_to_driver): 
    """
    set up webdriver
    """

    chromedriver = path_to_driver
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    return driver   


def show_jobs(driver_path, urls_lst):
    """
    given a list of unique urls, 
    opens each in a separate tab in the same browser window
    """
    
    driver = setup_webdriver(driver_path)
    
    for idx,i in enumerate(urls_lst):
        concatURL = 'window.open("' + i + '","_blank");'
        driver.execute_script(concatURL)
        print("Showing {} out of {}".format(idx, len(urls_lst)))
        if idx %10 == 0:
            input('Press enter to continue')
    input("If you press enter all your tabs will close.")
    input("So don't do it.")
    input("This time I'm serious.")


csv_path = input('\nEnter path to scrapy csv.\n> ')
db_path = input('\nEnter path to DB ending in sqlite.\n> ')
db_path_create = input('\nIs this a new db? y/n\n> ')
driver_path = input('\nEnter path to chromedriver.\n> ')
filter_days = input('\nHow many days back to check?\n> ')

if 'y' in db_path_create:
    create_db_table(db_path)
    df = csv_to_df(csv_path, filter_days)
    urls_lst = write_to_db(db_path, df)
    show_jobs(driver_path, urls_lst)
else:
    df = csv_to_df(csv_path, filter_days)
    urls_lst = write_to_db(db_path, df)
    show_jobs(driver_path, urls_lst)

    