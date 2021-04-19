import sys
from bs4 import BeautifulSoup
import ssl
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import re


def test():
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
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
	#sleep(0.5)
	driver.page_source

def scrape(source):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    soup = BeautifulSoup(source, 'html.parser')

    class_comments = soup.find_all("td", "TabularBody_LeftColumn")
    comments_text = []
    for comment in class_comments:
        comments_text.append(comment.text.strip())
    print(comments_text)
    return len(comments_text) > 0

def main():
    source = test()

if __name__ == "__main__":
    main()
