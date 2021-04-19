import sys
from bs4 import BeautifulSoup
import ssl
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import re
import extractor


def test():
    driver = webdriver.Chrome('./chromedriver.exe')
    #driver = webdriver.Chrome()
    scroll(driver)
    URL = get_url(driver)
    flag = True
    while(flag):
        links = driver.find_elements_by_xpath("//td[@class='title']/a")
        for link in links:
            link = link.get_attribute('href')
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(link)
            source = driver.page_source
            finished = scrape(source)
            if finished:
        		# close tab
                driver.close()
        		# switch back to main tab
                driver.switch_to.window(driver.window_handles[0])
                scroll(driver)
                flag = False
                break


def get_url(driver):
	#URL = 'https://www.google.com'
	URL = 'https://evaluations.uchicago.edu/?CourseDepartment=CMSC&CourseNumber=16100'
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
    print(questions_with_responses)
    extractor.create_csv(questions_with_responses)
    return len(questions_with_responses) > 0
                
                

def main():
    source = test()

if __name__ == "__main__":
    main()
