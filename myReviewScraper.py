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
    courses = set()
    try: 
        courses = pickle.load(open('courses.pkl', "rb"))
    except:
        pass
    evals = {course: {} for course in courses}   
    try: 
        evals = pickle.load(open('database4.pkl', "rb"))
    except:
        pass
    scraped = set()
    try: 
        scraped = pickle.load(open('scraped2.pkl', "rb"))
    except:
        pass
    for course in courses:
        department = course[0]
        course_num = course[1]
        print(course, end = " ")
        if(course in scraped):
            print("scraped.")
            continue
        else:
            print("scraping ...")
        scraped.add(course)
        #print(department + " " + course_num)
        scroll(driver)
        URL = get_url(driver, department, course_num)
        flag = True
        while(flag):
            links = driver.find_elements_by_xpath("//td[@class='title']/a")
            instructors = [instructor.get_attribute('innerHTML') for instructor in driver.find_elements_by_xpath("//td[@class='instructor']")]
            quarters = [quarter.get_attribute('innerHTML') for quarter in driver.find_elements_by_xpath("//td[@class='quarter']")]
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
                    instructors = [instructor.get_attribute('innerHTML') for instructor in driver.find_elements_by_xpath("//td[@class='instructor']")]
                    quarters = [quarter.get_attribute('innerHTML') for quarter in driver.find_elements_by_xpath("//td[@class='quarter']")]
                    link = links[i];
                    link = link.get_attribute('href')
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(link)
                source = driver.page_source
                time.sleep(0.1)
                title, finished, questions = scrape(source)
                if finished:
                    evals[course][(instructors[i], quarters[i], title)] = questions
                    # close tab
                    driver.close()
                    # switch back to main tab
                    driver.switch_to.window(driver.window_handles[0])
                    scroll(driver)
                    flag = False
            
        pickle.dump(evals, open("database4.pkl", "wb+"))
        pickle.dump(scraped, open("scraped2.pkl", "wb+"))
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
    chart_block = tag.find_all(class_="FrequencyBlockRow")
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
    elif chart_block:
        entry = {}
        title = tag.find_all("div", class_="FrequencyQuestionTitle")
        if title:          
            question_text = title[0].text.strip()
        img = tag.find_all("img")
        img_src =  "https://uchicago.bluera.com" + img[0]["src"]
        #extractor.parse_img(img_src, entry)
        entry["chart_src"] = img_src
        labels = tag.find_all("th", "TabularBody_LeftColumn")
        values = tag.find_all("th", "TabularBody_RightColumn_NoWrap")
        if(len(labels) and len(values)):
            for i in range(len(labels)):
                entry[labels[i].text.strip()] = values[i].text.strip()
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
    #print(title)
    #extractor.create_csv(questions_with_responses, 'test.csv')
    #html = extractor.create_html(questions_with_responses, 'test.csv')
    return (title, len(questions_with_responses) > 0, questions_with_responses)
