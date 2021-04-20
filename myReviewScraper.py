import sys
from bs4 import BeautifulSoup
import ssl
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import re
import time
import extractor
import pickle
#import asyncio


def test():
    #driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    # for Windows machines, put chromedriver.exe in directory of project:
    driver = webdriver.Chrome('./chromedriver.exe')
    scroll(driver)
    URL = get_url(driver)
    flag = True
    while(flag):
        links = driver.find_elements_by_xpath("//td[@class='title']/a")
        evals = {}
        for link in links:
            #print(driver.get_cookies())
            #pickle.dump(driver.get_cookies() , open("cookies.pkl","wb+"))
            try:
                link = link.get_attribute('href')
            except:
                continue
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(link)
            source = driver.page_source
            title, finished, questions = scrape(source)
            #time.sleep(2)
            if finished:
                evals[title] = questions
                # close tab
                driver.close()
                # switch back to main tab
                driver.switch_to.window(driver.window_handles[0])
                #driver.close()
                scroll(driver)
                flag = False
    print(evals) 
    return evals

def get_url(driver):
    #URL = 'https://www.google.com'
    URL = 'https://evaluations.uchicago.edu/?CourseDepartment=CMSC&CourseNumber=16100'
    '''
    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            #print(cookie)
            #if 'expiry' in cookies and cookies['expiry'] > time.time():
            print(time.time())
            driver.add_cookie(cookie)
    except:
        print("cookies expired")
    '''
    driver.get(URL)
    
    driver.maximize_window()
    return URL

def scroll(driver):
    # scroll to end of page
    html = driver.find_element_by_tag_name("html")
    html.send_keys(Keys.END)
    time.sleep(0.5)
    driver.page_source

def scrape(source):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    soup = BeautifulSoup(source, 'html.parser')
    title = soup.find("title").text.strip()
    questions_with_responses = {}
    questions = soup.find_all(class_="report-block")
    for question in questions:
        for tag in questions:
            headers = tag.find_all("h3")
            if headers:
                question_text = headers[0].text.strip()
                responses = tag.find_all("td", "TabularBody_LeftColumn")
                responses_text = [response.text.strip() for response in responses]
                questions_with_responses[question_text] = responses_text
    print(title)
    #extractor.create_csv(questions_with_responses, 'test.csv')
    #html = extractor.create_html(questions_with_responses, 'test.csv')
    return (title, len(questions_with_responses) > 0, questions_with_responses)
