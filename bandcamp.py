from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(executable_path=r"C:/bin/chromedriver.exe", chrome_options=chrome_options)

browser.get('https://bandcamp.com')
browser.find_element_by_class_name('playbutton').click()
#browser.close()
#quit()