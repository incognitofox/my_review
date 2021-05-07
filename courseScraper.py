import sys
from bs4 import BeautifulSoup
import ssl
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import re

listOfPrograms = ['anthropology', 'architecturalstudies', 'arthistory', 'astronomyastrophysics', 'biologicalchemistry',
                  'biologicalsciences', 'chemistry', 'cinemamediastudies', 'classicalstudies', 'comparativehumandevelopment'
                  ,'comparativeliterature', 'caam', 'computerscience', 'creativewriting', 'comparativeraceethnicstudies'
                  , 'datascience', 'digitalstudies', 'eastasianlanguagescivilizations', 'economics', 'educationandsociety'
                  , 'englishlanguageliterature', 'environmentalscience', 'environmentalstudies', 'fundamentalsissuesandtexts'
                  , 'genderstudies', 'geographicalstudies', 'geophysicalsciences', 'germanicstudies', 'globalstudies'
                  , 'healthandsociety', 'history', 'scienceandmedicinehips', 'humanrights', 'inequalityandsocialchange'
                  , 'Inquiryresearchhumanities', 'jewishstudies', 'latinamericanstudies', 'lawlettersandsociety',
                  'linguistics', 'mathematics', 'MediaArtsandDesign', 'medievalstudies', 'molecularengineering',
                  'music', 'neareasternlanguagescivilizations', 'neuroscience', 'norwegianstudies', 'philosophy',
                  'physics', 'politicalscience', 'psychology', 'publicpolicystudies', 'quantitativesocialanalysis'
                  , 'religiousstudies', 'renaissancestudies', 'romancelanguagesliteratures', 'slaviclanguagesliteratures'
                  , 'sociology', 'southasianlanguagescivilizations', 'statistics', 'theaterperformancestudies',
                  'visualarts', 'yiddish']

def test():
    driver = webdriver.Chrome('chromedriver.exe')
    scroll(driver)
    for program in listOfPrograms:
        URL = get_url(driver, program)
        source = driver.page_source
        finished = scrape(source)
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
                break


def get_url(driver, program):
	#URL = 'https://www.google.com'
	URL = 'http://collegecatalog.uchicago.edu/thecollege/' + program
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

    catalog = soup.find_all("p", "courseblocktitle")
    courses_text = []
    for course in catalog:
        next = course.text.strip()
        #courses_text.append(next)
        if (next[10:11] == '.'):
            courses_text.append([next[0:4], next[5:10], next[13:-13]])
    print(courses_text)
    return len(courses_text) > 0

def main():
    source = test()

if __name__ == "__main__":
    main()