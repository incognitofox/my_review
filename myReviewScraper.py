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
    evals = {}
    try: 
        evals = pickle.load(open('database.pkl', "rb"))
    except:
        pass
    courses = [23300, 10000, 10100, 10200, 10500, 10600, 10700, 11000, 11100, 11111, 11200, 11300, 11500, 11600, 11700, 11710, 11800, 11900, 12100, 12200, 12300, 12500, 12600, 13600, 15100, 15200, 15300, 15400, 16100, 16200, 17400, 19911, 20300, 20370, 20600, 20900, 20910, 21010, 21400, 21500, 21800, 22000, 22001, 22010, 22100, 22200, 22240, 22300, 22311, 22400, 22500, 22600, 22610, 22620, 22630, 22800, 22880, 22900, 23000, 23001, 23010, 23200, 23210, 23220, 23230, 23240, 23270, 23280, 23300, 23310, 23320, 23340, 23360, 23400, 23500, 23700, 23710, 23800, 23900, 24000, 25000, 25010, 25020, 25025, 25030, 25040, 25050, 25100, 25300, 25400, 25440, 25460, 25610, 25620, 25700, 25900, 27000, 27100, 27130, 27200, 27230, 27400, 27410, 27500, 27502, 27530, 27600, 27610, 27620, 27700, 27800, 27900, 28000, 28100, 28130, 28400, 28500, 28501, 28510, 28515, 28520, 28530, 28540, 29500, 29512, 30100, 30210, 30370, 30600, 30900, 31000, 31010, 31015, 31090, 31100, 31140, 31150, 31230, 31500, 31510, 31900, 32001, 32002, 32100, 32102, 32200, 32201, 32400, 32600, 32620, 32630, 32700, 32900, 33000, 33000, 33001, 33100, 33200, 33210, 33230, 33231, 33240, 33250, 33251, 33260, 33270, 33281, 33300, 33310, 33340, 33400, 33500, 33501, 33510, 33520, 33550, 33580, 33581, 33600, 33601, 33700, 33710, 33720, 33750, 33900, 33950, 34000, 34200, 34500, 34700, 34701, 34702, 34703, 34710, 34900, 34901, 34901, 34910, 35000, 35040, 35050, 35100, 35110, 35120, 35200, 35230, 35246, 35300, 35350, 35360, 35400, 35401, 35410, 35420, 35425, 35470, 35480, 35490, 35500, 35510, 35600, 35610, 35620, 35900, 36100, 36500, 37000, 37100, 37101, 37110, 37115, 37120, 37200, 37220, 37300, 37400, 37500, 37501, 37502, 37503, 37530, 37600, 37700, 37701, 37720, 37800, 37810, 37811, 37812, 38000, 38100, 38130, 38200, 38300, 38400, 38405, 38410, 38500, 38502, 38510, 38511, 38512, 38600, 38700, 38800, 38815, 39000, 39010, 39020, 39100, 39200, 39300, 39500, 39600, 41600]
    for course in courses:
        scroll(driver)
        URL = get_url(driver, 'CMSC', course)
        flag = True
        while(flag):
            links = driver.find_elements_by_xpath("//td[@class='title']/a")
            results = driver.find_elements_by_xpath("//div[@class='search-results']")
            flag = not bool(len(results))
            time.sleep(0.1)
            driver.switch_to.window(driver.window_handles[0])
            for i in range(len(links)): 
                try:
                    link = links[i]
                    link = link.get_attribute('href')
                except:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    links = driver.find_elements_by_xpath("//td[@class='title']/a")
                    link = links[i];
                    link = link.get_attribute('href')
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(link)
                source = driver.page_source
                title, finished, questions = scrape(source)
                if finished:
                    evals[title] = questions
                    # close tab
                    driver.close()
                    # switch back to main tab
                    driver.switch_to.window(driver.window_handles[0])
                    scroll(driver)
                    flag = False
    pickle.dump(evals, open("database.pkl", "wb+"))
    return evals

def get_url(driver, department, course):
    URL = 'https://evaluations.uchicago.edu/?CourseDepartment=' + str(department) + '&CourseNumber=' + str(course)
    driver.get(URL)
    return URL

def scroll(driver):
    # scroll to end of page
    html = driver.find_element_by_tag_name("html")
    html.send_keys(Keys.END)
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
            responses = row.find_all("td", class_="TabularBody_RightColumn_NoWrap2")
            responses_text = {headers_text[i]:responses[i].text.strip() for i in range(len(responses))}
            entry[sub_q] = responses_text
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
