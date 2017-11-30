def concat_url(job_title): 
    """
    concatenate indeed.com search urls for specifc 2 or 3 letter job titles
    """

    location = 'new york ny'
    
    location_upper = location.upper()
    base_url = 'https://www.indeed.com/jobs?q'
    # no comma in city 
    job = job_title.split(' ')
    loc = location_upper.split(' ')
    if len(job) == 2:
        return '{}={}+{}&l={}+{}%2C+{}&sort=date'.format(base_url, job[0], job[1], loc[0], loc[1], loc[2])
    if len(job) == 3:
        return '{}={}+{}+{}&l={}+{}%2C+{}&sort=date'.format(base_url, job[0], job[1],job[2], loc[0], loc[1], loc[2])

def add_page_num(url, int_pages):
    """
    append the page number (&start=10 => 1st page) to indeed.com search url
    """


    num_pages_lst = [x*10 for x in range(0, (1+1 * int(int_pages)))][1:]
    return [url+'&start='+str(x) for x in num_pages_lst]
 
# inputs    
num = input('Enter number of different job titles to search as integer.\n> ')
int_pages = input('Enter number of pages to search as integer.\n> ')

job_lst = []
for x in range(int(num)):
    job_title = input('Enter space delimited job title at least 2  words long.\n> ')
    job_lst.append(job_title)

job_urls = []
for i in job_lst:
    url = concat_url(i)
    job_urls.append(url)

urls_lst = []
for i in job_urls:
    urlz = add_page_num(i, int_pages)
    urls_lst.extend(urlz)
print(urls_lst)