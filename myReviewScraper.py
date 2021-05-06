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
    #courses = [12100, 12200,]
    evals = {}
    try: 
        evals = pickle.load(open('database.pkl', "rb"))
    except:
        pass
    courses = [12100,11800,15100,15200,15400,16100,16200,20300,20900,21800,22200,22500,22600,22800,23000,23200,23400,23500,23710,23900,25025,25300,25400,25460,25900,27100,27130,27200,27620,28130,28400,28510,30900,33231,33251,33281,33300,33750,34702,35200,35300,35401,35480,37115]
    for course in courses:
        scroll(driver)
        URL = get_url(driver, 'CMSC', course)
        flag = True
        while(flag):
            links = driver.find_elements_by_xpath("//td[@class='title']/a")
            results = driver.find_elements_by_xpath("//div[@class='search-results']")
            flag = not bool(len(results))
            time.sleep(0.1)
            for i in range(len(links)):
                #print(driver.get_cookies())
                #pickle.dump(driver.get_cookies() , open("cookies.pkl","wb+"))
                link = links[i]
                try:
                    link = link.get_attribute('href')
                except:
                    #print("reached")
                    time.sleep(0.1)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    links = driver.find_elements_by_xpath("//td[@class='title']/a")
                    time.sleep(0.1)
                    link = links[i]
                    link = link.get_attribute('href')
                    #continue
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
    pickle.dump(evals, open("database.pkl", "wb+"))
    #print(evals) 
    return evals

def get_url(driver, department, course):
    #URL = 'https://www.google.com'
    URL = 'https://evaluations.uchicago.edu/?CourseDepartment=' + str(department) + '&CourseNumber=' + str(course)
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
    
    #driver.maximize_window()
    return URL

def scroll(driver):
    # scroll to end of page
    html = driver.find_element_by_tag_name("html")
    html.send_keys(Keys.END)
    #time.sleep(0.5)
    driver.page_source
    
def parse(tag, section, questions_with_responses):
    comment_block = tag.find_all(class_="CommentBlockRow TableContainer")
    data_block = tag.find_all(class_="SpreadsheetBlockRow TableContainer")
    question_text = section[0].text.strip()
    if comment_block:
        responses = tag.find_all("td", "TabularBody_LeftColumn")
        responses_text = [response.text.strip() for response in responses]
        questions_with_responses[question_text] = {response_text: {} for response_text in responses_text}
    elif data_block:
        headers = data_block[0].find_all("th", class_="TabularHeader_RightBottomColumn")
        headers_text = [header.text.strip() for header in headers]
        entry = {}
        rows = tag.find_all("tr", class_="CondensedTabularOddRows") 
        for row in rows:
            sub_q = row.find("th", class_="TabularBody_LeftColumn")
            if sub_q:
                sub_q = sub_q.text.strip()
            else:
                sub_q = "Time spent"
                #continue
            responses = row.find_all("td", class_="TabularBody_RightColumn_NoWrap2")
            responses_text = {headers_text[i]:responses[i].text.strip() for i in range(len(responses))}
            entry[sub_q] = responses_text
        #print(entry)
        questions_with_responses[question_text] = entry
    
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
            section_h3 = tag.find_all("h3")
            if section_h3:
                section_h4 = tag.find_all("h4")
                if section_h4:
                    for section in section_h4:
                        parse(tag, section, questions_with_responses)
                parse(tag, section_h3, questions_with_responses)
           
            
            
                
                    
    print(title)
    #extractor.create_csv(questions_with_responses, 'test.csv')
    #html = extractor.create_html(questions_with_responses, 'test.csv')
    return (title, len(questions_with_responses) > 0, questions_with_responses)
